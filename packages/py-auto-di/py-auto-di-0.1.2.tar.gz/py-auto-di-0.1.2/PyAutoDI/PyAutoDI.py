from glob import glob
import logging
import os
from runpy import run_path

from .Container import Container

def get_module_paths(path_pattern):
    return glob(path_pattern, recursive=True)

def build_module_file_path(module_path):
    return os.path.realpath(os.path.join(os.getcwd(), module_path))

def load_modules(module_paths):
    import_file = lambda module_path: run_path(build_module_file_path(module_path))
    return map(import_file, module_paths)

def register_module(module, container):
    if("register" in module):
        module["register"](container)
    else:
        logging.warning("Module found that is missing a register function")

def load_and_register_modules(path_pattern, container):
    module_paths = get_module_paths(path_pattern)
    modules = load_modules(module_paths)
    
    for module in modules:
        register_module(module, container)
    
    return container

def get_new_container():
    return Container()
