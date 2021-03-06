from a10_module.iterable_structure import Iterable
from domain.exceptions import StoreException


class RepositoryException(StoreException):
    pass


class Repository:
    def __init__(self, entity_type):
        self.__list = []
        self.type = entity_type

    def find_using_attribute(self, attribute, value):
        """

        :param attribute:
        :param value:
        :return:
        """
        for index in range(len(self.__list)):
            item = self.__list[index]
            if getattr(item, attribute) == type(getattr(item, attribute))(value):
                return index
        return -1

    def store(self, item):
        """
        Validation for attributes is done in the service
        """
        self.__list.append(item)
        return 'Stored ' + str(item)

    def remove_by_attribute(self, attribute, value):
        """

        :param attribute:
        :param value:
        :return:
        """
        index = self.find_using_attribute(attribute, value)
        # if item not in self.__list:
        #     raise RepositoryException("Item is not in the repository!")
        if index == -1:
            raise RepositoryException("Item is not in the repository!")
        del self.__list[index]
        return "Removed item with {} equal to {}".format(attribute, value)

    '''
    Old implementation for remove
    def remove(self, id_):
        """
        Delete item with given attribute from repository
        """
        index = self.find(id_)
        if index == -1:
            raise RepositoryException("Item with id=" + str(id_) + " not in the repo.")

        item = self._data[index]
        # TODO: FIND OUT WHY 'variant1' and 'variant2' don't work
        variant1 = "item = self._data[index]\nself._data.remove(item)"
        variant2 = "item = self.__getitem__(id_)\nself._data.remove(item)"
        variant3 = "item = self._data.pop(index)"
        # item = self._data[index]  # item = self.__getitem__(id_)
        # self._data.remove(item)
        # item = self._data.pop(index)
        exec(variant3)
        return item
    '''

    def update_by_attribute(self, attribute, value, new_item):
        """
        Update an item from repository
        """
        index = self.find_using_attribute(attribute, value)
        # if old_item not in self.__list:
        #     raise RepositoryException("Item is not in the repository!")
        if index == -1:
            raise RepositoryException("Item is not in the repository!")
        self.__list[index] = new_item
        return 'Updated item with {} equal to {}'.format(attribute, value)

    def get_by_attribute(self, attribute, value):
        index = self.find_using_attribute(attribute, value)
        if index == -1:
            raise RepositoryException("Item is not in the repository!")
        return self.__list[index]

    def get_by_index(self, index):
        if index not in range(len(self.__list)):
            raise RepositoryException("Item is not in the repository!")
        return self.__list[index]

    def get_all(self):
        return self.__list

    def remove_all(self):
        length = len(self.__list)
        while length > 0:
            del self.__list[length - 1]
            length = length - 1
        '''
        other option:
                self.__list = []
                return self.__list
        '''
        return "Removed all items"

    def __str__(self):
        result = ""
        for item in self.__list:
            result = result + item.__str__() + '\n'
        return result

    def __len__(self):
        return len(self.__list)


class IterableBasedRepository:
    def __init__(self, entity_type):
        self.type = entity_type
        self.__list = Iterable()

    def find_using_attribute(self, attribute, value):
        """
        Return the index of an object from the repository having the given attribute with the given value
        Returns -1 if no such object was found
        """
        for index in range(len(self.__list)):
            item = self.__list[index]
            if getattr(item, attribute) == type(getattr(item, attribute))(value):
                return index
        return -1

    def store(self, item):
        """
        Stores a new item into the repository
        Validation for attributes is done in the service
        :param item: item to be stored
        :return: string - a message saying what object was stored
        """
        self.__list.append(item)
        return 'Stored ' + str(item)

    def remove_by_attribute(self, attribute, value):
        """
        Remove from the repository the object with the given attribute and value
        :param attribute: the attribute of the object to be removed
        :param value: the value of the attribute of the object which is removed
        :raise: RepositoryException - if there is no item satisfying the given attribute & value -based conditions
        :return: string - a message saying what object was removed
        """
        index = self.find_using_attribute(attribute, value)
        # if item not in self.__list:
        #     raise RepositoryException("Item is not in the repository!")
        if index == -1:
            raise RepositoryException("Item is not in the repository!")
        del self.__list[index]
        return "Removed item with {} equal to {}".format(attribute, value)

    def update_by_attribute(self, attribute, value, new_item):
        """
        Update the repo by replacing an object with a given value for a given attribute with a new given object
        :param attribute: attribute of the to be replaced object
        :param value: attribute's value of the to be replaced object
        :param new_item: the new object which will be replaced with
        :return: string - a message saying which object was updated
        """
        index = self.find_using_attribute(attribute, value)
        # if old_item not in self.__list:
        #     raise RepositoryException("Item is not in the repository!")
        if index == -1:
            raise RepositoryException("Item is not in the repository!")
        self.__list[index] = new_item
        return 'Updated item with {} equal to {}'.format(attribute, value)

    def get_by_attribute(self, attribute, value):
        """
        Get an object from the repository by finding it using the value of a given attribute
        :param attribute: name of the object's attribute
        :param value: value of the object's attribute
        :raise: RepositoryException - in case no such object was found
        :return: the found object
        """
        index = self.find_using_attribute(attribute, value)
        if index == -1:
            raise RepositoryException("Item is not in the repository!")
        return self.__list[index]

    def get_by_index(self, index):
        if index not in range(len(self.__list)):
            raise RepositoryException("Item is not in the repository!")
        return self.__list[index]

    def get_all(self):
        """
        Get all objects in the repository and return them as a list
        :return: a list of all objects present in the repository
        """
        result = []
        for item in iter(self.__list):
            result.append(item)
        return result

    def remove_all(self):
        """
        Remove all items from the repository
        :return: string - a message saying the removal was successful
        """
        length = len(self.__list)
        while length > 0:
            del self.__list[length - 1]
            length = length - 1
        return "Removed all items"  # return []

    def __str__(self):
        """
        Convert repository elements into their string version (assuming it exists)
        :return: string: result - all books from the repository printed line by line
        """
        result = ""
        for item in iter(self.__list):
            result = result + item.__str__() + '\n'
        return result

    def __len__(self):
        return len(self.__list)
