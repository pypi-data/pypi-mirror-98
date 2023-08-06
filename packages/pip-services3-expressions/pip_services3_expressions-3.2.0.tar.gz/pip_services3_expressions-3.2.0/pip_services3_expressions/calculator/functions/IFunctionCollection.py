# -*- coding: utf-8 -*-

from .IFunction import IFunction


class IFunctionCollection:
    """
    Defines a functions list.
    """

    # Gets a number of functions stored in the collection.
    length: int

    def add(self, func: IFunction):
        """
        Adds a new function to the collection.

        :param func: a function to be added.
        """

    def get(self, index):
        """
        Get a function by its index.

        :param index: a function index.
        :return: a retrieved function
        """

    def get_all(self):
        """
        Get all functions stores in the collection
        
        :return: a list with functions.
        """

    def find_index_by_name(self, name):
        """
        Finds function index in the list by it's name.

        :param name: The function name to be found.
        :return: Function index in the list or **-1** if function was not found.
        """

    def find_by_name(self, name):
        """
        Finds function in the list by it's name.

        :param name: The function name to be found.
        :return: A function or **None** if function was not found.
        """

    def remove(self, index):
        """
        Removes a function by its index.

        :param index: a index of the function to be removed.
        """

    def remove_by_name(self, name):
        """
        Removes function by it's name.

        :param name: The function name to be removed.
        """

    def clear(self):
        """
        Clears the collection.
        """
