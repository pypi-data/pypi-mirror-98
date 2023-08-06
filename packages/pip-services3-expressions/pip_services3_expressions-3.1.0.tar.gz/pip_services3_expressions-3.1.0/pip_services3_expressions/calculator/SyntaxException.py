# -*- coding: utf-8 -*-

from pip_services3_commons.errors import BadRequestException


class SyntaxException(BadRequestException):
    """
    Exception that can be thrown by Expression Parser.
    """

    def __init__(self, correlation_id=None, code=None, message=None):
        super(SyntaxException, self).__init__(correlation_id, code, message)
