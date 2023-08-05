import time
import grpc
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import datetime 
import threading
import pandas as pd
import queue
import inspect
import numpy as np
import grpc
import asyncio

from coinlib.helper import log
import simplejson as json
import traceback
from coinlib.WorkerJobProcess import WorkerJobProcess
from coinlib.Registrar import Registrar
from multiprocessing import Pool
import multiprocessing
import zlib
from chipmunkdb.ChipmunkDb import ChipmunkDb


from coinlib.ChartsIndicatorJob import ChartsIndicatorJob

class ChartsSeriesDataResult:
    """ Point class represents and manipulates x,y coords. """

    def __init__(self):
        """ Create a new point at the origin """
        self.output_name = None
        self.result_data = None
        self.indicator = None
        self.options = None


class ChartsWorker(WorkerJobProcess):
    
    def initialize(self):
        self.dataFrameLock = threading.Lock()
        self.registrar = Registrar()
        self.result_list = []
        self.final_result_list = []
        self.chartsInterface = stats.ChartsWorkerStub(self.getChannel())
        self.chartConfig = self.chartsInterface.GetConfig(self.workerJob)
        self.chartConfigData = self.chartConfig.chartData
        pass
        
    def getIndicatorConfiguration(self, element):
        return json.loads(str(element.indicatorConfig, 'ascii'))
    
    def getIndicatorMethod(self, indicator):
        found_method = None
        registeredFunctions = self.registrar.functionsCallbacks
        
        if registeredFunctions[indicator.feature+"."+indicator.subfeature] is not None:
            found_method = registeredFunctions[indicator.feature+"."+indicator.subfeature]
        
        return found_method

    def onErrorOnIndicatorHappened(self, indicator_element, error):

        indicatorError = statsModel.IndicatorError()
        indicatorError.error.message = str(error)
        indicatorError.worker.CopyFrom(self.workerJob)
        indicatorError.indicator.CopyFrom(indicator_element.indicator)

        self.chartsInterface.OnIndicatorErrorOccured(indicatorError)

        return False

    def runIndicatorCalculation(self, indicator_element):
        process = None
        try:
            start = time.time()
            targetIndicatorFunction = self.getIndicatorMethod(indicator_element.indicator)
            inputs = self.getIndicatorConfiguration(indicator_element)

            raw_inputs = self.extractInputsFromDataFrameAndInsertInDataFrame(inputs)
            raw_inputs["name"] = indicator_element.indicator.subfeature
            raw_inputs["group"] = indicator_element.indicator.feature

            chart = ChartsIndicatorJob(indicator_element.indicator.subfeature, indicator_element.indicator.feature,
                                       inputs, self.dataFrame.copy(), indicator_element, self)
            chart.setUniqueName(indicator_element.indicator.name)

            start = time.time()
            if (inspect.iscoroutinefunction(targetIndicatorFunction["process"])):
                async def runandwait():
                    result = await asyncio.wait(
                        [targetIndicatorFunction["process"](raw_inputs, chart)],
                        return_when=asyncio.FIRST_COMPLETED)

                loop = asyncio.new_event_loop()
                process = loop.run_until_complete(runandwait())
            else:
                process = targetIndicatorFunction["process"](raw_inputs, chart)

            log.info("running indicator finished " + indicator_element.indicator.subfeature, time.time() - start)
        except Exception as e:
            tb = traceback.format_exc()
            log.error(tb)
            log.error("Error on indicator")
            log.error(e)
            self.onErrorOnIndicatorHappened(indicator_element, e)
            pass

        return process

    def sendPartialChartData(self, indicator, output_name, options):

        partialData = statsModel.ChartsWorkerPartialDataLayout()
        partialData.chartInfo.name = output_name
        partialData.chartInfo.chartType = options["chartType"]
        if "color" in options:
            partialData.chartInfo.color = options["color"]
        if "size" in options:
            partialData.chartInfo.size = options["size"]
        if "opacity" in options:
            partialData.chartInfo.opacity = options["opacity"]

        # send raw data to Influx and then inform the listener
        #self.influxdb.insertChartSeries(output_name, result_data)

        indexes = self.dataFrame.index

       # self.influxDb.writeRawDataColumn(self.chartConfigData.chart_id, output_name, indexes, result_data)

        partialData.worker.CopyFrom(self.workerJob)
        partialData.indicator.CopyFrom(indicator.indicator)

        self.chartsInterface.OnPartialChartLayout(partialData)

    def pushAllResultsToCurrentDataFrame(self):

        targetColumns = []
        for result in self.result_list:

            targetLength = len(self.dataFrame.index)

            for key in result.result_data:
                if len(result.result_data[key]) > 0:
                    output_padded = np.pad(result.result_data[key], (targetLength - len(result.result_data[key]), 0), 'constant',
                                           constant_values=np.nan)
                    self.dataFrame[result.output_name+key] = output_padded
                    targetColumns.append(result.output_name+key)


        return True

    def onPartialChartDataReceived(self, indicator, name, result_data, options):
        output_name = indicator.indicator.id_output

        name = name.replace(indicator.indicator.subfeature, "")

        if output_name is None or output_name == "":
            output_name = indicator.indicator.name + ("." + name if name != "" else "")

        ## lets send the data to the chart worker
        #t = threading.Thread(target=self.sendPartialChartData, args=[indicator, output_name, result_data, options], daemon=True)
        #t.start()
        self.sendPartialChartData(indicator, output_name, options)

        series = ChartsSeriesDataResult()
        series.output_name = output_name
        series.result_data = result_data
        series.indicator = indicator
        series.options = options
        self.result_list.append(series)

        for c in result_data.columns:
            self.final_result_list.append(output_name+c)

        return True
    
    def calculateNextElements(self, chartConfig):
        workerJobs = []
        self.result_list = []

        for element in chartConfig.elements:
            ##t = self.runIndicatorCalculation(element, return_dict)
            #t = multiprocessing.Process(target=self.runIndicatorCalculation, args=[element])
            t = threading.Thread(target=self.runIndicatorCalculation, args=[element], daemon=True)

            workerJobs.append(t)

        # Start all threads
        for x in workerJobs:
            x.start()

        # Wait for all of them to finish
        for x in workerJobs:
            x.join()

        # pushing all received datas to the dataframe
        # and proceed to next corresponding indicators
        self.pushAllResultsToCurrentDataFrame()

        try:
            if len(chartConfig.children.elements) > 0:
                self.calculateNextElements(chartConfig.children)
        except:
            pass
            
        return True
        
    def run(self):

        start = time.time()
        self.calculateNextElements(self.chartConfig)
        log.info("Finished complete calculation ", time.time() - start)
        ## let ssave all
        target_columns = self.final_result_list
        only_relevant_columns_df = self.dataFrame[target_columns]

        start = time.time()
        self.chipmunkDb.save_as_pandas(only_relevant_columns_df, self.chartConfigData.workspace_id,
                                  mode="append",
                                  domain=self.chartConfigData.chart_prefix)
        end = time.time()
        log.info("Saving DataFrame to chipmunk ", end - start)
        ##self.influxDb.writeDataFrame(self.chartConfigData.chart_id, self.dataFrame)
            
        