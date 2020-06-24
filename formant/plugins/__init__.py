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

class FunctionProxy(object):
    def __init__(self, source):
        self.source = source

    def __getattr__(self, attr):
        return getattr(self.source, attr)

    def __call__(self, *args, **kwargs):
        return self.source(*args, **kwargs)

    def __format__(self, spec=None):
        return format(self.source(), spec)

    def __str__(self):
        return format(self, 's')
    def __repr__(self):
        return format(self, 'r')

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
        got = getattr(self.module, attr)
        if isinstance(got, types.FunctionType):
            return FunctionProxy(got)
        return got

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
