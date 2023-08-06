# -*- coding: utf-8 -*-

from pip_services3_expressions.io.StringPushbackReader import StringPushbackReader
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.generic.GenericCommentState import GenericCommentState


class TestGenericCommentState:

    def test_next_token(self):
        state = GenericCommentState()

        reader = StringPushbackReader("# Comment \r# Comment ")
        token = state.next_token(reader, None)
        assert "# Comment " == token.value
        assert TokenType.Comment == token.type

        reader = StringPushbackReader("# Comment \n# Comment ")
        token = state.next_token(reader, None)
        assert "# Comment " == token.value
        assert TokenType.Comment == token.type
