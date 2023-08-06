# -*- coding: utf-8 -*-

from pip_services3_expressions.tokenizers.INumberState import INumberState
from pip_services3_expressions.tokenizers.Token import Token
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.utilities.CharValidator import CharValidator


class GenericNumberState(INumberState):
    """
    A NumberState object returns a number from a reader. This state's idea of a number allows
    an optional, initial minus sign, followed by one or more digits. A decimal point and another string
    of digits may follow these digits.
    """

    def __init__(self):
        super(GenericNumberState, self).__init__()
        self.MINUS = ord('-')
        self.DOT = ord('.')

    def next_token(self, reader, tokenizer):
        """
        Gets the next token from the stream started from the character linked to this state.
        
        :param reader: A textual string to be tokenized.
        :param tokenizer: A tokenizer class that controls the process.
        :return: The next token from the top of the stream.
        """
        absorbed_dot = False
        got_a_digit = False
        token_value = ""
        next_symbol = reader.read()

        # Parses leading minus.
        if next_symbol == self.MINUS:
            token_value = token_value + '-'
            next_symbol = reader.read()

        # Parses digits before decimal separator.
        while CharValidator.is_digit(next_symbol) and not CharValidator.is_eof(next_symbol):
            got_a_digit = True
            token_value = token_value + chr(next_symbol)
            next_symbol = reader.read()

        # Parses part after the decimal separator.
        if next_symbol == self.DOT:
            absorbed_dot = True
            token_value += '.'
            next_symbol = reader.read()

            # Absorb all digits.
            while CharValidator.is_digit(next_symbol) and not CharValidator.is_eof(next_symbol):
                got_a_digit = True
                token_value = token_value + chr(next_symbol)
                next_symbol = reader.read()

        # Pushback last unprocessed symbol.
        if not CharValidator.is_eof(next_symbol):
            reader.pushback(next_symbol)

        # Process the result.
        if not got_a_digit:
            reader.pushback_string(token_value)
            if tokenizer.symbol_state is not None:
                return tokenizer.symbol_state.next_token(reader, tokenizer)
            else:
                raise Exception('Tokenizer must have an assigned symbol state.')

        return Token(TokenType.Float if absorbed_dot else TokenType.Integer, token_value)
