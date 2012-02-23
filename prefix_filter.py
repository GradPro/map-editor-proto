import sys

class PrefixFilter(object):
    def __init__(self, prefix=[], stream=sys.stdout):
        assert isinstance(prefix, list), 'prefix must be a list'
        self.__prefix = prefix
        self.__stream = stream
    def write(self, value):
        for pre in self.__prefix:
            if value.startswith(pre):
                return
        print >> self.__stream, value,
