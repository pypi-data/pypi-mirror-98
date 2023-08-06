# -*- coding: utf-8 -*-

from abc import ABC

class IPushbackReader(ABC):
    """
    Defines reader with ability to push back characters.
    This reader is used by tokenizers to process input streams.
    """
    def read(self):
        """
        Reads character from the top of the stream.

        :return: A read character or **-1** if stream processed to the end.
        """

    def peek(self):
        """
        Returns the character from the top of the stream without moving the stream pointer.

        :return: A character from the top of the stream or **-1** if stream is empty.
        """

    def pushback(self, value):
        """
        Puts the specified character to the top of the stream.

        :param value: A character to be pushed back.
        """

    def pushback_string(self, value):
        """
        Pushes the specified string to the top of the stream.
        
        :param value: A string to be pushed back.
        """