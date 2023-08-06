# -*- coding: utf-8 -*-

from pip_services3_expressions.io.IPushbackReader import IPushbackReader
from pip_services3_expressions.tokenizers.Token import Token
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.generic.SymbolNode import SymbolNode


class SymbolRootNode(SymbolNode):
    """
    This class is a special case of a **SymbolNode**. A **SymbolRootNode**
    object has no symbol of its own, but has children that represent all possible symbols.
    """

    def __init__(self):
        """
        Creates and initializes a root node.
        """
        super(SymbolRootNode, self).__init__(None, 0)

    def add(self, value, token_type):
        if value == '':
            raise Exception('Value must have at least 1 character')

        child_node = self.ensure_child_with_char(ord(value[0]))
        if child_node.token_type == TokenType.Unknown:
            child_node.valid = True
            child_node.token_type = TokenType.Symbol
        child_node.add_descendant_line(value[1:], token_type)

    def next_token(self, reader):
        """
        Return a symbol string from a reader.
        
        :param reader: A reader to read from
        :return: A symbol string from a reader
        """
        next_symbol = reader.read()
        child_node = self.find_child_with_char(next_symbol)
        if child_node is not None:
            child_node = child_node.deepest_read(reader)
            child_node = child_node.unread_to_valid(reader)
            return Token(child_node.token_type, child_node.ancestry())
        else:
            return Token(TokenType.Symbol, chr(next_symbol))
