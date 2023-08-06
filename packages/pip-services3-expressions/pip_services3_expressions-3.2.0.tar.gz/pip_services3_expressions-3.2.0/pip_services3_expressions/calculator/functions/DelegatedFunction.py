# -*- coding: utf-8 -*-

from pip_services3_expressions.calculator.functions.IFunction import IFunction


class DelegatedFunction(IFunction):

    def __init__(self, name, calculator):
        """
        Constructs this function class with specified parameters.

        :param name: The name of this function.
        :param calculator: The function calculator delegate.
        """
        if name is None:
            raise Exception('Name parameter cannot be null')
        if calculator is None:
            raise Exception('Calculator parameter cannot be null')
        self.__name = name
        self.__calculator = calculator

    @property
    def name(self):
        """
        The function name.
        """
        return self.__name

    def calculate(self, params, variant_operations, callback):
        """
        The function calculation method.
        
        :param params: an array with function parameters.
        :param variant_operations: Variants operations manager.
        :param callback: a callback to return function result.
        """
        try:
            self.__calculator(params, variant_operations, callback)
        except Exception as err:
            callback(err, None)


