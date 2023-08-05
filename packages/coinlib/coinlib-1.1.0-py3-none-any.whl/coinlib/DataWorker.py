import grpc

from coinlib.helper import is_in_ipynb
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
from coinlib.helper import get_current_kernel
from coinlib.helper import log
from coolname import generate_slug
from coinlib.Registrar import Registrar
import time
import sys
from chipmunkdb.ChipmunkDb import ChipmunkDb

from coinlib.helper import pip_install_or_ignore
from coinlib.logics.LogicOfflineWorker import LogicOfflineWorker

pip_install_or_ignore("semver", "semver")

import os

from coinlib.statistics import StatisticsMethodWorker, StatisticsRuleWorker
from coinlib import ChartsWorker
from coinlib import PluginsWorker

import threading
import queue

import semver
from grpc._cython.cygrpc import CompressionAlgorithm
from grpc._cython.cygrpc import CompressionLevel


class WorkerJobListener:
    def __init__(self, simulator=False):
        self.registrar = Registrar()
        self.channel = self.createChannel()
        self.stub = stats.DataWorkerStub(self.channel)
        self.waitingQueue = None
        self.serverPlugins = None
        self.stopped = True
        self.simulator = simulator
        self.workerList = []

        file_name = os.path.basename(sys.argv[0])
        fixed_worker_file = file_name+".pid"
        if not is_in_ipynb:
            if os.path.exists(fixed_worker_file):
                with open(fixed_worker_file, 'r') as file:
                    self.workerId = file.read()
            else:
                self.workerId = self.generate_worker_id()
                f = open(fixed_worker_file, "a")
                f.write(self.workerId)
                f.close()
        else:
            self.workerId = self.generate_worker_id()

        availablePlugins = []
        try:
            all_plugins = self.getAllPluginsAvailable()
            for p in all_plugins:
                availablePlugins.append(statsModel.WorkerAvailablePlugins(name=p["name"], version=p["version"], type=p["module"]))
        except Exception as e:
            pass

        self.worker = statsModel.Worker(workerId=self.workerId,
                                        availablePlugins=availablePlugins,
                                        workspaceId=self.registrar.workspaceId,
                                        worker_mode=self.registrar.worker_mode,
                                        environment=self.registrar.environment)
        return None

    def createChannel(self):
        chan_ops = [('grpc.max_receive_message_length', 1000 * 1024 * 1024),
                    ('grpc.default_compression_algorithm', CompressionAlgorithm.gzip),
                    ('grpc.grpc.default_compression_level', CompressionLevel.high)]
        return grpc.insecure_channel(self.registrar.coinlib_backend, options=chan_ops,
                                     compression=grpc.Compression.Gzip)

    def getChannel(self):
        return self.channel

    def onWorkerJobProcessError(self, workerJobProcess, err):
        try:
            self.workerList.remove(workerJobProcess)
        except Exception as e:
            pass
        log.info("Errored Worker: " + str(workerJobProcess.workerJob))
        log.info("Now worker running: " + str(len(self.workerList)))
        workerError = statsModel.WorkerJobError()
        workerError.workerJobId = workerJobProcess.workerJob.workerJobId
        workerError.errorMessage = str(err)
        workerError.workerJobType = workerJobProcess.workerJob.workerJobType
        self.stub.ErroredWorkerJob(workerJobProcess.workerJob)

    def onWorkerJobProcessFinished(self, workerJobProcess):
        try:
            self.workerList.remove(workerJobProcess)
        except Exception as e:
            pass
        log.info("Finished Worker: " + str(workerJobProcess.workerJob))
        log.info("Now worker running: " + str(len(self.workerList)))
        self.stub.FinishedWorkerJob(workerJobProcess.workerJob)

    def generate_worker_id(self):
        if is_in_ipynb:
            return get_current_kernel()
        return self.get_random_string()

    def get_random_string(self, length=3):
        return generate_slug(length)

    def stop(self):
        self.stopped = True
        self.waitingQueue.put(None)

    def canWorkOnJob(self, job):
        return True

    def onJobStarted(self):
        pass

    def installPlugin(self, plugin):
        pluginWorker = PluginsWorker.PluginsWorker(None, self)
        pluginWorker.installPlugin(plugin)

    def checkIfPluginShouldInstall(self, pluginConfig):
        module_directory = ".chart_modules"
        if pluginConfig.type == "chart":
            module_directory = ".chart_modules"
        elif pluginConfig.type == "stats":
            module_directory = ".statsrules_modules"
        elif pluginConfig.type == "statsMethod":
            module_directory = ".statsmethod_modules"
        elif pluginConfig.type.startsWith("logics"):
            module_directory = ".logic_modules"

        if not os.path.exists(module_directory):
            os.makedirs(module_directory)

        file_name = None
        version = "?"
        for file_name in os.listdir("./"+module_directory):
            if file_name.startswith(pluginConfig.name):
                version = file_name.split(".")[0].split("_")[1]
                version = version.replace("-", ".")
                if semver.compare(pluginConfig.version, version) == 0:
                    return False
                break

        if file_name is not None:
            log.info("New Version for "+file_name+" => old: "+version+" new: "+pluginConfig.version)
        return True

    def getAllPluginsAvailable(self):

        plugins = []
        for module_directory in os.listdir("./"):
            if module_directory.startswith(".") and module_directory.endswith("_modules"):
                for file_name in os.listdir("./" + module_directory):
                    if file_name.endswith(".py"):
                        version = file_name.split(".")[0].split("_")[1]
                        plugin_name = file_name.split(".")[0].replace("_"+version, "")
                        version = version.replace("-", ".")
                        plugins.append({
                            "module": module_directory,
                            "name": plugin_name,
                            "file": file_name,
                            "file_path": "./"+module_directory+"/"+file_name,
                            "version": version
                        })

        return plugins

    def getDirectoryForPluginType(self, type):
        if type == "stats":
            return ".statsrules_modules"
        if type == "statsMethod":
            return ".statsmethod_modules"
        if type == "chart":
            return ".chart_modules"
        if type.startsWith("logics"):
            return ".logic_modules"
        return None

    def downloadAllPlugins(self):
        self.serverPlugins = self.stub.GetAllPlugins(self.worker)

        foundPlugins = []
        for p in self.serverPlugins.plugin:
            try:
                foundPlugins.append(p)
                if self.checkIfPluginShouldInstall(p):
                    self.installPlugin(p)
            except Exception as e:
                log.error("Error installing Plugin "+p.name, e)
                pass

        ## remove all
        availablePlugins = self.getAllPluginsAvailable()

        for p in availablePlugins:
            found = False
            for p2 in foundPlugins:
                dirName = self.getDirectoryForPluginType(p2.type)
                if p["name"].lower() == p2.name.lower() and dirName == p["module"]:
                    found = True

            if found == False:
                ## delete the plugin
                self.deletePlugin(p["file_path"])
                log.info("Deleteing Plugin "+p["name"])

    def deletePlugin(self, full_path):
        return os.remove(full_path)

    def wait_for_jobs(self):

        try:
            self.stub.RegisterWorker(self.worker)
            self.downloadAllPlugins()

            for job in self.stub.WatchWorkerJobs(iter(self.waitingQueue.get, None)):
                if (self.canWorkOnJob(job)):
                    self.acceptJob(job)
                else:
                    self.declineJob(job)

        except Exception as e:
            self.onErrorHappenedInCommunication(e)

    def onErrorHappenedInCommunication(self, e):
        start_time = threading.Timer(1, self.restart)
        start_time.start()

    def declineJob(self, job):
        self.stub.DeclineWorkerJob(job)

    def acceptJob(self, job):
        self.stub.AcceptWorkerJob(job)
        workerStartingThread = threading.Thread(target=self.startWorkerProcess, args=[job], daemon=True)
        workerStartingThread.start()

    def getWorkerBulkJobData(self, chartData):
        start = time.time()
        self.chipmunkDb = ChipmunkDb(self.registrar.chipmunkdb)
        df = self.chipmunkDb.collection_as_pandas(chartData.workspace_id, columns=[])
        end = time.time()
        log.info("Downloading DataFrame from chipmunk ", end - start)

        return df

    def runBulkProcesses(self, workerJob):
        # lets download
        statisticInterface = stats.StatisticsMethodWorkerStub(self.getChannel())
        statisticConfig = statisticInterface.GetConfig(workerJob)

        # download
        dataFrame = self.getWorkerBulkJobData(statisticConfig.chartData)

        for workerJobChildConfig in statisticConfig.configs:
            try:
                workerJobChild = None
                if workerJobChildConfig.HasField("rule"):
                    workerJobChild = StatisticsRuleWorker.StatisticsRuleWorker(workerJob, self)
                    workerJobChild.setConfig(workerJobChildConfig.rule)
                else:
                    workerJobChild = StatisticsMethodWorker.StatisticsMethodWorker(workerJob, self)
                    workerJobChild.setConfig(workerJobChildConfig.methodWindow)

                if workerJobChild is not None:
                    workerJobChild.startProcessWithDataFrame(dataFrame.copy())

            except Exception as e:
                log.error("Data", str(e))
                pass


        return None

    def generateWorkerProcess(self, workerJob):

       try:
           workerJobProcess = None
           # instantiate a new channel and stub so that the requests are parallel
           if workerJob.workerJobType == "stats":
               workerJobProcess = StatisticsRuleWorker.StatisticsRuleWorker(workerJob, self)
           elif workerJob.workerJobType == "statsMethod":
               workerJobProcess = StatisticsMethodWorker.StatisticsMethodWorker(workerJob, self)
           elif workerJob.workerJobType == "charts":
               workerJobProcess = ChartsWorker.ChartsWorker(workerJob, self)
           elif workerJob.workerJobType == "plugin":
               workerJobProcess = PluginsWorker.PluginsWorker(workerJob, self)
           elif workerJob.workerJobType == "runLogicOffline":
               workerJobProcess = LogicOfflineWorker(workerJob, self)
           elif workerJob.workerJobType == "forcePluginUpdates":
               self.reloadAllPlugins()
           else:
               log.error("Unknown Worker Type received")
               return workerJobProcess
       except Exception as e:
           log.error("Erorr in creating worker", e)
           pass

       return workerJobProcess


    def startWorkerProcess(self, workerJob):
        try:
            workerJobProcess = None

            if workerJob.workerJobType == "statsBulked":
                return self.runBulkProcesses(workerJob)
            else:
                workerJobProcess = self.generateWorkerProcess(workerJob)

            self.workerList.append(workerJobProcess)
            log.info("Now worker running: " + str(len(self.workerList)))

            workerJobProcess.startProcess()
            return workerJobProcess
        except Exception as e:
            log.error(e)
            pass

    def reloadAllPlugins(self):

        self.registrar.chartsFactory.reloadPlugins()
        self.registrar.statsRuleFactory.reloadPlugins()
        self.registrar.statsMethodFactory.reloadPlugins()

        return True

    def reloadPluginsForType(self, type):

        if (type == "chart"):
            self.registrar.chartsFactory.reloadPlugins()
        if (type == "stats"):
            self.registrar.statsRuleFactory.reloadPlugins()
        if (type == "statsMethod"):
            self.registrar.statsMethodFactory.reloadPlugins()

        return True

    def restart(self):
        if (self.stopped == False):
            if (self.waitingQueue != None):
                self.waitingQueue.put(None)
            self.waitingQueue = None
            self.waitingQueue = queue.SimpleQueue()
            listenThread = threading.Thread(target=self.wait_for_jobs, daemon=True)
            listenThread.start()

    def start(self):
        if (self.stopped == False):
            self.stop()
        self.stopped = False
        self.restart()


