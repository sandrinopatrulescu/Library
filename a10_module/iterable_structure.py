class Iterable(object):
    def __init__(self):
        self.__list = []
        self.__index = 0

    def __getitem__(self, index):
        return self.__list[index]

    def __setitem__(self, index, value):
        self.__list[index] = value

    def __delitem__(self, index):
        del self.__list[index]

    def __next__(self):
        if self.__index < len(self.__list):
            current = self.__list[self.__index]
            self.__index = self.__index + 1
            return current
        else:
            raise StopIteration()

    def __iter__(self):
        self.__index = 0
        return self

    def append(self, item):
        self.__list.append(item)

    def __len__(self):
        return len(self.__list)


def complex_filter(list_for_filter, function):
    pass