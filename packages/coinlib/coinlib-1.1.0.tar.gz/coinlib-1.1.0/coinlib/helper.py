import os
import sys
from IPython.lib import kernel
from IPython import get_ipython
import importlib
import subprocess
import logging


log = logging
currentfile = sys.argv[0]
                       
def get_current_kernel():
    if (is_in_ipynb == False):
        return currentfile
        
    connection_file_path = kernel.get_connection_file()
    connection_file = os.path.basename(connection_file_path)
    kernel_id = connection_file.split('-', 1)[1].split('.')[0]
    return kernel_id

def in_ipynb():
    try:
        cfg = get_ipython().config 
        
        if ("jupyter" in cfg['IPKernelApp']['connection_file']):
            return True
        elif ("Jupyter" in cfg['IPKernelApp']['connection_file']):
            return True
        else:
            return False
    except Exception:
        return False
    
is_in_ipynb = in_ipynb()
if is_in_ipynb:
    log.basicConfig(level=logging.ERROR)

def debug(debug=True):
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    if debug:
        log.basicConfig(level=logging.INFO)
    else:
        log.basicConfig(level=logging.ERROR)
    return None

def set_loglevel(level):
    log.basicConfig(level=level)

if not 'workbookDir' in globals():
    workbookDir = os.getcwd()

def pip_install_or_ignore(import_name, module_name):
    try:
        return importlib.import_module(import_name)
    except ImportError:
        print("missing importing of "+import_name)
        if in_ipynb():
            get_ipython().run_line_magic('pip', 'install $module_name')
        else:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
# Function to display hostname and 
# IP address 
def get_coinlib_backend(): 
    try: 
        return os.environ["COINLIB_WB"]
    except: 
        pass
    return "localhost"

if in_ipynb():
    hostname = get_coinlib_backend()
else:
    hostname = get_coinlib_backend()
