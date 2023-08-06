# -*- coding: utf-8 -*-
from pip_services3_expressions.mustache.parsers.MustacheTokenType import MustacheTokenType


class MustacheToken:
    """
    Defines a mustache token holder.
    """

    def __init__(self, type: MustacheTokenType, value: str):
        """
        Creates an instance of a mustache token.

        :param type: a token type.
        :param value: a token value.
        """
        self.__type = type
        self.__value = value
        self.__tokens = []

    @property
    def type(self):
        """
        Gets the token value or variable name.
        """
        return self.__type

    @property
    def value(self):
        """
        Gets the token value or variable name.
        """
        return self.__value

    @property
    def tokens(self):
        """
        Gets a list of subtokens is this token a section.
        """
        return self.__tokens
