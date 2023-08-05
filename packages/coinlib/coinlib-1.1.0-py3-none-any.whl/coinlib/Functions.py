from coinlib.helper import get_current_kernel
import copy 
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import json
from coinlib.helper import is_in_ipynb
import ipynb_path
from grpc._cython.cygrpc import CompressionAlgorithm
from grpc._cython.cygrpc import CompressionLevel
import grpc
from coinlib.Registrar import Registrar
from google.protobuf.json_format import MessageToDict
import os
import sys

class Functions:
    def __init__(self):
        self.registrar = Registrar()
        pass

    def connect(self):
        self.channel = self.createChannel()
        self.functionsInterface = stats.FunctionsStub(self.channel)
        pass

    def createChannel(self):
        chan_ops = [('grpc.max_receive_message_length', 1000 * 1024 * 1024),
                    ('grpc.default_compression_algorithm', CompressionAlgorithm.gzip),
            ('grpc.grpc.default_compression_level', CompressionLevel.high)]
        return grpc.insecure_channel(self.registrar.coinlib_backend, options=chan_ops, compression=grpc.Compression.Gzip)
        
    def registerChartFunction(self, process, group, name, short, inputs, description, 
                              dynamicTimeseries=False, unstablePeriod=False, mode=""):
        """
            dynamicTimeseries =  for example ATR based charts which have the special problem of "recalculating" past events (for example renko) 
                            If dynamicTimeseries != False then we will handle this indicator very special
        """
        inputs.insert(0, {"type": "symbol", "name": "symbol", "required": "true"})
        
        self.registerIndicatorFunction(process, group, name, short, 
                                       inputs, description, type="chartType", chartType="line", mode=mode,
                                       dynamicTimeseries=dynamicTimeseries, unstablePeriod=unstablePeriod)
        
        return True
        

    
    def registerIndicatorFunction(self, process, group, name, short, inputs, 
                                  description, chartType="", type="function", mode="",
                                  dynamicTimeseries=False, unstablePeriod=False):
        """Register Indicator with callback Functions.
        
            types: 
                - color
                - integer
                - float
                - symbol
                - series
                - select
                - feature
                    if you need some features we fetch it for you and push it as an input
                    format of features:
                
                    {name: inputname, feature: featureName, subfeature: None}
                
        
        """
        
        registration = statsModel.ChartWorkerIndicatorRegistration()
        registration.chartType = chartType
        registration.name = name
        registration.group = group
        registration.short_description = short
        registration.dynamicTimeseries = dynamicTimeseries
        registration.type = type
        registration.mode = mode
        registration.inputs = json.dumps(inputs, ensure_ascii=False).encode('gbk')
        registration.stage = self.registrar.environment
        registration.description = description


        if not is_in_ipynb:
            namespace = sys._getframe(1).f_globals
            cwd = os.getcwd()
            rel_path = namespace['__file__']
            abs_path = os.path.join(cwd, rel_path)
            only_filename = os.path.splitext(os.path.basename(abs_path))[0]
            splitted = only_filename.split("_")
            only_filename_without_version = "_".join(splitted[:-1])

            registration.plugin = only_filename_without_version
            registration.pluginVersion = splitted[-1].replace("-", ".")
        else:
            abs_path = ipynb_path.get()
            only_filename = os.path.splitext(os.path.basename(abs_path))[0]

            registration.plugin = only_filename
            registration.pluginVersion = "?"

        registration_dict = MessageToDict(registration)
        
        # before we send the data, we need to add the "callback"
        # to a global handler list
        self.registrar.functionsCallbacks[group+"."+name] = registration_dict
        self.registrar.functionsCallbacks[group+"."+name]["process"] = process
        
        self.functionsInterface.registerIndicatorFunction(registration)
        
        return True

    
