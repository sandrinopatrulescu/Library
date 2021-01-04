import json
import jsonpickle
import os

from domain.book import Book
from repository.repo import Repository, IterableBasedRepository

'''
Swap 'IterableBasedRepository' and 'Repository when necessary'
'''


class FileRepository(IterableBasedRepository):
    def __init__(self, filename, entity_type):
        super().__init__(entity_type)
        self._file_name = filename
        self._load_file()

    def _load_file(self):
        """

        :return:
        """
        if os.path.getsize(self._file_name) != 0:
            with open(self._file_name, 'rt') as file:
                for line in file:
                    values_of_attributes = jsonpickle.loads(line)
                    item = self.type(*[values_of_attributes[attribute] for attribute in values_of_attributes])
                    super().store(item)
                file.close()

    def _save_file(self):
        """

        :return:
        """
        with open(self._file_name, 'wt') as file:
            items = self.get_all()
            for item in items:
                line = jsonpickle.dumps(item.__dict__) + "\n"  # the line stored in the file will be a dictionary of the class
                file.write(line)
            file.close()

    def store(self, item):
        result = super().store(item)
        self._save_file()
        return result

    def remove_by_attribute(self, attribute, value):
        result = super().remove_by_attribute(attribute, value)
        self._save_file()
        return result

    def update_by_attribute(self, attribute, value, item):
        result = super().update_by_attribute(attribute, value, item)
        self._save_file()
        return result

    def remove_all(self):
        result = super().remove_all()
        self._save_file()
        return result


def test():
    repo = FileRepository('temp.txt', Book)

    '''
    print(repo.store(Book(1, "1", "11")))
    repo.store(Book(99, 'idk', 'idk2'))
    print(repo.store(Book(2, "2", "22")))
    print(repo.store(Book(3, "3", "33")))
    print(repo.update_by_attribute('title', 'idk', Book(2, 'nu', 'nu')))
    print(repo.remove_by_attribute('id', 2))
    '''
    repo.store(Book(55, 'test', 'da, test'))

    print(repo.__str__())
    # print(repo.__str__())


#test()
# TODO: remove old classes
'''
class BookFileRepository(Repository):
    """
        Store/retrieve books from file

        Inheritance:
        Repository -> BookFileRepository


        for universal FileRepository class: (use the implementation for RentalFileRepository)
        WHY? because only _load_file and _save_file method differ
        attributes = re.split(': |, ', line)
        attributes_count = len(attributes)
        caller = ?
        for k in range(0, (attributes_count - 2) / 2 + 1):
            for attributes[k-1] in dir(caller):
                type = type(caller.attributes[k-1])
        item/entity = caller(type(*[attribute[k]) for type in ...])
        item/entity = caller()
    """
    def __init__(self, filename):
        super().__init__()
        self._file_name = filename
        self._load_file()

    def _load_file(self):
        """
        :return:
        """
        try:
            file = open(self._file_name, 'rt')
            line = file.readline().strip()
            # line pattern: book_id: 4, title: The Idiot, author: Dostoevsky
            while len(line) > 0:
                # attributes = line.split(', ')
                attributes = re.split(': |, ', line)
                id_, title, author = list(range(1, 6, 2))
                book = Book(int(attributes[id_]), str(attributes[title]), str(attributes[author]))
                super().store(book)  # self.store(book)
                line = file.readline().strip()
        except IOError:
            raise RepositoryException("Input file not found")
        finally:
            try:
                file.close()
            except IOError:
                raise IOError

    def _save_file(self):
        """

        :return:
        """
        try:
            file = open(self._file_name, 'wt')
            books = self.get_all()
            for book in books:
                line = "book_id: " + str(book.id) + ", title: " + book.title + ", author: " + book.author + '\n'
                file.write(line)
        except IOError:
            raise RepositoryException("Output file not found")
        finally:
            try:
                file.close()
            except IOError as ioe:
                raise ioe

    def store(self, item):
        """

        :param item:
        :return:
        """
        super().store(item)
        self._save_file()
        return item

    def remove(self, id_):
        """

        :param id_:
        :return:
        """
        item = super().remove(id_)
        self._save_file()
        return item

    def update(self, id_, item):
        """

        :param id_:
        :param item:
        :return:
        """
        super().update(id_, item)
        self._save_file()

    def remove_all(self):
        """

        :return:
        """
        super().remove_all()
        self._save_file()


# repo = BookFileRepository("books.txt")
# print(repo.__str__())
# repo.remove_all()
# print(repo.__str__())


class ClientFileRepository(Repository):
    """
        Store/retrieve clients from file
    """
    def __init__(self, filename):
        super().__init__()
        self._file_name = filename
        self._load_file()

    def _load_file(self):
        """

        :return:
        """
        with open(self._file_name, 'rt') as file:
            for line in file:
                attributes = re.split(': |, ', line)
                id_, name = range(1, 4, 2)
                client = Client(int(attributes[id_]), attributes[name])
                super().store(client)

    def _save_file(self):
        """

        :return:
        """
        with open(self._file_name, 'wt') as file:
            clients = self.get_all()
            for client in clients:
                line = "client_id: " + str(client.id) + ", name: " + str(client.name) + "\n"
                file.write(line)

    def store(self, item):
        """

        :param item:
        :return:
        """
        super().store(item)
        self._save_file()
        return item

    def remove(self, id_):
        """

        :param id_:
        :return:
        """
        item = super().remove(id_)
        self._save_file()
        return item

    def update(self, id_, item):
        """

        :param id_:
        :param item:
        :return:
        """
        super().update(id_, item)
        self._save_file()

    def remove_all(self):
        """

        :return:
        """
        super().remove_all()
        self._save_file()


class RentalFileRepository(Repository):
    def __init__(self, filename):
        super().__init__()
        self._file_name = filename
        self._load_file()

    def _load_file(self):
        """

        :return:
        """
        with open(self._file_name, 'rt') as file:
            for line in file:
                attributes = re.split(': |, ', line)
                id_, book_id, client_id, rented_date, returned_date = range(1, 11, 5)
                rental = Rental(int(attributes[id_]), int(attributes[book_id]), int(attributes[client_id]), strptime(attributes[rented_date], "%Y-%M-%D"), strptime(attributes[returned_date], "%Y-%M-%D"))
                super().store(rental)

    def _save_file(self):
        """

        :return:
        """
        with open(self._file_name, 'wt') as file:
            rentals = self.get_all()
            for rental in rentals:
                line = rental.__str__() + '\n'
                file.write(line)

    def store(self, item):
        """

        :param item:
        :return:
        """
        super().store(item)
        self._save_file()

    def remove(self, id_):
        """

        :return:
        """
        item = super().remove(id_)
        self._save_file()
        return item

    def update(self, id_, item):
        """

        :param id_:
        :param item:
        :return:
        """
        super().update(id_, item)
        self._save_file()

    def remove_all(self):
        """

        :return:
        """
        super().remove_all()
        self._save_file()
'''