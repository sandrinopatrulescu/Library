from domain.book import Book
from domain.client import Client
from domain.exceptions import StoreException
from domain.rental import Rental


class BookValidatorException(StoreException):
    pass


class ClientValidatorException(StoreException):
    pass


class RentalValidatorException(StoreException):
    pass


class BookValidator(object):
    @staticmethod
    def validate(book):
        try:
            new_book = Book(int(book.id), book.title, book.author)
            book = new_book
        except ValueError:
            raise BookValidatorException("book_id must be an int!")
        if book.id < 0:
            raise BookValidatorException("book_id must be greater or equal than 0!")
        if book.title == "":
            raise BookValidatorException("title must not be an empty string!")
        if book.author == "":
            raise BookValidatorException("author must not be an empty string!")


class ClientValidator(object):
    @staticmethod
    def validate(client):
        try:
            new_client = Client(int(client.id), client.name)
            client = new_client
        except ValueError:
            raise ClientValidatorException("client_id must be an int!")
        if client.id < 0:
            raise ClientValidatorException("client_id must be greater or equal than 0")
        if client.name == "":
            raise ClientValidatorException("name must not be an empty string!")


class RentalValidator(object):
    @staticmethod
    def validate(rental):
        try:
            new_rental = Rental(int(rental.id), rental.book_id, rental.client_id, rental.rented_date, rental.returned_date)
            rental = new_rental
        except ValueError:
            raise RentalValidatorException("rental_id must be an int!")
        try:
            new_rental = Rental(rental.id, int(rental.book_id), rental.client_id, rental.rented_date, rental.returned_date)
            rental = new_rental
        except ValueError:
            raise RentalValidatorException("book_id must be an int!")
        try:
            new_rental = Rental(rental.id, rental.book_id, int(rental.client_id), rental.rented_date, rental.returned_date)
            rental = new_rental
        except ValueError:
            raise RentalValidatorException("client_id must be an int!")
        if rental.id < 0:
            raise RentalValidatorException("rental_id must be greater or equal than 0")
        if type(rental.book_id) is not int:
            raise RentalValidatorException("book_id must be an int!")
        if rental.book_id < 0:
            raise RentalValidatorException("book_id must be greater or equal than 0!")
        if type(rental.client_id) is not int:
            raise RentalValidatorException("client_id must be an int!")
        if rental.client_id < 0:
            raise RentalValidatorException("client_id must be greater or equal than 0")
