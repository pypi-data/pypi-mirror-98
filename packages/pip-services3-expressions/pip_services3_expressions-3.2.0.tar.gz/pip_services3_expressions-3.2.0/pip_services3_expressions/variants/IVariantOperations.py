# -*- coding: utf-8 -*-

from abc import ABC


class IVariantOperations(ABC):
    """
    Defines an interface for variant operations manager.
    """

    def convert(self, value, new_type):
        """
        Converts variant to specified type

        :param value: A variant value to be converted.
        :param new_type: A type of object to be returned.
        :return: A converted Variant value.
        """

    def add(self, value1, value2):
        """
        Performs '+' operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def sub(self, value1, value2):
        """
        Performs '-' operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def mul(self, value1, value2):
        """
        Performs '*' operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def div(self, value1, value2):
        """
        Performs '/' operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def mod(self, value1, value2):
        """
        Performs '%' operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def pow(self, value1, value2):
        """
        Performs '^' operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def and_(self, value1, value2):
        """
        Performs AND operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def or_(self, value1, value2):
        """
        Performs OR operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def xor(self, value1, value2):
        """
        Performs XOR operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def lsh(self, value1, value2):
        """
        Performs << operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def rsh(self, value1, value2):
        """
        Performs >> operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def not_(self, value):
        """
        Performs NOT operation for two variants.

        :param value: The operand for this operation.
        :return: A result variant object.
        """

    def negative(self, value):
        """
        Performs unary '-' operation for a variant.

        :param value: The operand for this operation.
        :return: A result variant object.
        """

    def equal(self, value1, value2):
        """
        Performs '=' operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def not_equal(self, value1, value2):
        """
        Performs '<>' operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def more(self, value1, value2):
        """
        Performs '<' operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def less(self, value1, value2):
        """
        Performs '>' operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def more_equal(self, value1, value2):
        """
        Performs '<=' operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def less_equal(self, value1, value2):
        """
        Performs '>=' operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def in_(self, value1, value2):
        """
        Performs IN operation for two variants.

        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """

    def get_element(self, value1, value2):
        """
        Performs [] operation for two variants.
        
        :param value1: The first operand for this operation.
        :param value2: The second operand for this operation.
        :return: A result variant object.
        """
