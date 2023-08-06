# -*- coding: utf-8 -*-

from pip_services3_expressions.io.StringPushbackReader import StringPushbackReader
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.generic.CppCommentState import CppCommentState


class TestCppCommentState:

    def test_next_token(self):
        state = CppCommentState()

        reader = StringPushbackReader("-- Comment \n Comment ")
        failed = False

        try:
            state.next_token(reader, None)
        except Exception as e:
            failed = True
        assert failed is True

        reader = StringPushbackReader("// Comment \n Comment ")
        token = state.next_token(reader, None)
        assert "// Comment " == token.value
        assert TokenType.Comment == token.type
