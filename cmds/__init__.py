import glob,importlib
from os.path import relpath,join,basename,sep
from os import getcwd

module_files=list()
path=relpath(__path__[0],getcwd())
for file in glob.glob(join(path,"**/*.py"), recursive=True):
    if basename(file).startswith("_"): continue
    if basename(file)=="tools.py": continue#TODO Regrouper les tools
    if basename(file)=="DefaultCmdClass.py": continue#TODO gêrer les filtres
    file=relpath(file,getcwd())
    file=file.replace(sep,".")
    file=file.replace(".py","")
    module_files.append(file)

path=path.replace(sep,".")
modules=list()
for method in module_files:
    modules.append(importlib.import_module(method))