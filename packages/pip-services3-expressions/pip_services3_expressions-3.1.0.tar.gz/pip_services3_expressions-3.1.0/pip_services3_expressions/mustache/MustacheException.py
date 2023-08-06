# -*- coding: utf-8 -*-

from pip_services3_commons.errors import BadRequestException


class MustacheException(BadRequestException):
    """
    Exception that can be thrown by Mustache Template.
    """

    def __init__(self, correlation_id=None, code=None, message=None):
        super(MustacheException, self).__init__(correlation_id, code, message)
