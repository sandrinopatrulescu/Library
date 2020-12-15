import datetime
import unittest

from domain.book import Book
from domain.client import Client
from domain.rental import Rental
from domain.validators import BookValidator, ClientValidator, ClientValidatorException, BookValidatorException, \
    RentalValidator, RentalValidatorException


class TestBook(unittest.TestCase):
    def test_book(self):
        item = Book(1, "abc", "ABC")
        self.assertEqual(item.id, 1)
        self.assertEqual(item.title, "abc")
        self.assertEqual(item.author, "ABC")

    def test_title_setter(self):
        item = Book(20, "a", "abcd")
        item.title = "b"
        self.assertEqual(item.title, "b")

    def test_author_setter(self):
        item = Book(20, "a", "abcd")
        item.author = "efg"
        self.assertEqual(item.author, "efg")

    def test_str(self):
        item = Book(1, "abc", "ABC")
        self.assertEqual("book_id: 1, title: abc, author: ABC", item.__str__())


class TestBookValidator(unittest.TestCase):
    def test_book_validator(self):
        val = BookValidator()
        # book invalid if book_id is not int
        book = Book("abc", "lll", 17)
        try:
            val.validate(book)
            assert False
        except BookValidatorException:
            pass

        # book invalid if book_id is lower than 0
        book = Book(-1, "lll", 17)
        try:
            val.validate(book)
            assert False
        except BookValidatorException:
            pass

        # book invalid if title is empty string
        book = Book(1, "", "abc")
        try:
            val.validate(book)
            assert False
        except BookValidatorException:
            pass

            # book invalid if author is empty string
            book = Book(1, "abc", "")
            try:
                val.validate(book)
                assert False
            except BookValidatorException:
                pass


class TestClient(unittest.TestCase):
    def test_client_getters(self):
        item = Client(1, "zz")
        self.assertEqual(item.id, 1)
        self.assertEqual(item.name, "zz")

    def test_client_setters(self):
        item = Client(1, "zz")
        try:
            item.id = 5
            self.assertFalse("client_id was set, though it should not have happened")
        except AttributeError as aerror:
            self.assertTrue(str(aerror) == "can't set attribute")

        item.name = "m"
        self.assertNotEqual(item.id, 5)
        self.assertEqual(item.name, "m")

    def test_str(self):
        item = Client(1, "abc")
        self.assertEqual("client_id: 1, name: abc", item.__str__())


class TestClientValidator(unittest.TestCase):
    def test_client_validator(self):
        val = ClientValidator()
        # client invalid if book_id is not int
        client = Client("", "abc")
        try:
            val.validate(client)
            assert False
        except ClientValidatorException:
            pass

        # client invalid if book_id lower than 0
        client = Client(-1, "xyz")
        try:
            val.validate(client)
            assert False
        except ClientValidatorException:
            pass

        # client invalid if name is empty string
        client = Client(1, "")
        try:
            val.validate(client)
            assert False
        except ClientValidatorException:
            pass


class TestRental(unittest.TestCase):
    def test_rental(self):
        rental = Rental(1, 2, 3, None, None)
        self.assertEqual(rental.id, 1)
        self.assertEqual(rental.book_id, 2)
        self.assertEqual(rental.client_id, 3)
        rental.rented_date = 4
        self.assertEqual(rental.rented_date, 4)
        rental.returned_date = 5
        self.assertEqual(rental.returned_date, 5)


class TestRentalValidator(unittest.TestCase):
    def test_rental_validator(self):
        val = RentalValidator()
        #
        rental = Rental("", 2, 3, None, None)
        try:
            val.validate(rental)
            assert False
        except RentalValidatorException:
            pass

        #
        rental = Rental(-1, 2, 3, None, None)
        try:
            val.validate(rental)
            assert False
        except RentalValidatorException:
            pass

        #
        rental = Rental(1, "", 3, None, None)
        try:
            val.validate(rental)
            assert False
        except RentalValidatorException:
            pass

        #
        rental = Rental(1, -1, 3, None, None)
        try:
            val.validate(rental)
            assert False
        except RentalValidatorException:
            pass

        #
        rental = Rental(1, 1, "", None, None)
        try:
            val.validate(rental)
            assert False
        except RentalValidatorException:
            pass

        #
        rental = Rental(1, 1, -1, None, None)
        try:
            val.validate(rental)
            assert False
        except RentalValidatorException:
            pass
