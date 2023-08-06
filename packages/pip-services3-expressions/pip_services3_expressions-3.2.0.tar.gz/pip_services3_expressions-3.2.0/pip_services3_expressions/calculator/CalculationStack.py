# -*- coding: utf-8 -*-

class CalculationStack:
    """
    Implements a stack of Variant values.
    """

    def __init__(self):
        self.__values = []

    @property
    def length(self):
        return len(self.__values)

    def push(self, value):
        self.__values.append(value)

    def pop(self):
        if len(self.__values) == 0:
            raise Exception('Stack is empty.')
        return self.__values.pop()

    def peek_at(self, index):
        return self.__values[index]

    def peek(self):
        if len(self.__values) == 0:
            raise Exception('Stack is empty.')
        return self.__values[-1]
