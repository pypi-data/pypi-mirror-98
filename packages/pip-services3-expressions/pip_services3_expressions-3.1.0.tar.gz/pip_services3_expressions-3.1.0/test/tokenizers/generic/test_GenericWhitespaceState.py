# -*- coding: utf-8 -*-

from pip_services3_expressions.io.StringPushbackReader import StringPushbackReader
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.generic.GenericWhitespaceState import GenericWhitespaceState


class GenericWhitespaceState:

    def test_next_token(self):
        state = GenericWhitespaceState()

        reader = StringPushbackReader(" \t\n\r #")
        token = state.next_token(reader, None)
        assert " \t\n\r " == token.value
        assert TokenType.Whitespace == token.type
