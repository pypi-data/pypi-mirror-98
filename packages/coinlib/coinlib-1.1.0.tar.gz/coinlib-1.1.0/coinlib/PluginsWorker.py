import time
import grpc
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import datetime 
import threading
from coinlib.helper import log
import pandas as pd
import queue
import inspect
import numpy as np
import grpc
import glob
from shutil import copyfile
import random
import string
import asyncio
import simplejson as json
from coinlib.WorkerJobProcess import WorkerJobProcess
from coinlib.Registrar import Registrar
import zlib
import os
from coinlib.helper import pip_install_or_ignore

pip_install_or_ignore("jupyter", "jupyter")

class PluginsWorker(WorkerJobProcess):
    
    def initialize(self):
        self.registrar = Registrar()
        self.pluginsInterface = stats.PluginWorkerStub(self.getChannel())
        self.config = self.pluginsInterface.GetConfig(self.workerJob)
        pass

    def get_random_string(self, length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def convertNotebookToPython(self, fileContent):
        random_name = self.get_random_string(10)
        file_input = random_name+".ipynb"
        with open(file_input, 'w') as modified: modified.write(fileContent)

        file_output = random_name
        file_output_py = file_output + ".py"

        os.system("jupyter nbconvert --to script " + file_input + "  --output " + file_output)

        os.remove(file_input)
        appending_lines = 'import sys\n' \
                          'sys.path.insert(0, "..")\n' \
                          'from IPython import get_ipython\n'

        with open(file_output_py, 'r') as original: data = original.read()
        with open(file_output_py, 'w') as modified: modified.write(appending_lines + data)
        with open(file_output_py, 'r') as original: complete_file_data = original.read()

        os.remove(file_output_py)

        return complete_file_data

    def archiveModulesWithName(self, moduleName, module_dir):

        if not os.path.exists("../archive"):
            os.makedirs("../archive")

        for file_name in os.listdir("./"+module_dir):
            if file_name.startswith(moduleName):
                file_comp = os.path.join(module_dir, file_name)
                file_arch = os.path.join("../archive", "asd" + file_name)
                copyfile(file_comp, file_arch)
                os.remove(file_comp)

        return True

    def writeModuleWithNameAndVersion(self, name, version, pythoncontent, module_dir):
        version_fixed = str(version).replace(".", "-").replace("/", "-").replace(":", "-")
        complete_name = "./"+module_dir+"/"+name+"_"+version_fixed+".py"

        with open(complete_name, 'w') as modified: modified.write(pythoncontent)

        return True

    def installPlugin(self, pluginConfig):
        try:
            workerJobs = []

            pythoncontent = self.convertNotebookToPython(pluginConfig.filecontent)

            module_directory = ".chart_modules"
            if pluginConfig.type == "chart":
                module_directory = ".chart_modules"
            elif pluginConfig.type == "stats":
                module_directory = ".statsrules_modules"
            elif pluginConfig.type == "statsMethod":
                module_directory = ".statsmethod_modules"

            if not os.path.exists(module_directory):
                os.makedirs(module_directory)

            self.archiveModulesWithName(pluginConfig.name, module_directory)

            self.writeModuleWithNameAndVersion(pluginConfig.name, pluginConfig.version, pythoncontent, module_directory)

            self.factory.reloadPluginsForType(pluginConfig.type)
        except Exception as e:
            log.error("Error on installing", e)
            pass
            
        return True
        
    def run(self):
        
        self.installPlugin(self.config)
            
        