from datetime import date

from a10_module.sort import odd_even_sort
from domain.rental import Rental
from services.undo_and_redo_service import FunctionCall, Operation


class RentalService(object):
    def __init__(self, undo_service, validator, repository, book_repository, client_repository, caller=None):
        self.__undo_service = undo_service
        self.__validator = validator
        self.__repository = repository
        self.__book_repository = book_repository
        self.__client_repository = client_repository
        self._caller = caller

        self.rent_count_of_books = {}
        self.rent_days_of_clients = {}
        self.rent_count_of_authors = {}

        """
        # useful for generating dictionaries
        if self.__book_repository.__len__() == 0:
            self.rent_count_of_books = {}
            self.rent_count_of_authors = {}
        else:
            self.rent_count_of_books = {key: 0 for key in (book.id for book in self.__book_repository.get_all())}
            self.rent_count_of_authors = {key: 0 for key in (book.author for book in self.__book_repository.get_all())}
        if self.__client_repository.__len__() == 0:
            self.rent_days_of_clients = {}
        else:
            self.rent_days_of_clients = {key: 0 for key in (client.id for client in self.__client_repository.get_all())}
        """

    def run_stats(self):
        self.rent_count_of_books = {key: 0 for key in (book.id for book in self.__book_repository.get_all())}
        self.rent_days_of_clients = {key: 0 for key in (client.id for client in self.__client_repository.get_all())}
        self.rent_count_of_authors = {key: 0 for key in (book.author for book in self.__book_repository.get_all())}

    def __getitem__(self, id_):
        return self.__repository.get_by_attribute('id', id_)

    def validate_renting(self, id_, book_id, client_id):
        # TODO: fill specifications
        """

        :param id_:
        :param book_id:
        :param client_id:
        :return:
        """

        if self.__repository.find_using_attribute('id', id_) != -1:
            raise ValueError("rental id already exists")
        if self.__book_repository.find_using_attribute('id', book_id) == -1:
            raise ValueError("book id not found")
        if self.__client_repository.find_using_attribute('id', client_id) == -1:
            raise ValueError("client id not found")
        if len(self.__repository) != 0:
            for rental in self.__repository.get_all():
                if rental.book_id == book_id and rental.returned_date is None:
                    raise ValueError("book is already rented")
        return True

    def create_rental(self, id_, book_id, client_id, rent_date, return_date):
        """
        used by the undo service
        :param id_:
        :param book_id:
        :param client_id:
        :param rent_date:
        :param return_date:
        :return:
        """
        rental = Rental(id_, book_id, client_id, rent_date, return_date)
        self.validate_renting(id_, book_id, client_id)
        # TODO: self.validator.validate()
        self.__repository.store(rental)

        return rental

    def update_rental(self, id_, new_id, new_book_id, new_client_id, new_rent_date, new_return_date):
        """
        used by the undo service
        :param id_:
        :param new_id:
        :param new_book_id:
        :param new_client_id:
        :param new_rent_date:
        :param new_return_date:
        :return:
        """
        rental = Rental(new_id, new_book_id, new_client_id, new_rent_date, new_return_date)
        # TODO: self.validator.validate()

        old_rental = self.__repository.get_by_attribute('id', id_)

        self.__repository.update_by_attribute('id', id_, rental)

        return old_rental

    def rent_book(self, id_, book_id, client_id):
        """

        :param id_:
        :param book_id:
        :param client_id:
        :return:
        """
        self.validate_renting(id_, book_id, client_id)
        rent_date = date.today()
        rental = Rental(id_, book_id, client_id, rent_date, None)
        self.__validator.validate(rental)
        self.__repository.store(rental)

        if self._caller != "undo":
            del self.__undo_service._history[self.__undo_service._index + 1:]
            undo = FunctionCall(self.remove, rental.id)
            redo = FunctionCall(self.create_rental, rental.id, rental.book_id, rental.client_id, rental.rented_date, rental.returned_date)
            operation = Operation(undo, redo)
            self.__undo_service.record(operation)
        self._caller = "default"
        if rental is not None:
            return "Book was successfully rented"
        return rental

    def validate_returning(self, id_, book_id, client_id):
        """

        :param id_:
        :param book_id:
        :param client_id:
        :return:
        """
        if self.__repository.find_using_attribute('id', id_) == -1:
            raise ValueError("rental id not found")
        if self.__repository.get_by_attribute('id', id_).returned_date is not None:
            raise ValueError("the book was already returned")
        if self.__repository.get_by_attribute('id', id_).book_id != book_id:
            raise ValueError("book id doesn't match rental")
        if self.__repository.get_by_attribute('id', id_).client_id != client_id:
            raise ValueError("client id doesn't match rental")

    def return_book(self, id_, book_id, client_id, return_date=date.today()):
        """

        :param id_:
        :param book_id:
        :param client_id:
        :param return_date:
        :return:
        """
        self.validate_returning(id_, book_id, client_id)
        rent_date = self.__repository.get_by_attribute('id', id_).rented_date
        rental = Rental(id_, book_id, client_id, rent_date, return_date)
        self.__validator.validate(rental)
        self.__repository.update_by_attribute('id', id_, rental)

        if self._caller != "undo":
            del self.__undo_service._history[self.__undo_service._index + 1:]
            undo = FunctionCall(self.update_rental, rental.id, rental.id, rental.book_id, rental.client_id, rental.rented_date, None)
            # x = self.update_rental(self.update_rental, rental.id, rental.book_id, rental.client_id, rental.rented_date, None)
            # print(x)
            redo = FunctionCall(self.update_rental, rental.id, rental.id, rental.book_id, rental.client_id, rental.rented_date, rental.returned_date)
            operation = Operation(undo, redo)
            self.__undo_service.record(operation)
        self._caller = "default"
        if rental is not None:
            return "Book was successfully returned"
        return rental

    def sort(self, dictionary):
        """

        :param dictionary:
        :return:
        """
        order = {"ascending": 1, "descending": -1}
        # return {key: value for key, value in sorted(dictionary.items(), key=lambda item: order["descending"] * item[1])}
        converted_to_list = list(dictionary.items())
        odd_even_sort(converted_to_list, lambda item1, item2: item1[1] >= item2[1])
        sorted_list = converted_to_list
        return {item[0]: item[1] for item in sorted_list}

    def most_rented_books(self):
        """
        !!! counts even if book wasn't returned
        :return:
        """
        self.run_stats()
        for rental in self.__repository.get_all():
            self.rent_count_of_books[rental.book_id] = self.rent_count_of_books[rental.book_id] + 1

        sorted_list = self.sort(self.rent_count_of_books)
        self.rent_count_of_books = sorted_list
        # print("check most rented books: ", self.rent_count_of_books)
        result = "Most rented books:\n"
        if self.rent_count_of_books != {}:
            for book_id in self.rent_count_of_books.keys():
                result = result + "count: " + str(self.rent_count_of_books[book_id]) + "  "
                result = result + self.__book_repository.get_by_attribute('id', book_id).__str__() + "\n"

        return result

    def most_active_clients(self):
        """
        !!! counts even if book wasn't returned -> until current system date
        :return:
        """
        self.run_stats()
        for rental in self.__repository.get_all():
            if rental.returned_date is None:
                date_difference = date.today() - rental.rented_date
            else:
                date_difference = rental.returned_date - rental.rented_date
            self.rent_days_of_clients[rental.client_id] = self.rent_days_of_clients[rental.client_id] + int(date_difference.days)

        # print(rent_days_of_clients)  # - check validity
        sorted_list = self.sort(self.rent_days_of_clients)
        self.rent_days_of_clients = sorted_list
        # print(sorted_rent_days_of_clients)  # - check validity
        # print("check most active clients: ", self.rent_days_of_clients)
        result = "Most active clients:\n"
        for client_id in self.rent_days_of_clients.keys():
            result = result + "count: " + str(self.rent_days_of_clients[client_id]) + "  "
            result = result + self.__client_repository.get_by_attribute('id', client_id).__str__() + "\n"

        return result

    def most_rented_author(self):
        """

        :return:
        """
        self.run_stats()
        for rental in self.__repository.get_all():
            author = self.__book_repository.get_by_attribute('id', rental.book_id).author
            self.rent_count_of_authors[author] = self.rent_count_of_authors[author] + 1

        sorted_list = self.sort(self.rent_count_of_authors)
        self.rent_count_of_authors = sorted_list
        # print("check most rented authors: ", self.rent_count_of_authors)
        if len(self.rent_count_of_authors) != 0:
            first = 0
            most_rented_author = list(self.rent_count_of_authors.keys())[first]
            most_rented_books_for_print = self.most_rented_books()

            result = "Books of most rented author" + '\n'

            for book_id in self.rent_count_of_books.keys():
                book = self.__book_repository.get_by_attribute('id', book_id)
                if book.author == most_rented_author:
                    count = self.rent_count_of_books[book.id] if book.id in self.rent_count_of_books.keys() else 0
                    result = result + "count: " + str(count) + "  "
                    result = result + book.__str__() + '\n'

            if result == "Books of most rented author" + '\n':
                result = "No books were rented"
            return result

    def filter_rentals(self, rental_id, book_id, client_id, rented_date, returned_date):
        result = []
        rentals = self.__repository.get_all()
        for rental in rentals:
            if rental_id is not None and rental_id != rental.id:
                continue
            if book_id is not None and book_id != rental.book_id:
                continue
            if client_id is not None and client_id != rental.client_id:
                continue
            if rented_date is not None and rented_date != rental.rental.rented_date:
                continue
            if returned_date is not None and returned_date != rental.rental.returned_date:
                continue
            result.append(rental)
        return result

    def get_all(self):
        rentals = self.__repository.get_all()
        return rentals

    def remove(self, id_):
        rental = self.__repository.remove_by_attribute('id', id_)
        return rental

    def list(self):
        """
        :return: the list of rentals
        """
        rentals = self.__repository.__str__()
        return rentals
