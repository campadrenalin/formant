import os
import importlib
import pkgutil
import types

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def find_packages(root='formant.plugins'):
    rootpkg = importlib.import_module(root)
    prefix  = rootpkg.__name__ + '.'
    for finder, name, ispkg in pkgutil.iter_modules(rootpkg.__path__, prefix):
        access_name = remove_prefix(name, prefix)
        yield access_name, name

class Plugin(object):
    def __init__(self, name):
        self.name = name
        self._mod = None

    @property
    def module(self):
        if self._mod is None:
            self._mod = importlib.import_module(self.name)
        return self._mod

    def __getattr__(self, attr):
        return getattr(self.module, attr)

class Registry(object):
    def __init__(self, *roots, include_std=True):
        if include_std:
            roots = set([*roots, 'formant.plugins'])

        self.__plugins = {}
        for root in roots:
            if not root:
                continue
            for access_name, name in find_packages(root):
                self.__plugins[access_name] = Plugin(name)

    def __getattr__(self, attr):
        return self.__plugins[attr]
    def __getitem__(self, item):
        return self.__plugins[item]

    def __iter__(self):
        return iter(self.__plugins)

default_roots = os.environ.get('FORMANT_PLUGIN_PKGS', '').split(',')
registry = Registry(*default_roots)
