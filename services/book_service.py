from a10_module.filter import filtering_function
from domain.book import Book
from domain.exceptions import BookSearchException
from repository.repo import RepositoryException
from services.undo_and_redo_service import FunctionCall, Operation, CascadeOperation


class BookService(object):
    """
    Manages book services
    """

    def __init__(self, undo_service, rental_service, validator, repository, caller=None):
        self.__undo_service = undo_service
        self.__rental_service = rental_service
        self.__validator = validator
        self.__repository = repository
        self._caller = caller

    def create(self, id_, title, author):
        """
        Create, validate and store new book
        :param id_: non-null int
        :param title: string
        :param author: string
        :returns: book: Book
        :raises BookValidatorException: - invalid book format
                 RepositoryException: - book id already exists
        """
        book = Book(id_, title, author)
        # validate, raise exception if book is invalid
        self.__validator.validate(book)
        # store the book, raise exception if duplicate id
        if self.__repository.find_using_attribute('id', id_) != -1:
            raise RepositoryException("Item with id=" + str(book.id) + " already in the repo.")
        self.__repository.store(book)

        if self._caller != "undo":
            # then record
            del self.__undo_service._history[self.__undo_service._index + 1:]
            undo = FunctionCall(self.remove, book.id)
            redo = FunctionCall(self.create, book.id, book.title, book.author)
            operation = Operation(undo, redo)
            self.__undo_service.record(operation)
        self._caller = "default"
        return book

    def remove(self, id_):
        """
        Remove book with given ID
        :returns: - removed book
        :raises RepositoryException: - book id doesn't exist
        """

        """
        1. We delete the book from the repository
        """
        self.__validator.validate(Book(id_, None, None))
        book = self.__repository.get_by_attribute('id', id_)
        self.__repository.remove_by_attribute('id', id_)

        """
        2. We delete the rentals with the respective book from the repository
        """
        rentals = self.__rental_service.filter_rentals(None, id_, None, None, None)
        for rental in rentals:
            self.__rental_service.remove(rental.id)

        if self._caller != "undo":
            del self.__undo_service._history[self.__undo_service._index + 1:]
            undo = FunctionCall(self.create, id_, book.title, book.author)
            redo = FunctionCall(self.remove, id_)
            operation = Operation(undo, redo)
            # self.__undo_service.record(operation)

            cascade_list = [operation]
            for rental in rentals:
                undo = FunctionCall(self.__rental_service.create_rental, rental.id, rental.book_id, rental.client_id,
                                    rental.rented_date, rental.returned_date)
                redo = FunctionCall(self.__rental_service.remove, rental.id)
                cascade_list += [Operation(undo, redo)]
            cascaded_operation = CascadeOperation(*cascade_list)
            self.__undo_service.record(cascaded_operation)
        self._caller = "default"
        return book

    def update(self, id_, new_id, new_title, new_author):
        """
        Update book with given ID
        :param id_: non-null int
        :param new_id: non-null int
        :param new_title: string
        :param new_author: string
        :return: old_book - the old book
        :raises BookValidatorException: - invalid book format
                    RepositoryException: - book id to update doesn't exist
        """
        new_book = Book(new_id, new_title, new_author)

        # validate the new book
        self.__validator.validate(new_book)

        # get the old book
        old_book = self.__repository.get_by_attribute('id', id_)

        if self._caller != "undo":
            del self.__undo_service._history[self.__undo_service._index + 1:]
            undo = FunctionCall(self.update, new_book.id, old_book.id, old_book.title, old_book.author)
            redo = FunctionCall(self.update, old_book.id, new_book.id, new_book.title, new_book.author)
            operation = Operation(undo, redo)
        """assuming id can be also updated, then we will update the rentals"""
        if new_id != id_:
            rentals = self.__rental_service.filter_rentals(None, old_book.id, None, None, None)
            for rental in rentals:
                self.__rental_service.update_rental(rental.id, rental.id, new_book.id, rental.client_id, rental.rented_date,
                                                    rental.returned_date)

            if self._caller != "undo":
                rentals = self.__rental_service.filter_rentals(None, new_book.id, None, None, None)
                cascade_list = [operation]
                for rental in rentals:
                    undo = FunctionCall(self.__rental_service.update_rental, rental.id, rental.id, old_book.id, rental.client_id,
                                        rental.rented_date, rental.returned_date)
                    redo = FunctionCall(self.__rental_service.update_rental, rental.id, rental.id, new_book.id, rental.client_id,
                                        rental.rented_date, rental.returned_date)
                    cascade_list = cascade_list + [Operation(undo, redo)]
                cascade_operation = CascadeOperation(*cascade_list)
                self.__undo_service.record(cascade_operation)
        else:
            if self._caller != "undo":
                self.__undo_service.record(operation)
        self._caller = "default"
        # update the book
        self.__repository.update_by_attribute('id', id_, new_book)
        return old_book

    def list(self):
        """
        :return: the list of books
        """
        books = str(self.__repository)
        if books == "":
            return "No books in the repo"
        return books

    def filter(self, attribute, value):
        result = []
        books = self.__repository.get_all()
        filter_function = lambda item: getattr(item, attribute) == type(getattr(item, attribute))(value)
        result = filtering_function(books, filter_function)
        return result

    def search(self, searched_attribute, searched_value):
        """
        Search for books with given field and given value for the field
        :returns found_books: - string which contains the found books
        """
        books = self.__repository.get_all()
        found_books = ""
        for book in books:
            try:
                attribute_value = getattr(book, searched_attribute)
            except AttributeError as ae:
                raise BookSearchException("Book doesn't have such attribute")
            if isinstance(attribute_value, int):
                try:
                    searched_value = int(searched_value)
                    if searched_value == attribute_value:
                        found_books = found_books + (book.__str__()) + '\n'
                except ValueError:
                    raise ValueError("Value must be int for int attributes")
            elif searched_value.lower() in attribute_value.lower():
                found_books = found_books + (book.__str__()) + '\n'
        if found_books == "":
            found_books = "No such books found"
        return found_books
