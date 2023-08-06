# -*- coding: utf-8 -*-

from pip_services3_expressions.tokenizers.ICommentState import ICommentState
from pip_services3_expressions.tokenizers.Token import Token
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.utilities.CharValidator import CharValidator


class GenericCommentState(ICommentState):
    """
    A CommentState object returns a comment from a reader.
    """

    def __init__(self):
        super(GenericCommentState, self).__init__()
        self.LF = ord('\r')
        self.CR = ord('\n')

    def next_token(self, reader, tokenizer):
        """
        Either delegate to a comment-handling state, or return a token with just a slash in it.
        
        :param reader: A textual string to be tokenized.
        :param tokenizer: A tokenizer class that controls the process.
        :return: The next token from the top of the stream.
        """
        token_value = ''
        next_symbol = reader.read()
        while not CharValidator.is_eof(next_symbol) and next_symbol != self.CR and next_symbol != self.LF:
            token_value = token_value + chr(next_symbol)
            next_symbol = reader.read()
        if not CharValidator.is_eof(next_symbol):
            reader.pushback(next_symbol)

        return Token(TokenType.Comment, token_value)
