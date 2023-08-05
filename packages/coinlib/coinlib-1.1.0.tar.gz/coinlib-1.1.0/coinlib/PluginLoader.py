import os
import importlib
import pkgutil
import sys
import importlib
from pathlib import Path
from coinlib.helper import log
from coinlib import Registrar

class PluginLoader:

    def __init__(self, parentdirectory=""):
        self.parentDirectory = parentdirectory
        self.loadPlugins()
        return None


    def loadPlugins(self):
        dirname = self.parentDirectory + self.getLoaderPath()
        log.info("Loading plugins from "+ str(dirname))
        ##for importer, package_name, _ in pkgutil.iter_modules([dirname]):

        for loader, package_name, is_pkg in pkgutil.walk_packages([dirname]):
            replaced_dirname = dirname.replace("/", ".")
            full_package_name = '%s.%s' % (replaced_dirname, package_name)
            if package_name not in sys.modules:
                log.info("Package is not in sys.modules "+package_name)
                log.info(dirname)
                self.loadPlugin(dirname+"/"+package_name)

        pass

    def reloadPlugins(self):

        dirname = self.getLoaderPath()
        for importer, package_name, _ in pkgutil.iter_modules([dirname]):
            full_package_name = '%s.%s' % (dirname, package_name)
            log.info(full_package_name)
            self.reloadPlugin(dirname+"/"+package_name)

        return True

    def reloadPlugin(self, path):
        ret = False
        try:
            try:
                del sys.modules[path]
            except:
                pass

            # ret = __import__('%s' % path, globals=globals())
            base = os.path.basename(path)
            dirname = path.split("/")[0]
            path_comp = Path(path)
            moduleName = os.path.splitext(base)[0]
            sys.path.insert(0, dirname)
            ret = __import__('%s' % moduleName, globals=globals())
            log.info("Reimported plugin: "+moduleName)
        except Exception as e:
            log.warning("ERror loading", str(e))
            pass
        return ret
        ##mod = importlib.import_module('%s' % path)
        ##return mod

    def loadPlugin(self, path):
        ret = None
        try:
            #ret = __import__('%s' % path, globals=globals())

            base = os.path.basename(path)
            dirname = path.split("/")[0]
            path_comp = Path(path)
            moduleName = os.path.splitext(base)[0]
            sys.path.insert(0, dirname)
            ret = __import__('%s' % moduleName, globals=globals())
            log.info("Imported plugin: "+moduleName)

            #with open(path+".py", 'rb') as fp:
            #    globals()[moduleName] = importlib.import_module(moduleName, fp)
        except Exception as e:
            log.warning("Error loading", e)
            pass
        return ret
        ##mod = importlib.import_module('%s' % path)
        ##return mod






