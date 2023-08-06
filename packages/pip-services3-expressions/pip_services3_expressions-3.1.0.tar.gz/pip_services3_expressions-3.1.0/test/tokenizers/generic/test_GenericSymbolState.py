# -*- coding: utf-8 -*-

from pip_services3_expressions.io.StringPushbackReader import StringPushbackReader
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.generic.GenericSymbolState import GenericSymbolState

class TestGenericSymbolState:

    def test_next_token(self):
        state = GenericSymbolState()
        state.add("<", TokenType.Symbol)
        state.add("<<", TokenType.Symbol)
        state.add("<>", TokenType.Symbol)

        reader = StringPushbackReader("<A<<<>")

        token = state.next_token(reader, None)
        assert "<" == token.value
        assert TokenType.Symbol == token.type

        token = state.next_token(reader, None)
        assert "A" == token.value
        assert TokenType.Symbol == token.type

        token = state.next_token(reader, None)
        assert "<<" == token.value
        assert TokenType.Symbol == token.type

        token = state.next_token(reader, None)
        assert "<>" == token.value
        assert TokenType.Symbol == token.type

