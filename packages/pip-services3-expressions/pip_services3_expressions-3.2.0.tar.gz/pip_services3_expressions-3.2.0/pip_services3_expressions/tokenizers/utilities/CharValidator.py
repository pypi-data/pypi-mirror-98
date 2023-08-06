# -*- coding: utf-8 -*-

class CharValidator:
    Eof = 0xffff
    Zero = ord('0')
    Nine = ord('9')

    @staticmethod
    def is_eof(value):
        return value == CharValidator.Eof or value == -1

    @staticmethod
    def is_eol(value):
        return value == 10 or value == 13

    @staticmethod
    def is_digit(value):
        return CharValidator.Zero <= value <= CharValidator.Nine
