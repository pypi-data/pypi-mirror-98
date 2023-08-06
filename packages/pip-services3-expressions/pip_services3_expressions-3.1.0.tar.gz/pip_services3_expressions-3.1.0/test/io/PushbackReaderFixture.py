# -*- coding: utf-8 -*-

from pip_services3_expressions.io.IPushbackReader import IPushbackReader
from pip_services3_expressions.tokenizers.utilities.CharValidator import CharValidator


class PushbackReaderFixture:
    __reader: IPushbackReader
    __content: str

    def __init__(self, reader, content):
        self.__reader = reader
        self.__content = content

    def test_operations(self):
        char = self.__reader.peek()
        assert ord(self.__content[0]) == char

        char = self.__reader.read()
        assert ord(self.__content[0]) == char

        self.__reader.pushback(ord('#'))
        char = self.__reader.read()
        assert '#' == chr(char)

        self.__reader.pushback_string("@$")
        char = self.__reader.read()
        assert '@' == chr(char)

        char = self.__reader.read()
        assert '$' == chr(char)

        for i in range(1, len(self.__content)):
            char = self.__reader.read()
            assert ord(self.__content[i]) == char

        char = self.__reader.read()
        assert -1 == char

        char = self.__reader.read()
        assert -1 == char

    def test_pushback(self):
        last_chr: int
        char = self.__reader.read()

        while not CharValidator.is_eof(char):
            char = self.__reader.read()
            last_chr = char

        self.__reader.pushback(last_chr)
        self.__reader.pushback(char)

        char1 = self.__reader.peek()
        assert last_chr == char1

        char1 = self.__reader.peek()
        assert last_chr == char1
