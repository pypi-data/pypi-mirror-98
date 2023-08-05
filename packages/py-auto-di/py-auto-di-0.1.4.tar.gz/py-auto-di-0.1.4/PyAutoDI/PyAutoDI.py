from glob import glob
import logging
import os
import re

from .Container import Container


def get_module_paths(path_pattern):
    return glob(path_pattern, recursive=True)


def build_module_path(file_path):
    module_path = ".".join(file_path.split(os.path.sep))[0:-3]

    return module_path


def load_modules(file_paths):
    module_paths = filter(
        lambda path: not re.search("__init__", path),
        map(build_module_path, file_paths)
    )

    return list(map(lambda path: __import__(path, fromlist=['']), module_paths))


def register_module(module, container):
    try:
        module.register(container)
    except:
        logging.warning("Module found that is missing a register function")


def load_and_register_modules(path_pattern, container):
    module_paths = get_module_paths(path_pattern)
    modules = load_modules(module_paths)

    for module in modules:
        register_module(module, container)

    return container


def get_new_container():
    return Container()
