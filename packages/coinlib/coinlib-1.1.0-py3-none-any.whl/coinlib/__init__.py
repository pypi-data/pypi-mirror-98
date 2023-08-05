from coinlib.helper import in_ipynb, set_loglevel
from coinlib.helper import pip_install_or_ignore
from coinlib.helper import log, debug
import asyncio

pip_install_or_ignore("ipynb_path", "ipynb_path")
# pip_install_or_ignore("import_ipynb", "import_ipynb")
pip_install_or_ignore("websocket", "websocket-client")
pip_install_or_ignore("plotly", "plotly")
pip_install_or_ignore("simplejson", "simplejson")
pip_install_or_ignore("asyncio", "asyncio")
pip_install_or_ignore("grpc", "grpcio-tools")
pip_install_or_ignore("matplotlib", "matplotlib")
pip_install_or_ignore("zlib", "zlib")
pip_install_or_ignore("pandas", "pandas")
pip_install_or_ignore("timeit", "timeit")
pip_install_or_ignore("dateutil", "python-dateutil")
pip_install_or_ignore("chipmunkdb", "chipmunkdb-python-client")

global coinlib_job_task

from coinlib.Registrar import Registrar
from coinlib.logics.Logic import Logic
from coinlib.Functions import Functions
from coinlib.Features import Features
from coinlib.statistics.Statistics import Statistics
from coinlib.Simulator import Simulator
from coinlib.ChartsIndicatorJob import ChartsIndicatorJob

registrar = Registrar()

if registrar.features is None:
    registrar.features = Features()
    registrar.logic = Logic()
    registrar.functions = Functions()
    registrar.statistics = Statistics()
    registrar.simulator = Simulator()


features = registrar.features
logic = registrar.logic
functions = registrar.functions
statistics = registrar.statistics
simulator = registrar.simulator
pip_install_or_ignore = pip_install_or_ignore
set_loglevel = set_loglevel
debug = debug

WORKER_MODE_ALL = "ALL"
WORKER_MODE_LOGIC = "LOGIC"

def registerToWorkspace(workspaceId):
    registrar.workspaceId = workspaceId

def addLogicToWorkspace(identifier, type, logicComponentId, params=None, workspaceId=registrar.workspaceId):
    return logic.addLogicToWorkspace(identifier,
                                     type,
                                     logicComponentId,
                                     params, workspaceId)

def connectAsLogic(hostname=None, workspaceId=None):
    return connect(hostname, workspaceId=workspaceId, worker_mode=WORKER_MODE_LOGIC)

def connect(hostname=None, workspaceId=None, worker_mode=WORKER_MODE_ALL, reconnect=False):
    if registrar.connected and not reconnect:
        return

    if not registrar.hasEnvironment():
        if hostname is not None:
            registrar.setBackendPath(hostname)
        registrar.setEnvironment("dev")
        registrar.worker_mode = worker_mode
        registrar.workspaceId = workspaceId

    registrar.simulator.connect()
    registrar.features.connect()
    registrar.functions.connect()
    registrar.logic.connect()
    registrar.statistics.connect()
    registrar.connected = True

def waitForJobs():

    # register as a worker if not already done


    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    finally:
        loop.close()
