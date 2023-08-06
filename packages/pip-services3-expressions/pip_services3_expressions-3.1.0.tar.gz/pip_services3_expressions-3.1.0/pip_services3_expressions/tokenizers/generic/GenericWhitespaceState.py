# -*- coding: utf-8 -*-


from pip_services3_expressions.tokenizers.IWhitespaceState import IWhitespaceState
from pip_services3_expressions.tokenizers.Token import Token
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.utilities.CharReferenceMap import CharReferenceMap
from pip_services3_expressions.tokenizers.utilities.CharValidator import CharValidator


class GenericWhitespaceState(IWhitespaceState):
    """
    A whitespace state ignores whitespace (such as blanks and tabs), and returns the tokenizer's
    next token. By default, all characters from 0 to 32 are whitespace.
    """

    def __init__(self):
        self.__map = CharReferenceMap()
        self.set_whitespace_chars(0, ord(' '), True)

    def next_token(self, reader, tokenizer):
        """
        Ignore whitespace (such as blanks and tabs), and return the tokenizer's next token.

        :param reader: A textual string to be tokenized.
        :param tokenizer: A tokenizer class that controls the process.
        :return: The next token from the top of the stream.
        """
        token_value = ""
        next_symbol = reader.read()
        while self.__map.lookup(next_symbol):
            token_value = token_value + chr(next_symbol)
            next_symbol = reader.read()

        if not CharValidator.is_eof(next_symbol):
            reader.pushback(next_symbol)

        return Token(TokenType.Whitespace, token_value)

    def set_whitespace_chars(self, from_symbol, to_symbol, enable):
        """
        Establish the given characters as whitespace to ignore.
        
        :param from_symbol: First character index of the interval.
        :param to_symbol: Last character index of the interval.
        :param enable: **True** if this state should ignore characters in the given range.
        """
        self.__map.add_interval(from_symbol, to_symbol, enable)

    def clear_whitespace_chars(self):
        """
        Clears definitions of whitespace characters.
        """
        self.__map.clear()
