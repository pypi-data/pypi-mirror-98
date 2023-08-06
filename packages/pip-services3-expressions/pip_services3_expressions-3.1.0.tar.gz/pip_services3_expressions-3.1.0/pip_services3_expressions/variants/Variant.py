# -*- coding: utf-8 -*-

import copy
from datetime import datetime
from decimal import Decimal

from pip_services3_commons.convert.StringConverter import StringConverter
from .VariantType import VariantType


class Variant:
    """
    Defines container for variant values.
    """

    __empty = None

    def __init__(self, value=None):
        """
        Constructs this class and Assignes another variant value.

        :param value: value a value to be assigned to this variant.
        """
        self.__type: VariantType
        self.__value = None
        self.as_object = value

    @staticmethod
    def Empty():
        if Variant.__empty is None:
            Variant.__empty = Variant(None)
        return Variant.__empty

    @property
    def type(self):
        """
        Gets a type of the variant value

        :return:  the variant value type
        """
        return self.__type

    @property
    def as_integer(self):
        """
        Sets variant value as integer
        """
        return self.__value

    @as_integer.setter
    def as_integer(self, value):
        """
        Sets variant value as integer

        :param value: a value to be set
        """
        self.__type = VariantType.Integer
        self.__value = value

    @property
    def as_long(self):
        """
        Gets variant value as long

        :return: number value
        """
        return self.__value

    @as_long.setter
    def as_long(self, value):
        """
        Sets variant value as long
        """
        self.__type = VariantType.Long
        self.__value = value

    @property
    def as_boolean(self):
        """
        Gets variant value as boolean
        """
        return self.__value

    @as_boolean.setter
    def as_boolean(self, value):
        """
        Sets variant value as boolean

        :param value: a value to be set
        """
        self.__type = VariantType.Boolean
        self.__value = value

    @property
    def as_float(self):
        """
        Gets variant value as float
        """
        return self.__value

    @as_float.setter
    def as_float(self, value):
        """
        Sets variant value as float

        :param value: a value to be set
        """
        self.__type = VariantType.Float
        self.__value = value

    @property
    def as_double(self):
        """
        Gets variant value as double
        """
        return self.__value

    @as_double.setter
    def as_double(self, value):
        """
        Sets variant value as double

        :param value: a value to be set
        """
        self.__type = VariantType.Double
        self.__value = value

    @property
    def as_string(self):
        """
        Gets variant value as string
        """
        return self.__value

    @as_string.setter
    def as_string(self, value):
        """
        Sets variant value as string

        :param value: a value to be set
        """
        self.__type = VariantType.String
        self.__value = value

    @property
    def as_datetime(self):
        """
        Gets variant value as datetime
        """
        return self.__value

    @as_datetime.setter
    def as_datetime(self, value):
        """
        Sets variant value as datetime

        :param value: a value to be set
        """
        self.__type = VariantType.DateTime
        self.__value = value

    @property
    def as_time_span(self):
        """
        Gets variant value as time span
        """
        return self.__value

    @as_time_span.setter
    def as_time_span(self, value):
        """
        Sets variant value as :class:`TimeSpan <VariantType.TimeSpan>`

        :param value: a value to be set
        """
        self.__type = VariantType.TimeSpan
        self.__value = value

    @property
    def as_object(self):
        """
        Gets variant value as Object
        """
        return self.__value

    @as_object.setter
    def as_object(self, value):
        """
        Sets variant value as Object

        :param value: a value to be set
        """
        self.__value = value
        if value is None:
            self.__type = VariantType.Null
        elif type(value) == int:
            self.__type = VariantType.Integer
        elif type(value) == float:
            self.__type = VariantType.Float
        elif type(value) == Decimal:
            self.__type = VariantType.Double
        elif type(value) == bool:
            self.__type = VariantType.Boolean
        elif issubclass(datetime, type(value)):
            self.__type = VariantType.DateTime
        elif type(value) == str:
            self.__type = VariantType.String
        elif type(value) == list:
            self.__type = VariantType.Array
        elif isinstance(value, Variant):
            self.__type = value.__type
            self.__value = value.__value
        else:
            self.__type = VariantType.Object

    @property
    def as_array(self):
        """
        Gets variant value as variant array
        """
        return self.__value

    @as_array.setter
    def as_array(self, value):
        """
        Sets variant value as variant array

        :param value: a value to be set
        """
        self.__type = VariantType.Array
        if value is not None:
            self.__value = copy.deepcopy(value)
        else:
            self.__value = None

    @property
    def length(self):
        """
        Gets length of the array
        
        :return: The length of the array or 0
        """
        if self.__type == VariantType.Array and type(self.__value) == list:
            return len(self.__value)
        return 0

    @length.setter
    def length(self, value):
        if self.__type == VariantType.Array:
            self.__value = copy.deepcopy(self.__value)

            for _ in range(value):
                self.__value.append(None)
        else:
            raise Exception('Cannot set array length for non-array data type.')

    def get_by_index(self, index):
        """
        Gets an array element by its index.

        :param index: an element index
        :return: a requested array element
        """
        if self.__type == VariantType.Array:
            if type(self.__value) == list and len(self.__value) > index:
                return self.__value[index]
            else:
                raise Exception('Requested element of array is not accessible.')
        else:
            raise Exception('Cannot access array element for none-array data type.')

    def set_by_index(self, index, element):
        """
        Sets an array element by its index.

        :param index: an element index
        :param element: an element value
        """
        if self.__type == VariantType.Array:
            if type(self.__value) == list:
                for _ in range(index + 1):
                    self.__value.append(None)

                self.__value[index] = element
            else:
                raise Exception('Requested element of array is not accessible.')
        else:
            raise Exception('Cannot access array element for none-array data type.')

    def is_null(self):
        """
        Checks is this variant value Null.

        :return: **True** if this variant value is Null.
        """
        return self.__type == VariantType.Null

    def is_empty(self):
        """
        Checks is this variant value empty.

        :return: **True** is this variant value is empty.
        """
        return self.__value is None

    def assign(self, value):
        """
        Assignes a new value to this object.

        :param value: A new value to be assigned.
        """
        if value is not None:
            self.__type = value.__type
            self.__value = value.__value
        else:
            self.__type = VariantType.Null
            self.__value = None

    def clear(self):
        """
        Clears this object and assignes a VariantType.Null type.
        """
        self.__type = VariantType.Null
        self.__value = None

    def to_string(self):
        """
        Returns a string value for this object.

        :return: a string value for this object.
        """
        if self.__value is None:
            return 'null'
        else:
            return StringConverter.to_string(self.__value)

    def equals(self, obj):
        """
        Compares this object to the specified one.

        :param obj: An object to be compared.
        :return: **True** if objects are equal.
        """
        if isinstance(obj, Variant):
            var_obj = obj
            value1 = self.__value
            value2 = var_obj.__value
            if value1 is None or value2 is None:
                return value1 == value2
            return self.__type == var_obj.__type and value1 == value2

        return False

    def clone(self):
        """
        Cloning the variant value

        :return: The cloned value of this variant
        """
        return Variant(copy.deepcopy(self))

    @staticmethod
    def from_integer(value):
        """
        Creates a new variant from Integer value.

        :param value: a variant value.
        :return: a created variant object.
        """
        result = Variant()
        result.as_integer = value
        return result

    @staticmethod
    def from_long(value):
        """
        Creates a new variant from Long value.

        :param value: a variant value.
        :return: a created variant object.
        """
        result = Variant()
        result.as_long = value
        return result

    @staticmethod
    def from_boolean(value):
        """
        Creates a new variant from Boolean value.

        :param value: a variant value.
        :return: a created variant object.
        """
        result = Variant()
        result.as_boolean = value
        return result

    @staticmethod
    def from_float(value):
        """
        Creates a new variant from Float value.

        :param value: a variant value.
        :return: a created variant object.
        """
        result = Variant()
        result.as_float = value
        return result

    @staticmethod
    def from_double(value):
        """
        Creates a new variant from Double value.

        :param value: a variant value.
        :return: a created variant object.
        """
        result = Variant()
        result.as_double = value
        return result

    @staticmethod
    def from_string(value):
        """
        Creates a new variant from String value.

        :param value: a variant value.
        :return: a created variant object.
        """
        result = Variant()
        result.as_string = value
        return result

    @staticmethod
    def from_datetime(value):
        """
        Creates a new variant from DateTime value.

        :param value: a variant value.
        :return: a created variant object.
        """
        result = Variant()
        result.as_datetime = value
        return result

    @staticmethod
    def from_time_span(value):
        """
        Creates a new variant from TimeSpan value.

        :param value: a variant value.
        :return: a created variant object.
        """
        result = Variant()
        result.as_time_span = value
        return result

    @staticmethod
    def from_object(value):
        """
        Creates a new variant from Object value.

        :param value: a variant value.
        :return: a created variant object.
        """
        result = Variant()
        result.as_object = value
        return result

    @staticmethod
    def from_array(value):
        """
        Creates a new variant from Array value.

        :param value: a variant value.
        :return: a created variant object.
        """
        result = Variant()
        result.as_array = value
        return result
