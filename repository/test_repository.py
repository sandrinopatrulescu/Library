import unittest
from unittest import TestCase

from domain.book import Book
from repository.repo import Repository, RepositoryException, IterableBasedRepository


class TestRepository(unittest.TestCase):
    def setUp(self):
        """
        Runs before each test method
        """
        self.repo = Repository(Book)
        self.repo.store(Book(1, "Ciuleandra", "Liviu Rebreanu?"))
        self.repo.store(Book(2, "Rascoala", "Liviu Rebreanu"))
        self.repo.store(Book(3, "Ion", "Liviu Rebreanu"))
        self.repo.store(Book(4, "Padurea spanzuratiilor", "Liviu Rebreanu"))

    def test_find_using_attribute(self):
        self.assertEqual(self.repo.find_using_attribute('id', 1), 0)
        self.assertEqual(self.repo.find_using_attribute('title', 'Ion'), 2)

    def test_store(self):
        self.assertEqual(len(self.repo), 4)
        self.repo.store(Book(5, "Cel mai iubit dintre pamanteni", "Marin Preda"))
        self.assertEqual(len(self.repo), 5)

    def test_remove_by_attribute(self):
        self.assertEqual(len(self.repo), 4)
        self.repo.remove_by_attribute('id', 1)
        self.assertEqual(len(self.repo), 3)
        self.assertEqual(self.repo.find_using_attribute('id', 1), -1)
        self.assertRaises(RepositoryException, self.repo.remove_by_attribute, *['id', 10])

    def test_update_by_attribute(self):
        book = Book(100, 'Unknown title', 'Unknown Author')
        self.repo.update_by_attribute('author', 'Liviu Rebreanu?', book)
        self.assertEqual(self.repo.find_using_attribute('id', 1), -1)
        self.assertEqual(self.repo.find_using_attribute('author', 'Unknown Author'), 0)
        self.assertRaises(RepositoryException, self.repo.update_by_attribute, *['title', 'Ciuleandra', book])

    def test_get_by_attribute(self):
        book = self.repo._Repository__list[1]
        self.assertEqual(self.repo.get_by_attribute('title', 'Rascoala'), book)
        self.assertRaises(RepositoryException, self.repo.get_by_attribute, *['title', 'da'])

    def test_get_by_index(self):
        self.assertEqual(self.repo.get_by_index(1), self.repo.get_by_attribute('id', 2))
        self.assertRaises(RepositoryException, self.repo.get_by_index, 6)

    def test_get_all(self):
        self.assertEqual(self.repo.get_all(), [item for item in self.repo._Repository__list])

    def test_remove_all(self):
        self.repo.remove_all()
        self.assertEqual(len(self.repo), 0)

    def test_str(self):
        self.repo.remove_all()
        self.repo.store(Book(1, "abc", "ABC"))
        self.repo.store(Book(2, "efg", "EFG"))
        self.repo.store(Book(3, "hij", "HIJ"))
        repo_string = ""
        repo_string = repo_string + "book_id: 1, title: abc, author: ABC\n"
        repo_string = repo_string + "book_id: 2, title: efg, author: EFG\n"
        repo_string = repo_string + "book_id: 3, title: hij, author: HIJ\n"
        self.assertEqual(str(self.repo), repo_string)

    def tearDown(self):
        print("TORN DOWN")
        """
        Runs after each test method
        """


class TestIterableBasedRepository(TestCase):
    def setUp(self) -> None:
        self.repo = IterableBasedRepository(Book)
        self.repo.store(Book(1, "Ciuleandra", "Liviu Rebreanu?"))
        self.repo.store(Book(2, "Rascoala", "Liviu Rebreanu"))
        self.repo.store(Book(3, "Ion", "Liviu Rebreanu"))
        self.repo.store(Book(4, "Padurea spanzuratiilor", "Liviu Rebreanu"))
        
    def test_find_using_attribute(self):
        self.assertEqual(self.repo.find_using_attribute('id', 1), 0)
        self.assertEqual(self.repo.find_using_attribute('title', 'Ion'), 2)

    def test_store(self):
        self.assertEqual(len(self.repo), 4)
        self.repo.store(Book(5, "Cel mai iubit dintre pamanteni", "Marin Preda"))
        self.assertEqual(len(self.repo), 5)

    def test_remove_by_attribute(self):
        self.assertEqual(len(self.repo), 4)
        self.repo.remove_by_attribute('id', 1)
        self.assertEqual(len(self.repo), 3)
        self.assertEqual(self.repo.find_using_attribute('id', 1), -1)
        self.assertRaises(RepositoryException, self.repo.remove_by_attribute, *['id', 10])

    def test_update_by_attribute(self):
        book = Book(100, 'Unknown title', 'Unknown Author')
        self.repo.update_by_attribute('author', 'Liviu Rebreanu?', book)
        self.assertEqual(self.repo.find_using_attribute('id', 1), -1)
        self.assertEqual(self.repo.find_using_attribute('author', 'Unknown Author'), 0)
        self.assertRaises(RepositoryException, self.repo.update_by_attribute, *['title', 'Ciuleandra', book])

    def test_get_by_attribute(self):
        book = self.repo._IterableBasedRepository__list[1]
        self.assertEqual(self.repo.get_by_attribute('title', 'Rascoala'), book)
        self.assertRaises(RepositoryException, self.repo.get_by_attribute, *['title', 'da'])

    def test_get_by_index(self):

        self.assertEqual(self.repo.get_by_index(1), self.repo.get_by_attribute('id', 2))
        self.assertRaises(RepositoryException, self.repo.get_by_index, 6)

    def test_get_all(self):
        self.assertEqual(self.repo.get_all(), [item for item in self.repo._IterableBasedRepository__list])

    def test_remove_all(self):
        self.repo.remove_all()
        self.assertEqual(len(self.repo), 0)

    def test_str(self):
        self.repo.remove_all()
        self.repo.store(Book(1, "abc", "ABC"))
        self.repo.store(Book(2, "efg", "EFG"))
        self.repo.store(Book(3, "hij", "HIJ"))
        repo_string = ""
        repo_string = repo_string + "book_id: 1, title: abc, author: ABC\n"
        repo_string = repo_string + "book_id: 2, title: efg, author: EFG\n"
        repo_string = repo_string + "book_id: 3, title: hij, author: HIJ\n"
        self.assertEqual(str(self.repo), repo_string)
        
    def tearDown(self) -> None:
        print("TORE DOWN")
