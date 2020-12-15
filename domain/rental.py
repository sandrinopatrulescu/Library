from domain.entitywithid import EntityWithId


class Rental(EntityWithId):
    def __init__(self, id_, book_id, client_id, rented_date=None, returned_date=None):
        super().__init__(id_)
        self.__book_id = book_id
        self.__client_id = client_id
        self.__rented_date = rented_date
        self.__returned_date = returned_date

    @property
    def book_id(self):
        return self.__book_id

    @property
    def client_id(self):
        return self.__client_id

    @property
    def rented_date(self):
        return self.__rented_date

    @rented_date.setter
    def rented_date(self, value):
        self.__rented_date = value

    @property
    def returned_date(self):
        return self.__returned_date

    @returned_date.setter
    def returned_date(self, value):
        self.__returned_date = value

    def __str__(self):
        result = "rental_id: " + str(self.id) + ','
        result = result + " book_id: " + str(self.__book_id) + ','
        result = result + " client_id: " + str(self.client_id) + ','
        result = result + " rented_date: " + str(self.__rented_date) + ','
        result = result + " returned_date: " + str(self.__returned_date)
        return result
