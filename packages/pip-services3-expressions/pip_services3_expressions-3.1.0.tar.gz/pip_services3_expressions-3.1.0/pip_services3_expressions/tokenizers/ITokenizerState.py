# -*- coding: utf-8 -*-

from abc import ABC


class ITokenizerState(ABC):
    """
    A tokenizerState returns a token, given a reader, an initial character read from the reader,
    and a tokenizer that is conducting an overall tokenization of the reader. The tokenizer will
    typically have a character state table that decides which state to use, depending on an initial 
    character. If a single character is insufficient, a state such as **SlashState**
    will read a second character, and may delegate to another state, such as **SlashStarState**.
    This prospect of delegation is the reason that the :func:`next_token()`
    method has a tokenizer argument.
    """

    def next_token(self, reader, tokenizer):
        """
        Gets the next token from the stream started from the character linked to this state.
        
        :param reader: A textual string to be tokenized.
        :param tokenizer: A tokenizer class that controls the process.
        :return: The next token from the top of the stream.
        """
