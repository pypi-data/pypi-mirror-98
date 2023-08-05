from coinlib.logics.LogicLoader import LogicFactory
from coinlib.helper import get_current_kernel
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
from grpc._cython.cygrpc import CompressionAlgorithm
from grpc._cython.cygrpc import CompressionLevel
import grpc
from coinlib.helper import in_ipynb
from coinlib.statistics.StatisticsMethodLoader import StatisticsMethodFactory
from coinlib.ChartsLoader import ChartsFactory
from coinlib.statistics.StatisticsRuleLoader import StatisticsRuleFactory

from coinlib.Registrar import Registrar
import simplejson as json

from coinlib.DataWorker import WorkerJobListener


class Simulator:
    def __init__(self):
        self._isConnected = False
        self._registrar = Registrar()
        if self.__isLiveStage() == False:
            self.channel = self.__createChannel()
            self.stub = stats.SimulatorStub(self.channel)
            self.workerJobs = None

        return None

    def connect(self):
        self._isConnected = True
        if not self._registrar.isRegistered:
            self.__registerAsWorker()

    def __isLiveStage(self):
        return self._registrar.isLiveEnvironment()

    def __registerAsWorker(self):
        if self.__isLiveStage():
            return False
        if not self._registrar.isRegistered:
            self.workerJobs = WorkerJobListener(simulator=True)
            self.workerJobs.start()
            self._registrar.isRegistered = True

            self._registrar.statsRuleFactory = StatisticsRuleFactory()
            self._registrar.statsMethodFactory = StatisticsMethodFactory()
            self._registrar.chartsFactory = ChartsFactory()
            self._registrar.logicFactory = LogicFactory()


        return True

    def __createChannel(self):
        chan_ops = [('grpc.max_receive_message_length', 1000 * 1024 * 1024),
                    ('grpc.default_compression_algorithm', CompressionAlgorithm.gzip),
                    ('grpc.grpc.default_compression_level', CompressionLevel.high)]
        return grpc.insecure_channel(self._registrar.coinlib_backend, options=chan_ops,
                                     compression=grpc.Compression.Gzip)

    def plot(self, plotly_fig):

        if self.__isLiveStage():
            return False
        self.__registerAsWorker()

        json = plotly_fig.to_json()

        if in_ipynb():
            iframe_src = 'http://'+self._registrar.iframe_host+'/simulator/plotly/'+get_current_kernel()

            self.__displayCoinChartFrame(iframe_src, iframe_width=str(1140), message='{type: "jupyter", plotly:'+json+', command: "reloadPlotlyChartData"}')


        return True

    def statsMethod(self, methods, name="simulatorDefaultWorkspace"):

        if self.__isLiveStage():
            return False
        self.__registerAsWorker()

        simulatorChartConfig = statsModel.SimulatorMethodCallChartConfig()
        simulatorChartConfig.kernel_id = get_current_kernel()
        simulatorChartConfig.simulatorName = name
        simulatorChartConfig.workerId = self.workerJobs.workerId

        for method in methods:
            meth = statsModel.SimulatorMethodCall()
            meth.method = method["method"]
            meth.params = str(json.dumps(method["params"], ignore_nan=True))

            simulatorChartConfig.methods.append(meth)

        info = self.stub.simulateStatisticsMethod(simulatorChartConfig)


        if in_ipynb():
            iframe_src = 'http://localhost:3000/simulator/statsMethod/'+info.workspaceId+"/"+get_current_kernel()

            self.__displayCoinChartFrame(iframe_src,
                                         iframe_width=str(1140),
                                         messageData=str(json.dumps({"methods": methods,
                                                                     "workspaceId": info.workspaceId}, ignore_nan=True)))

        return True

    def statsRule(self, name="simulatorDefaultWorkspace"):

        if self.__isLiveStage():
            return False
        self.__registerAsWorker()

        simulatorChartConfig = statsModel.SimulatorStatisticChartConfig()
        simulatorChartConfig.kernel_id = get_current_kernel()
        simulatorChartConfig.simulatorName = name

        info = self.stub.simulateStatisticsRule(simulatorChartConfig)

        if in_ipynb():
            iframe_src = 'http://localhost:3000/simulator/stats/'+info.workspaceId+"/"+get_current_kernel()

            self.__displayCoinChartFrame(iframe_src,
                                         messageData=str(json.dumps({"workspaceId": info.workspaceId}, ignore_nan=True)),
                                         iframe_width=str(1140))


        return True

    def __displayCoinChartFrame(self, iframe_src, iframe_width = str(980), iframe_height = str(360), messageData='', message=''):
        from IPython.display import Javascript
        from IPython.core.display import display
        postmessage = message
        if (messageData == ''):
            messageData = "{}"

        if message == "":
            postmessage = '{type: "jupyter", kernel_id: "'+get_current_kernel()+'", command: "reloadChartDataFromNotebook", data: '+messageData+'}'
        display(Javascript(' const currentNotebookPanel = document.querySelector(".jp-NotebookPanel:not(.p-mod-hidden)");'\
                           ' if (currentNotebookPanel.querySelector(".coinchartoutput") != null) '\
                           ' { '\
                           '    currentNotebookPanel.querySelector(".coinchartoutput").querySelector("iframe").contentWindow.postMessage('+postmessage+', "*"); '\
                           ' } '\
                           ' else '\
                           ' { '\
                           '    const elem = document.createElement("div"); '\
                           '    elem.innerHTML = "<iframe src=\'' + iframe_src + '\' border=0 width=\'' + iframe_width + '\' height=\'' + iframe_height + '\' />";'\
                           '    elem.style = "position: absolute;width:' + iframe_width + 'px;height:' + iframe_height + 'px;bottom: 0px;opacity: 0.9;z-index: 9999;"; '\
                           '    elem.className = "coinchartoutput";'\
                           '    currentNotebookPanel.appendChild(elem); '\
                           ' } '))

        return True

    def chart(self, broker, symbol, timeframe, indicators):

        if self.__isLiveStage():
            return False
        self.__registerAsWorker()

        simulatorChartConfig = statsModel.SimulatorChartConfig()
        simulatorChartConfig.kernel_id = get_current_kernel()
        simulatorChartConfig.broker = broker
        simulatorChartConfig.symbol = symbol
        simulatorChartConfig.timeframe = timeframe
        simulatorChartConfig.workerId = self.workerJobs.workerId
        indilist = []
        for indi in indicators:
            indicator = statsModel.SimulatorChartConfigIndicator()
            indicator.feature = indi["feature"]
            indicator.subfeature = indi["subfeature"]
            if "chartIndex" in indi:
                indicator.chartIndex = indi["chartIndex"]

            for key in indi["inputs"]:
                indicator.inputs[key] = str(indi["inputs"][key])

            simulatorChartConfig.indicators.append(indicator)

        self.stub.simulateChart(simulatorChartConfig)

        if in_ipynb():
            iframe_src = 'http://localhost:3000/simulator/chart/'+get_current_kernel()

            self.__displayCoinChartFrame(iframe_src)

        return True