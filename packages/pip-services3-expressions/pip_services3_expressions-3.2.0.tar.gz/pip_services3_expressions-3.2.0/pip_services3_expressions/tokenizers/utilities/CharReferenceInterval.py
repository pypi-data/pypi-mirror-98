# -*- coding: utf-8 -*-

class CharReferenceInterval:
    """
    Represents a character interval that keeps a reference.
    This class is internal and used by [[CharReferenceMap]].
    """

    def __init__(self, start, end, reference):
        if start > end:
            raise Exception('Start must be less or equal End')
        self.__start = start
        self.__end = end
        self.__reference = reference

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def reference(self):
        return self.__reference

    def in_range(self, symbol):
        return self.__start <= symbol <= self.__end
