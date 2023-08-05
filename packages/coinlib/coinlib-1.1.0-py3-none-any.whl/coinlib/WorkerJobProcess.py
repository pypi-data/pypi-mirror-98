import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import threading
import time
from coinlib.helper import log
import pandas as pd
import queue
import grpc
import simplejson as json
import traceback
import zlib
import binascii
from coinlib.Registrar import Registrar
from coinlib.InfluxDatabase import InfluxDatabase
from chipmunkdb.ChipmunkDb import ChipmunkDb

class WorkerJobProcess:
    def __init__(self, workerJob, factory):
        self.workerChannel = factory.createChannel()
        self.registrar = Registrar()
        self.chipmunkDb = ChipmunkDb(self.registrar.chipmunkdb)
        self.stub = stats.DataWorkerStub(self.workerChannel)
        self.workerJob = workerJob
        self.stopped = True
        self.currentWorkerJobData = []
        self.factory = factory
        self.dataFrame = pd.DataFrame()
        return None

    def generateRawData(self, result_data):

        result_data_json = str(json.dumps(result_data, ignore_nan=True)).encode('utf8')
        result_data_json_compressed = zlib.compress(bytes(result_data_json))

        return result_data_json_compressed

    def getDataFrameColumn(self, key, column_name, _type="base"):
        try:
            if column_name+":open" in self.dataFrame.columns:
                dfCopy = self.dataFrame[[column_name+":open", column_name+":high",
                                        column_name+":low", column_name+":close", column_name+":volume"]].copy()
                dfCopy["open"] = dfCopy[column_name+":open"]
                dfCopy["high"] = dfCopy[column_name + ":high"]
                dfCopy["low"] = dfCopy[column_name + ":low"]
                dfCopy["close"] = dfCopy[column_name + ":close"]
                dfCopy["volume"] = dfCopy[column_name + ":volume"]

                #self.dataFrame[key + ":open"] = self.dataFrame[column_name + ":open"]
                #self.dataFrame[key + ":open"] = self.dataFrame[column_name + ":high"]
                #self.dataFrame[key + ":low"] = self.dataFrame[column_name + ":low"]
                #self.dataFrame[key + ":close"] = self.dataFrame[column_name + ":close"]
                #self.dataFrame[key + ":volume"] = self.dataFrame[column_name + ":volume"]

                return dfCopy
            elif column_name+":y" in self.dataFrame.columns:
                return self.dataFrame[column_name + ":y"].copy()

        except Exception as e:
            log.error("Assert error")
            pass

        return self.dataFrame[column_name]

    def extractInputsFromDataFrameAndInsertInDataFrame(self, inputs):
        raw_inputs = {}
        for key in inputs:
            try:
                inputVal = inputs[key]
                type = inputVal["type"]
                value = inputVal["value"]
                if type == "symbol":
                    val = value
                    if isinstance(val, dict):
                        val = value["id"] if "id" in value else value["value"]
                    raw_inputs[key] = self.getDataFrameColumn(key, val, _type="ohlc")
                elif type == "dataInput" or type == "any":
                    val = value
                    if isinstance(val, dict):
                        val = value["id"] if "id" in value else value["value"]
                    raw_inputs[key] = self.getDataFrameColumn(key, val, _type="ohlc")
                elif type == "feature":
                    val = value
                    if isinstance(val, dict):
                        val = value["id"] if "id" in value else value["value"]
                    raw_inputs[key] = self.getDataFrameColumn(key, val)
                elif type == "any":
                    raw_inputs[key] = value
                    self.dataFrame[key] = value
                elif type == "number":
                    raw_inputs[key] = value
                    self.dataFrame[key] = value
                elif type == "int":
                    raw_inputs[key] = value
                    self.dataFrame[key] = value
                elif type == "float":
                    raw_inputs[key] = value
                    self.dataFrame[key] = value
                else:
                    raw_inputs[key] = value
                    self.dataFrame[key] = value
            except Exception as e:
                tb = traceback.format_exc()
                log.error("Problem on extracting data", e)
                pass

        return raw_inputs

    def initialize(self):
        pass
    
    def getDf(self):
        return self.dataFrame
    
    def getChannel(self):
        return self.workerChannel
        
    def getWorkerJobDataFrame(self, workerJob):
        df = pd.DataFrame()
        if hasattr(self, 'chartConfigData'):

            configData = self.chartConfigData
            start = time.time()
            if configData.chart_prefix:
                df = self.chipmunkDb.collection_as_pandas(configData.workspace_id, columns=[],
                                                          domain=configData.chart_prefix)
            else:
                df = self.chipmunkDb.collection_as_pandas(configData.workspace_id, columns=[])
            end = time.time()
            log.info("Downloading DataFrame from chipmunk ", end - start)

            if configData.chart_prefix != "" and configData.chart_prefix is not None:
                df.columns = df.columns.str.replace('^'+configData.chart_prefix + ".", "", regex=True)

                if "symbol." not in df.columns:
                    # we need to copy open, high, low, close
                    key = "symbol"
                    df[key + ":open"] = df["main:open"]
                    df[key + ":high"] = df["main:high"]
                    df[key + ":low"] = df["main:low"]
                    df[key + ":close"] = df["main:close"]
                    df[key + ":volume"] = df["main:volume"]

        return df

        # currentWorkerJobData = b''
        #for dataBlock in self.stub.GetWorkerJobData(workerJob):
        #    currentWorkerJobData = currentWorkerJobData + bytes(dataBlock.data)

        #if len(currentWorkerJobData) > 0:
        #    decompressed_data = zlib.decompress(currentWorkerJobData, 15 + 32)
        #    df = pd.DataFrame(json.loads(decompressed_data))
        #    df['Datetime'] = pd.to_datetime(df['datetime'], unit='s')
        #    df = df.set_index(['Datetime'])
        #else:
        #    df = pd.DataFrame()

        #return df
    
    def runProcess(self):
        try:
            self.run()

        except Exception as e:
            log.error(e)
            self.onErrorProcess(e)
            return

        log.info("Finished")
        self.onFinishedProcess()
    
    def run(self):
        pass

    def onErrorProcess(self, e):
        self.stop()
        self.factory.onWorkerJobProcessError(self, e)

    def onFinishedProcess(self):
        self.stop()
        self.factory.onWorkerJobProcessFinished(self)
        
    def stop(self):
        self.stopped = True
        #self.listenThread.join()
        
    def onBeforeDownloadData(self):
        pass
    
    def downloadAndRunprocess(self):
        self.onBeforeDownloadData()

        self.initialize()
        self.dataFrame = self.getWorkerJobDataFrame(self.workerJob)
        if (self.stopped == False):
            self.stop()
            self.stopped = True
            
        self.listenThread = threading.Thread(target=self.runProcess, daemon=True)
        self.listenThread.start()
            
        return True

    def startProcessWithDataFrame(self, dataFrame):
        self.onBeforeDownloadData()

        self.initialize()
        self.dataFrame = dataFrame
        if (self.stopped == False):
            self.stop()
            self.stopped = True

        self.listenThread = threading.Thread(target=self.runProcess, daemon=True)
        self.listenThread.start()

        return True

    def startProcess(self):
        
        downloadThread = threading.Thread(target=self.downloadAndRunprocess, daemon=True)
        downloadThread.start()

        pass

    def setConfig(self, configuration):
        pass
    
    