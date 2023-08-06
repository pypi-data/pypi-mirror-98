# -*- coding: utf-8 -*-

from .IPushbackReader import IPushbackReader


class StringPushbackReader(IPushbackReader):
    """
    Wraps string to provide unlimited pushback that allows tokenizers
    to look ahead through stream to perform lexical analysis.
    """
    Eof = -1

    def __init__(self, content):
        self.__pushback_chars_count = 0
        self.__pushback_single_char: int
        self.__pushback_chars = ''

        if not content:
            raise Exception('Content cannot be null')

        self.__content = content
        self.__position = 0

    def read(self):
        if self.__pushback_chars_count == 1:
            self.__pushback_chars_count -= 1
            return self.__pushback_single_char
        elif self.__pushback_chars_count > 1:
            result = ord(self.__pushback_chars[0])
            self.__pushback_chars = self.__pushback_chars[1:]
            self.__pushback_chars_count -= 1

            if self.__pushback_chars_count == 1:
                self.__pushback_single_char = ord(self.__pushback_chars[0])
                self.__pushback_chars = ''

            return result
        else:
            if self.__position < len(self.__content):
                self.__position += 1
                return ord(self.__content[self.__position - 1])

            return StringPushbackReader.Eof

    def peek(self):
        """
        Returns the character from the top of the stream without moving the stream pointer.

        :return: A character from the top of the stream or **-1** if stream is empty.
        """
        if self.__pushback_chars_count == 1:
            return self.__pushback_single_char
        elif self.__pushback_chars_count > 1:
            return ord(self.__pushback_chars[0])
        else:
            return ord(self.__content[self.__position]) if self.__position < len(
                self.__content) else StringPushbackReader.Eof

    def pushback(self, value):
        """
        Puts the specified character to the top of the stream.

        :param value: A character to be pushed back.
        """
        # Skip EOF
        if value == StringPushbackReader.Eof:
            return

        if self.__pushback_chars_count == 0:
            self.__pushback_single_char = value
        elif self.__pushback_chars_count == 1:
            self.__pushback_chars = chr(value) + chr(self.__pushback_single_char)
        else:
            self.__pushback_chars = chr(value) + self.__pushback_chars

        self.__pushback_chars_count += 1

    def pushback_string(self, value):
        """
        Pushes the specified string to the top of the stream.
        
        :param value: A string to be pushed back.
        """
        if value != '':
            if self.__pushback_chars_count == 1:
                self.__pushback_chars = chr(self.__pushback_single_char)

            self.__pushback_chars = value + self.__pushback_chars
            self.__pushback_chars_count += len(value)
