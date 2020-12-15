from domain.entitywithid import EntityWithId


class Book(EntityWithId):

    def __init__(self, book_id_, title, author):
        super().__init__(book_id_)
        self.__title = title
        self.__author = author

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, new_value):
        self.__title = new_value

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, new_value):
        self.__author = new_value

    def __str__(self):
        result = "book_id: " + str(self.id) + ','
        result = result + " title: " + str(self.__title) + ','
        result = result + " author: " + str(self.__author)
        return result

    def __eq__(self, other):
        if self.id != other.id or self.__title != other.__title or self.__author != other.__author:
            return False
        return True
