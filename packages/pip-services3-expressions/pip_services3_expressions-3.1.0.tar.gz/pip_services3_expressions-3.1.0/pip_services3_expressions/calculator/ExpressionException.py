# -*- coding: utf-8 -*-

from pip_services3_commons.errors import BadRequestException


class ExpressionException(BadRequestException):
    """
    Exception that can be thrown by Expression Calculator.
    """

    def __init__(self, correlation_id=None, code=None, message=None):
        super(ExpressionException, self).__init__(correlation_id, code, message)
