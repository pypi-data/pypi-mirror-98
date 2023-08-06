# -*- coding: utf-8 -*-

from .TokenType import TokenType


class Token:
    """
    A token represents a logical chunk of a string. For example, a typical tokenizer would break
    the string "1.23 &lt;= 12.3" into three tokens: the number 1.23, a less-than-or-equal symbol,
    and the number 12.3. A token is a receptacle, and relies on a tokenizer to decide precisely how
    to divide a string into tokens.
    """

    def __init__(self, type, value):
        """
        Constructs this token with type and value.

        :param type: The type of this token.
        :param value: The token string value.
        """
        self.__type = type
        self.__value = value

    @property
    def type(self):
        """
        The token type.
        """
        return self.__type

    @property
    def value(self):
        """
        The token value.
        """
        return self.__value

    def equals(self, obj):
        if isinstance(obj, Token):
            token = obj
            return token.__type == self.__type and token.__value == self.__value
