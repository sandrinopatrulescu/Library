import datetime
import unittest

from domain.book import Book
from domain.client import Client
from domain.exceptions import BookSearchException, ClientSearchException
from domain.validators import BookValidator, ClientValidator, RentalValidator
from repository.repo import Repository
from services.book_service import BookService
from services.client_service import ClientService
from services.rental_service import RentalService


class TestBookService(unittest.TestCase):
    def setUp(self):
        self._book_service = BookService(BookValidator, Repository(BookValidator))
        self.assertEqual(self._book_service.list(), "Repository is empty!")
        self._book_service.create(1, "abc", "xyz")
        self._book_service.create(4, "def", "uvw")
        self._book_service.create(9, "ghi", "rst")
        self._book_service.create(10, "da", "nu")
        self._book_service.create(49, "h", "v")
        self.assertEqual(self._book_service.list(), self._book_service._BookService__repository.__str__())

    def test_create(self):
        self._book_service.create(5, "adb", "xyz")
        self.assertEqual(self._book_service._BookService__repository.__getitem__(5).__str__(), Book(5, "adb", "xyz").__str__())

    def test_remove(self):
        self.assertEqual(self._book_service.remove(10), 10)
        self.assertEqual(self._book_service._BookService__repository.__len__(), 4)

    def test_update(self):
        new_book = Book(7, "potter", "rowling")
        self._book_service.update(1, 7, "potter", "rowling")
        self.assertEqual(self._book_service._BookService__repository.__getitem__(7).__str__(), new_book.__str__())
        self.assertEqual(self._book_service._BookService__repository.find(1), -1)

    def test_search(self):
        self.assertRaises(BookSearchException, self._book_service.search, *["", ""])
        self.assertRaises(ValueError, self._book_service.search, *["", "id"])
        self.assertEqual(self._book_service.search(-1, "id"), "No such books found")
        self.assertEqual(self._book_service.search(1, "id"), "book_id: 1, title: abc, author: xyz\n")
        self.assertEqual(self._book_service.search("h", "title"), "book_id: 9, title: ghi, author: rst\nbook_id: 49, title: h, author: v\n")
        self.assertEqual(self._book_service.search("v", "author"), "book_id: 4, title: def, author: uvw\nbook_id: 49, title: h, author: v\n")

    def tearDown(self):
        pass


class TestClientService(unittest.TestCase):
    def setUp(self):
        self._client_service = ClientService(ClientValidator, Repository(ClientValidator))
        self.assertEqual(self._client_service.list(), "Repository is empty!")
        self._client_service.create(101, "Brandon Urie")
        self._client_service.create(104, "Adam Levine")
        self._client_service.create(109, "5SOS")
        self._client_service.create(110, "three days grace")
        self._client_service.create(149, "icon for hire")
        self.assertEqual(self._client_service.list(), self._client_service._ClientService__repository.__str__())

    def test_create(self):
        self._client_service.create(102, "LOST KINGS")
        self.assertEqual(self._client_service._ClientService__repository.__getitem__(102).__str__(),
                         Client(102, "LOST KINGS").__str__())

    def test_remove(self):
        self.assertEqual(self._client_service.remove(149), 149)
        self.assertEqual(self._client_service._ClientService__repository.__len__(), 4)

    def test_update(self):
        new_client = Client(107, "zedd")
        self._client_service.update(101, 107, "zedd")
        self.assertEqual(self._client_service._ClientService__repository.__getitem__(107).__str__(), new_client.__str__())
        self.assertEqual(self._client_service._ClientService__repository.find(101), -1)

    def test_search(self):
        self.assertRaises(ClientSearchException, self._client_service.search, *["", ""])
        self.assertRaises(ValueError, self._client_service.search, *["", "id"])
        self.assertEqual(self._client_service.search(-1, "id"), "No such clients found")
        self.assertEqual(self._client_service.search(101, "id"), "client_id: 101, name: Brandon Urie\n")
        self.assertEqual(self._client_service.search("5", "name"), "client_id: 109, name: 5SOS\n")
        self.assertEqual(self._client_service.search("re", "name"),
                         "client_id: 110, name: three days grace\nclient_id: 149, name: icon for hire\n")

    def tearDown(self):
        pass


