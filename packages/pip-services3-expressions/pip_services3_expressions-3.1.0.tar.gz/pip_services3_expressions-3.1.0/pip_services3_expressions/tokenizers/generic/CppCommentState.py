# -*- coding: utf-8 -*-

from pip_services3_expressions.io.IPushbackReader import IPushbackReader
from pip_services3_expressions.tokenizers.ITokenizer import ITokenizer
from pip_services3_expressions.tokenizers.Token import Token
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.generic.GenericCommentState import GenericCommentState
from pip_services3_expressions.tokenizers.utilities.CharValidator import CharValidator


class CppCommentState(GenericCommentState):
    """
    This state will either delegate to a comment-handling state, or return a token with just a slash in it.
    """

    def __init__(self):
        super(CppCommentState, self).__init__()
        self.STAR = ord('*')
        self.SLASH = ord('/')

    def get_multi_line_comment(self, reader):
        result = ''
        last_symbol = 0
        next_symbol = reader.read()

        while not CharValidator.is_eof(next_symbol):
            result += chr(next_symbol)
            if last_symbol == self.STAR and next_symbol == self.SLASH:
                break
            last_symbol = next_symbol
            next_symbol = reader.read()
        return result

    def get_single_line_comment(self, reader):
        """
        Ignore everything up to an end-of-line and return the tokenizer's next token.
        """
        result = ''
        next_symbol = reader.read()

        while not CharValidator.is_eof(next_symbol) and not CharValidator.is_eol(next_symbol):
            result = result + chr(next_symbol)
            next_symbol = reader.read()

        if CharValidator.is_eol(next_symbol):
            reader.pushback(next_symbol)

        return result

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
            raise Exception('Incorrect usage of CppCommentState.')

        second_symbol = reader.read()
        if second_symbol == self.STAR:
            return Token(TokenType.Comment, '/*' + self.get_multi_line_comment(reader))
        elif second_symbol == self.SLASH:
            return Token(TokenType.Comment, '//' + self.get_single_line_comment(reader))
        else:
            if not CharValidator.is_eof(second_symbol):
                reader.pushback(second_symbol)
            if not CharValidator.is_eof(first_symbol):
                reader.pushback(first_symbol)
            return tokenizer.symbol_state.next_token(reader, tokenizer)
