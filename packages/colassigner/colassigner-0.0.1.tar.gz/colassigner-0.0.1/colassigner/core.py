from abc import ABCMeta
from collections.abc import Mapping

dic_methods = ["get", "keys", "items", "values"]


class ColMeta(ABCMeta):
    def __getattribute__(cls, attid):
        if attid.startswith("_") or (attid in dic_methods):
            return super().__getattribute__(attid)
        return attid


class ColAssigner(Mapping, metaclass=ColMeta):
    """define functions that create columns in a dataframe
    
    later the class atributes can be used to access the column"""

    def __init__(self):
        self._callables = {}
        self._add_callables()

    def __getitem__(self, key):
        return self._callables[key]

    def __iter__(self):
        for k in self._callables.keys():
            yield k

    def __len__(self):
        return len(self._callables)

    def _add_callables(self):
        for mid in self.__dir__():
            if mid.startswith("_") or (mid in dic_methods):
                continue
            m = getattr(self, mid)
            if callable(m):
                self._callables[mid] = m
