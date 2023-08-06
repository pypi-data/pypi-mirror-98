# -*- coding: utf-8 -*-

from pip_services3_expressions.calculator.variables.IVariable import IVariable
from pip_services3_expressions.variants.Variant import Variant


class Variable(IVariable):
    """
    Implements a variable holder object.
    """

    def __init__(self, name, value=None):
        """
        Constructs this variable with name and value.
        
        :param name: The name of this variable.
        :param value: The variable value.
        """
        if name is None:
            raise Exception("Name parameter cannot be null.")
        self.__name = name
        self.__value = value or Variant()

    @property
    def name(self):
        """
        The variable name.
        """
        return self.__name

    @property
    def value(self):
        """
        The variable value.
        """
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
