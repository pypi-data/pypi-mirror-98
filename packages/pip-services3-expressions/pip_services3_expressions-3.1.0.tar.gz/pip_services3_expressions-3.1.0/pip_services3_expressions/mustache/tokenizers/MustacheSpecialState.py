# -*- coding: utf-8 -*-
from pip_services3_expressions.io.IPushbackReader import IPushbackReader
from pip_services3_expressions.tokenizers.ITokenizer import ITokenizer
from pip_services3_expressions.tokenizers.ITokenizerState import ITokenizerState
from pip_services3_expressions.tokenizers.Token import Token
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.utilities.CharValidator import CharValidator


class MustacheSpecialState(ITokenizerState):
    """
    Implements a quote string state object for Mustache templates.
    """

    _Bracket = ord("{")

    def next_token(self, reader: IPushbackReader, tokenizer: ITokenizer):
        """
        Gets the next token from the stream started from the character linked to this state.

        :param reader: A textual string to be tokenized.
        :param tokenizer: A tokenizer class that controls the process.
        :return: The next token from the top of the stream.
        """
        token_value = ""

        next_symbol = reader.read()
        while not CharValidator.is_eof(next_symbol):
            if next_symbol == MustacheSpecialState._Bracket:
                if reader.peek() == MustacheSpecialState._Bracket:
                    reader.pushback(next_symbol)
                    break
            token_value = token_value + chr(next_symbol)

            next_symbol = reader.read()

        return Token(TokenType.Special, token_value)


