# -*- coding: utf-8 -*-

from pip_services3_expressions.tokenizers.Token import Token
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.generic.GenericNumberState import GenericNumberState
from pip_services3_expressions.tokenizers.utilities.CharValidator import CharValidator


class ExpressionNumberState(GenericNumberState):
    """
    Implements an Expression-specific number state object.
    """

    def __init__(self):
        super(ExpressionNumberState, self).__init__()
        self.PLUS = ord('+')
        self.EXP1 = ord('e')
        self.EXP2 = ord('E')

    def next_token(self, reader, tokenizer):
        """
        Gets the next token from the stream started from the character linked to this state.
        
        :param reader: A textual string to be tokenized.
        :param tokenizer: A tokenizer class that controls the process.
        :return: The next token from the top of the stream.
        """
        if reader.peek() == self.MINUS:
            return tokenizer.symbol_state.next_token(reader, tokenizer)

        # Process numbers using base class algorithm.
        token = super().next_token(reader, tokenizer)

        # Exit if number was not detected.
        if token.type != TokenType.Integer and token.type != TokenType.Float:
            return token

        # Exit if number is not in scientific format.
        next_char = reader.peek()
        if next_char != self.EXP1 and next_char != self.EXP2:
            return token

        token_value = ''
        token_value = token_value + chr(reader.read())

        # Process '-' or '+' in mantissa
        next_char = reader.peek()
        if next_char == self.MINUS or next_char == self.PLUS:
            token_value += chr(reader.read())
            next_char = reader.peek()

        # Exit if mantissa has no digits.
        if not CharValidator.is_digit(next_char):
            reader.pushback_string(token_value)
            return token

        # Process matissa digits
        while CharValidator.is_digit(next_char):
            token_value += chr(reader.read())
            next_char = reader.peek()

        return Token(TokenType.Float, token.value + token_value)
