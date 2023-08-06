# -*- coding: utf-8 -*-

from pip_services3_expressions.io.StringPushbackReader import StringPushbackReader
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.generic.GenericNumberState import GenericNumberState


class TestGenericNumberState:

    def test_next_token(self):
        state = GenericNumberState()

        reader = StringPushbackReader("ABC")
        failed = False
        try:
            state.next_token(reader, None)
        except Exception as e:
            failed = True
        assert failed is True

        reader = StringPushbackReader("123#")
        token = state.next_token(reader, None)
        assert '123' == token.value
        assert TokenType.Integer == token.type

        reader = StringPushbackReader("-123#")
        token = state.next_token(reader, None)
        assert '-123' == token.value
        assert TokenType.Integer == token.type

        reader = StringPushbackReader("123.#")
        token = state.next_token(reader, None)
        assert '123.' == token.value
        assert TokenType.Float == token.type

        reader = StringPushbackReader("123.456#")
        token = state.next_token(reader, None)
        assert '123.456' == token.value
        assert TokenType.Float == token.type

        reader = StringPushbackReader("-123.456#")
        token = state.next_token(reader, None)
        assert '-123.456' == token.value
        assert TokenType.Float == token.type
