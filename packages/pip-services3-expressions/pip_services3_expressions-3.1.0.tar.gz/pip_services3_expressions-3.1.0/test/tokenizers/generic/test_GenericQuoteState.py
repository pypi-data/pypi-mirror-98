# -*- coding: utf-8 -*-

from pip_services3_expressions.io.StringPushbackReader import StringPushbackReader
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.generic.GenericQuoteState import GenericQuoteState

class TestGenericQuoteState:

    def test_next_token(self):
        state = GenericQuoteState()\

        reader = StringPushbackReader("'ABC#DEF'#")
        token = state.next_token(reader, None)
        assert "'ABC#DEF'" == token.value
        assert TokenType.Quoted == token.type

        reader = StringPushbackReader("'ABC#DEF''")
        token = state.next_token(reader, None)
        assert "'ABC#DEF'" == token.value
        assert TokenType.Quoted == token.type

    def test_encode_and_decode_string(self):
        state = GenericQuoteState()

        value = state.encode_string("ABC", ord("'"))
        assert "'ABC'" == value

        value = state.decode_string(value, ord("'"))
        assert "ABC" == value

        value = state.decode_string("'ABC'DEF'", ord("'"))
        assert "ABC'DEF" == value

