# -*- coding: utf-8 -*-

from pip_services3_expressions.io.StringPushbackReader import StringPushbackReader
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.generic.GenericWordState import GenericWordState


class TestGenericWordState:

    def test_next_token(self):
        state = GenericWordState()

        reader = StringPushbackReader("AB_CD=")
        token = state.next_token(reader, None)
        assert "AB_CD" == token.value
        assert TokenType.Word == token.type
