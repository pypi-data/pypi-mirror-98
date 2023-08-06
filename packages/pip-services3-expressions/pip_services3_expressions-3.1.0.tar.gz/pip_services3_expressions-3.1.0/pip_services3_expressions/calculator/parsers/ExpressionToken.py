# -*- coding: utf-8 -*-

class ExpressionToken:
    """
    Defines an expression token holder.
    """

    def __init__(self, type, value=None):
        """
        Creates an instance of this token and initializes it with specified values.
        
        :param type: The type of this token.
        :param value: The value of this token.
        """
        self.__type = type
        self.__value = value

    @property
    def type(self):
        """
        The type of this token.
        """
        return self.__type

    @property
    def value(self):
        return self.__value
