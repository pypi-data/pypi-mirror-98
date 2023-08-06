# -*- coding: utf-8 -*-

from pip_services3_expressions.io.IPushbackReader import IPushbackReader
from pip_services3_expressions.tokenizers.ITokenizer import ITokenizer
from pip_services3_expressions.tokenizers.Token import Token
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.generic.CppCommentState import CppCommentState
from pip_services3_expressions.tokenizers.utilities.CharValidator import CharValidator


class CCommentState(CppCommentState):
    """
    This state will either delegate to a comment-handling state, or return a token with just a slash in it.
    """

    def next_token(self, reader, tokenizer):
        """
        Either delegate to a comment-handling state, or return a token with just a slash in it.
        
        :param reader: A textual string to be tokenized.
        :param tokenizer: A tokenizer class that controls the process.
        :return: The next token from the top of the stream.
        """
        first_symbol = reader.read()
        if first_symbol != self.SLASH:
            reader.pushback(first_symbol)
            raise Exception('Incorrect usage of CCommentState.')

        second_symbol = reader.read()
        if second_symbol == self.STAR:
            return Token(TokenType.Comment, '/*' + self.get_multi_line_comment(reader))
        else:
            if not CharValidator.is_eof(second_symbol):
                reader.pushback(second_symbol)

            if not CharValidator.is_eof(first_symbol):
                reader.pushback(first_symbol)

            return tokenizer.symbol_state.next_token(reader, tokenizer)
