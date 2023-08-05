from coinlib.helper import get_current_kernel
import copy 
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import json
from grpc._cython.cygrpc import CompressionAlgorithm
from grpc._cython.cygrpc import CompressionLevel
import grpc
from coinlib.Registrar import Registrar
from google.protobuf.json_format import MessageToDict

class Features:
    def __init__(self):
        self.registrar = Registrar()
        pass

    def connect(self):
        self.channel = self.createChannel()
        self.featuresInterface = stats.FeaturesStub(self.channel)
        return True

    def createChannel(self):
        chan_ops = [('grpc.max_receive_message_length', 1000 * 1024 * 1024),
                    ('grpc.default_compression_algorithm', CompressionAlgorithm.gzip),
            ('grpc.grpc.default_compression_level', CompressionLevel.high)]
        return grpc.insecure_channel(self.registrar.coinlib_backend, options=chan_ops, compression=grpc.Compression.Gzip)
        
        
        
    def registerMarketFeatureData(self, name, field, chartType="line", unit=None, dstype=None, info_url=None, 
                                  source=None, title=None, short=None, description=None, interval=None):
        """Register Market Feature Data so that others know what this feature is.
        name : The name of your feature
        return : This is return
        """
        
        sendDataMessage({'cmd': 'registerMarketFeatureData', 'name': name, 'unit': unit, 'info_url': info_url, 'source': source, 
                         'field': field, 'chartType': chartType, 'short_description': short, 'type': dstype, 'interval': interval, 'description': description, 'title': title})
        
        return True;
    
            
    def registerSymbolFeatureData(self, name, field, chartType="line", unit=None, symbol="*", info_url=None,  
                                  source=None, dstype=None, title=None, interval=None, short=None, description=None):
        """Register Symbol Feature Data so that others know what this feature is.
        name : The name of your feature
        return : This is return
        """
        
        sendDataMessage({'cmd': 'registerSymbolFeatureData', 'field': field, 'interval': interval, 'unit': unit,  'info_url': info_url, 'source': source,  'chartType': chartType, 'symbol': symbol, 'name': name, 'type': dstype, 
                         'description': description, 'short_description': short, 'title': title})
        
        return True;
    
    
    
    
    def addMarketFeatureData(self, name, value,time=None, dstype=None, elementTitle=None, description=None):
        """Generate Market Feature Data Block
        name : The name of your feature
        return : This is return
        """
        if (time == None):
            time = datetime.now()
            
        if ("datetime" in str(type(time))):
            time = str(time)
        
        sendDataMessage({'cmd': 'addMarketFeatureData', 'name': name, 'type': dstype, 'description': description, 
                         'title': elementTitle, 'time': time, 'value': value})
        
        return True;
    
    
    def addSymbolFeatureData(self, symbol, name, value, time=None, dstype=None, elementTitle=None, description=None):
        """Generate Symbol Feature Data Block
        name : The name of your feature
        return : This is return
        """
        if (time == None):
            time = datetime.now()
            
        if ("datetime" in str(type(time))):
            time = str(time)
            
        sendDataMessage({'cmd': 'addSymbolFeatureData', 'symbol': symbol, 'description': description, 'type': dstype, 'title': elementTitle,
                         'name': name, 'time': time, 'value': value})
        
        return True;
    
    def getSymbolsSync(self, symbol, features=[], marketFeatures=[], timeframe="1h", onlyFinal=True, ranges="15", dateFrom=None, dateTo=None):
        global syncResutl
        syncResutl = None
        def runAsThread():
            global syncResutl
            loop = asyncio.new_event_loop()
            syncResutl = loop.run_until_complete(self.getSymbols(symbol, features=features, 
                                                                 marketFeatures=marketFeatures, 
                                                                 timeframe=timeframe,
                                                                 onlyFinal=onlyFinal, 
                                                                 ranges=ranges, 
                                                                 dateFrom=dateFrom, 
                                                                 dateTo=dateTo))

        thread1 = threading.Thread(target = runAsThread)
        thread1.start()
        thread1.join()
        return syncResutl
    
    

    async def getAggtrades(self, symbol, features=[], marketFeatures=[], timeframe="1h", onlyFinal=True, ranges="15", dateFrom=None, dateTo=None):
        """Get the aggtrades for a specific symbol and timeframe
        name : The name of your symbol
        return : This is return
        """
        t = await sendDataMessageWithResponse({
            "cmd": "getAggtrades",
            "symbol": symbol,
            "finals": onlyFinal,
            "features": features,
            "marketFeatures" : marketFeatures,
            "timeframe": timeframe,
            "ranges":ranges,
            "dateFrom": dateFrom,
            "dateTo": dateTo
        })      
        
        jsn = json.loads(t)    
        
        if (len(jsn) > 0):
            d = pd.DataFrame.from_dict(jsn)
            d['date'] = pd.to_datetime(d['date'])
            d = d.set_index("date")

            return d
        
        return None
    
    
    async def getSymbols(self, symbol, features=[], marketFeatures=[], timeframe="1h", onlyFinal=True, ranges="15", dateFrom=None, dateTo=None):
        """Get the symbols for a specific symbol and timeframe
        name : The name of your symbol
        return : This is return
        """
        t = await sendDataMessageWithResponse({
            "cmd": "getSymbols",
            "symbol": symbol,
            "finals": onlyFinal,
            "features": features,
            "marketFeatures" : marketFeatures,
            "timeframe": timeframe,
            "ranges":ranges,
            "dateFrom": dateFrom,
            "dateTo": dateTo
        })      
        
        jsn = json.loads(t)    
        
        if (len(jsn) > 0):
            d = pd.DataFrame.from_dict(jsn)
            d['date'] = pd.to_datetime(d['date'])
            d = d.set_index("date")

            return d
        
        return None
    
    
    async def getMarketFeatures(self, name, timeframe="1h", onlyFinal=True,  ranges="60", dateFrom=None, dateTo=None):
        """Get the market features
        name : The name of your feature
        return : This is return
        """
        
        t = await sendDataMessageWithResponse({
            "cmd": "getMarketFeatures",
            "name": name,
            "finals": onlyFinal,
            "timeframe": timeframe,
            "ranges":ranges,
            "dateFrom": dateFrom,
            "dateTo": dateTo
        })
        
        jsn = json.loads(t)    
        
        if (len(jsn) > 0):
            d = pd.DataFrame.from_dict(jsn)
            d['date'] = pd.to_datetime(d['date'])
            d = d.set_index("date")

            return d
        

        return None
       
    
    
    async def getSymbolFeatures(self, symbol, name, onlyFinal=True,  timeframe="1h", ranges="60", dateFrom=None, dateTo=None):

        t = await sendDataMessageWithResponse({
            "cmd": "getSymbolFeatures",
            "name": name,
            "symbol": symbol,
            "finals": onlyFinal,
            "timeframe": timeframe,
            "ranges":ranges,
            "dateFrom": dateFrom,
            "dateTo": dateTo
        })
        
        jsn = json.loads(t)    
        
        if (len(jsn) > 0):
            d = pd.DataFrame.from_dict(jsn)
            d['date'] = pd.to_datetime(d['date'])
            d = d.set_index("date")

            return d

        return None
    
    
    def registerHistoricalSymbolData(self, feature, cb, limit, interval, subfeature=None, symbols=None, title=None):
        
        global historicalMethodsCallback
        
        proc_name = "historicalSymbolFeature_" + feature 
        if (subfeature != None):
            proc_name = proc_name + "_"
        
        send_data = {
            "cmd": "registerHistoricalSymbolData",
            "feature": feature,
            "subfeature": subfeature,
            "title": title,
            "kernel_id": get_current_kernel(),
            "symbols": symbols,
            "limit": limit,
            "interval": interval,
            "proc_name": proc_name,
            "environment": getEnvironment(),
            "mode": "symbol", 
            "process": cb
        }
       
        # before we send the data, we need to add the "callback"
        # to a global handler list
        historicalMethodsCallback[proc_name] = copy.copy(send_data)

        send_data["process"] = None

        sendDataMessage(send_data)
        
        return True
        
    
features = Features()
