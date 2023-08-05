from coinlib.helper import log, get_coinlib_backend

class Registrar(object):
    _instance = None
    functionsCallbacks = {}
    statisticsCallbacks = {}
    logicCallbacks = {}
    chartsFactory = None
    statsRuleFactory = None
    logicFactory = None
    workspaceId = None
    environment = None
    statsMethodFactory = None
    worker_mode = None
    connected = False
    isRegistered = False
    iframe_host = get_coinlib_backend()+":3000"
    coinlib_backend = get_coinlib_backend()+":3994"
    chipmunkdb = get_coinlib_backend()

    simulator = None
    statistics = None
    logic = None
    functions = None
    features = None


    def __new__(cls):
        if cls._instance is None:
            log.info('Creating the object')
            cls._instance = super(Registrar, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def hasEnvironment(self):
        return self.environment is not None

    def setEnvironment(self, env):
        if self.environment is None:
            self.environment = env
        else:
            log.error("You are trying to change the environment - thats probably an error?")

    def isLiveEnvironment(self):
        return self.environment == "live"
    
    def setBackendPath(self, path):
        self.iframe_host = path + ":3000"
        self.coinlib_backend = path + ":3994"
        self.chipmunkdb = path