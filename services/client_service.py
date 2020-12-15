from a10_module.filter import filtering_function
from domain.client import Client
from domain.exceptions import ClientSearchException
from repository.repo import RepositoryException
from services.undo_and_redo_service import FunctionCall, Operation, CascadeOperation


class ClientService(object):
    """
    Manages client services
    """
    def __init__(self, undo_service, rental_service, validator, repository, caller=None):
        self.__undo_service = undo_service
        self.__rental_service = rental_service
        self.__validator = validator
        self.__repository = repository
        self._caller = caller

    def create(self, id_, name):
        """
        Create, validate and store new client
        :param id_: non-null integer
        :param name: string
        :returns client: Client
        :raises ClientValidatorException: - invalid client format
                    RepositoryException: - client id already exists
        """
        client = Client(id_, name)
        # validate, raise exception if client is invalid
        self.__validator.validate(client)
        if self.__repository.find_using_attribute('id', client.id) != -1:
            raise RepositoryException("Item with id=" + str(client.id) + " already in the repo.")
        # store the client, raise exception if duplicate id
        self.__repository.store(client)
        # x = dir(self)

        if self._caller != "undo":
            del self.__undo_service._history[self.__undo_service._index + 1:]
            undo = FunctionCall(self.remove, client.id)
            redo = FunctionCall(self.create, client.id, client.name)
            operation = Operation(undo, redo)
            self.__undo_service.record(operation)
        self._caller = "default"
        return client

    def remove(self, id_):
        """
        Remove client with given ID
        :returns: - removed client
        :raises RepositoryException: - client id doesn't exist
        """
        # check what happens at line 48
        self.__validator.validate(Client(id_, None))
        removed_client = self.__repository.remove_by_attribute('id', id_)
        # print(type(client))
        # print(str(client))
        # print(client.__str__())

        """
        2. We delete the rentals with the respective book from the repository
        """
        rentals = self.__rental_service.filter_rentals(None, None, id_, None, None)
        for rental in rentals:
            self.__rental_service.remove(rental.id)

        if self._caller != "undo":
            del self.__undo_service._history[self.__undo_service._index + 1:]
            undo = FunctionCall(self.create, client.id, client.name)
            redo = FunctionCall(self.remove, client.id)
            operation = Operation(undo, redo)

            cascade_list = [operation]
            for rental in rentals:
                undo = FunctionCall(self.__rental_service.create_rental, rental.id, rental.book_id, client.id, rental.rented_date, rental.returned_date)
                redo = FunctionCall(self.__rental_service.remove, rental.id)
                cascade_list += Operation(undo, redo)
            cascade_operation = CascadeOperation(*cascade_list)
            self.__undo_service.record(cascade_operation)
        self._caller = "default"
        return removed_client

    def update(self, id_, new_id, new_name):
        """
        Update client with given ID
        :param id_: non-null int
        :param new_id: non-null int
        :param new_name: string
        :return: old_client - the old client
        :raises BookValidatorException: - invalid client format
                    RepositoryException: - client id to update doesn't exist
        """
        new_client = Client(new_id, new_name)

        # validate the new client
        self.__validator.validate(new_client)

        # get the old client
        old_client = self.__repository.get_by_attribute('id', id_)

        # print("inside client service:", self._caller) - check the caller
        if self._caller != "undo":
            del self.__undo_service._history[self.__undo_service._index + 1:]
            undo = FunctionCall(self.update, new_client.id, old_client.id, old_client.name)
            redo = FunctionCall(self.update, old_client.id, new_client.id, new_client.name)
            operation = Operation(undo, redo)
        """assuming id can be also updated, then we will update the rentals"""
        if new_id != id:
            rentals = self.__rental_service.filter_rentals(None, None, old_client.id, None, None)
            for rental in rentals:
                self.__rental_service.update_rental(rental.id, rental.book_id, new_client.id, rental.rented_date, rental.returned_date)

            if self._caller != "undo":
                rentals = self.__rental_service.filter_rentals(None, None, new_client.id, None, None)
                cascade_list = [operation]
                for rental in rentals:
                    undo = FunctionCall(self.__rental_service.update_rental, rental.id, rental.book_id, old_client.id, rental.rented_date, rental.returned_date)
                    redo = FunctionCall(self.__rental_service.update_rental, rental.id, rental.book_id, new_client.id, rental.rented_date, rental.returned_date)
                    cascade_list += Operation(undo, redo)
                cascade_operation = CascadeOperation(*cascade_list)
                self.__undo_service.record(cascade_operation)
        else:
            if self._caller != "undo":
                self.__undo_service.record(operation)
        self._caller = "default"
        # update the client
        self.__repository.update_by_attribute('id', id_, new_client)
        return old_client

    def list(self):
        """
        :return: the list of clients
        """
        clients = str(self.__repository)
        if clients == "":
            return "No clients in the repo"
        return clients

    def filter(self, attribute, value):
        result = []
        clients = self.__repository.get_all()
        filter_function = lambda item: getattr(item, attribute) == type(getattr(item, attribute))(value)
        result = filtering_function(clients, filter_function)
        return result

    def search(self, searched_attribute, searched_value):
        """
        Search for clients with given field and given value for the field
        :returns found_clients: - string which contains the found clients
        """
        clients = self.__repository.get_all()
        found_clients = ""
        for client in clients:
            try:
                attribute_value = getattr(client, searched_attribute)
            except AttributeError as ae:
                raise ClientSearchException("Book doesn't have such attribute")
            if isinstance(attribute_value, int):
                try:
                    searched_value = int(searched_value)
                    if searched_value == attribute_value:
                        found_clients = found_clients + (client.__str__()) + '\n'
                except ValueError:
                    raise ValueError("Value must be int for int attributes")
            elif searched_value.lower() in attribute_value.lower():
                found_clients = found_clients + (client.__str__()) + '\n'
        if found_clients == "":
            found_clients = "No such clients found"
        return found_clients