class TestRentalService(unittest.TestCase):
    def setUp(self):
        book_validator = BookValidator()
        book_repository = Repository(book_validator)
        book_service = BookService(book_validator, book_repository)
        self._book_service = book_service

        client_validator = ClientValidator()
        client_repository = Repository(client_validator)
        client_service = ClientService(client_validator, client_repository)
        self._client_service = client_service

        rental_validator = RentalValidator()
        rental_repository = Repository(rental_validator)
        self._rental_service = RentalService(rental_validator, rental_repository, book_repository, client_repository)

        self._book_service.create(1, "Meditations", "Marcus Aurelius")
        self._book_service.create(2, "War and Peace", "Leo Tolstoy")
        self._book_service.create(3, "Crime and Punishment", "Dostoevsky")
        self._book_service.create(4, "The Idiot", "Dostoevsky")
        self._book_service.create(5, "A Confession", "Leo Tolstoy")
        self._book_service.create(11, "Critique of Pure Reason", "Immanuel Kant")
        self._book_service.create(12, "Republic", "Plato")
        self._book_service.create(13, "Man’s Search for Meaning", "Viktor Frankl")
        self._book_service.create(14, "Paltinis Diary", "Gabriel Liiceanu")
        self._book_service.create(15, "Demons", "Dostoevsky")
        self._client_service.create(101, "Hermione Kline")
        self._client_service.create(102, "Felix Fox")
        self._client_service.create(103, "Eden Clements")
        self._client_service.create(104, "Lowkey Tesseract")
        self._client_service.create(105, "Annie Copeland")
        self._client_service.create(111, "Rosie Simpson")
        self._client_service.create(112, "Kyla Chan")
        self._client_service.create(113, "Scarlet Lane")
        self._client_service.create(114, "Scarlet Lane")
        self._client_service.create(115, "Mark Jefferson")

        #print(self._rental_service.most_rented_books())

        self._rental_service.rent_book(53, 11, 104)
        self._rental_service.__getitem__(53).rented_date = datetime.date(2020, 10, 1)
        self._rental_service.__getitem__(53).returned_date = datetime.date(2020, 11, 21)

        self._rental_service.rent_book(51, 15, 104)
        date = datetime.date(2020, 11, 1)
        self._rental_service.__getitem__(51).rented_date = date

        self._rental_service.rent_book(52, 3, 111)
        date = datetime.date(2020, 10, 9)
        self._rental_service.__getitem__(52).rented_date = date

        #print(self._rental_service.most_rented_books())

    def test_sort(self):
        initial_dict = {"a": 420, "b": 69, "c": 1337}
        sorted_dict = {"c": 1337, "a": 420, "b": 69}
        self.assertEqual(self._rental_service.sort(initial_dict), sorted_dict)

    def test_rent_book(self):
        self.assertRaises(ValueError, self._rental_service.rent_book, *[51, 15, 101])
        self.assertRaises(ValueError, self._rental_service.rent_book, *[55, 0, 101])
        self.assertRaises(ValueError, self._rental_service.rent_book, *[55, 15, 69])
        self.assertRaises(ValueError, self._rental_service.rent_book, *[55, 15, 102])

        rental = self._rental_service.rent_book(56, 11, 103)
        self.assertEqual([rental.id, rental.book_id, rental.client_id], [56, 11, 103])

    def test_return_book(self):
        self.assertRaises(ValueError, self._rental_service.return_book, *[53, 11, 104])
        self.assertRaises(ValueError, self._rental_service.return_book, *[59, 15, 104])
        self.assertRaises(ValueError, self._rental_service.return_book, *[51, 12, 104])
        self.assertRaises(ValueError, self._rental_service.return_book, *[51, 15, 100])

        returnal = self._rental_service.return_book(51, 15, 104)
        self.assertEqual(returnal.returned_date, datetime.date.today())

    def test_most_rented_books(self):
        pass

    def test_most_active_clients(self):
        self._rental_service.run_stats()
        returnal = self._rental_service.return_book(51, 15, 104)
        self._rental_service.__getitem__(51).returned_date = datetime.date(2020, 11, 21)
        rental = self._rental_service.rent_book(56, 15, 113)
        rental.rented_date = datetime.date(2020, 12, 1)
        # TODO: self._rental_service.rent_count_of_books - dictionary check
        print(self._rental_service.most_rented_books())
        print(self._rental_service.most_active_clients())
        print(self._rental_service.most_rented_author())

    def test_most_rented_author(self):
        pass

    def tearDown(self):
        pass
