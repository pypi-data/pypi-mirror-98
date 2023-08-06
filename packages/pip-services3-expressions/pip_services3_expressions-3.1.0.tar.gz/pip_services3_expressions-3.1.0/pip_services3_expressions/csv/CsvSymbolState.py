# -*- coding: utf-8 -*-

from pip_services3_expressions.csv.CsvConstant import CsvConstant
from pip_services3_expressions.tokenizers.Token import Token
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.generic.GenericSymbolState import GenericSymbolState


class CsvSymbolState(GenericSymbolState):
    """
    Implements a symbol state to tokenize delimiters in CSV streams.
    """

    def __init__(self):
        super(CsvSymbolState, self).__init__()
        self.add("\n", TokenType.Eol)
        self.add("\r", TokenType.Eol)
        self.add("\r\n", TokenType.Eol)
        self.add("\n\r", TokenType.Eol)

    def next_token(self, reader, tokenizer):
        # Optimization...
        next_symbol = reader.read()
        if next_symbol != CsvConstant.LF and next_symbol != CsvConstant.CR:
            return Token(TokenType.Symbol, chr(next_symbol))
        else:
            reader.pushback(next_symbol)
            return super().next_token(reader, tokenizer)
