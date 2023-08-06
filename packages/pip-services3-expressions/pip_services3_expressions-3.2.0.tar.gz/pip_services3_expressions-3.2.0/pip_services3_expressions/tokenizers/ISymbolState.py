# -*- coding: utf-8 -*-

from abc import ABC

from .ITokenizerState import ITokenizerState


class ISymbolState(ITokenizerState, ABC):
    """
    Defines an interface for tokenizer state that processes delimiters.
    """

    def add(self, value, token_type):
        """
        Add a multi-character symbol.
        
        :param value: The symbol to add, such as "=:="
        :param token_type: The token type
        """
