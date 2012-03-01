# -*- coding: UTF-8 -*-
import sys

class PrefixFilter(object):
    def __init__(self, prefix=[], stream=sys.stdout):
        # prefix必須是list物件
        assert isinstance(prefix, list), 'prefix must be a list'
        self.__prefix = prefix
        self.__stream = stream
    def write(self, value):
        # 檢查所有prefix
        for pre in self.__prefix:
            # 如果是黑名單其中一個開頭
            if value.startswith(pre):
                # 就忽略不印
                return
        # 印出來
        print >> self.__stream, value,
