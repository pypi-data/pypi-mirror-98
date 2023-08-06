# -*- coding: utf-8 -*-

from abc import ABC

from pip_services3_expressions.variants.Variant import Variant


class IVariable(ABC):
    """
    Defines a variable interface.
    """

    # The variable name.
    name: str

    # The variable value.
    value: Variant

