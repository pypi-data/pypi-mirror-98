# -*- coding: utf-8 -*-

from abc import ABC


class IFunction(ABC):
    """
    Defines an interface for expression function.
    """

    # The function name.
    name: str

    def calculate(self, params, variant_operations, callback):
        """
        The function calculation method.

        :param params: The stack to get function parameters and place
        :param variant_operations: Variants operations manager.
        """
