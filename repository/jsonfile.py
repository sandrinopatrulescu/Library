import json
import os

from domain.book import Book
from repository.repo import Repository, IterableBasedRepository


class JsonFileRepository(IterableBasedRepository):
    def __init__(self, filename, entity_type):
        super().__init__(entity_type)
        self._file_name = filename
        self._load_file()

    def _load_file(self):
        if os.path.getsize(self._file_name) != 0:
            with open(self._file_name, 'r') as json_file:
                json_serialized_books = json.load(json_file)
                for json_serialized_book in json_serialized_books:
                    values_of_attributes = json.loads(json_serialized_book)
                    item = self.type(*[values_of_attributes[attribute] for attribute in values_of_attributes])
                    super().store(item)
                json_file.close()

    def _save_file(self):
        with open(self._file_name, 'w') as json_file:
            json_serialized_items = []
            items = self.get_all()
            for item in items:
                json_serialized_item = json.dumps(item.__dict__)
                json_serialized_items.append(json_serialized_item)
            json.dump(json_serialized_items, json_file)
            json_file.close()

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
    repo = JsonFileRepository('test_json.json', Book)
    book0 = Book(0, 'da', '500')

    def add_entries():
        # repo.remove_all()
        print(repo.store(Book(1, "1", "11")))
        repo.store(Book(99, 'idk', 'idk2'))
        print(repo.store(Book(2, "2", "22")))
        print(repo.store(Book(3, "3", "33")))
        print(repo.update_by_attribute('title', 'idk', Book(2, 'nu', 'nu')))
        print(repo.remove_by_attribute('id', 2))
        repo.store(Book(55, 'test', 'da, test'))
        repo.store(book0)
    add_entries()
    print(repo.__str__())


#test()
'''
class JsonFileRepository(Repository):
    def __init__(self):
        super().__init__()

    def _save_file(self):
        pass

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


class BookJsonFileRepository(JsonFileRepository):
    def __init__(self, filename):
        super().__init__()
        self._file_name = filename
        self._load_file()

    def _load_file(self):
        """

        :return:
        """
        with open(self._file_name, 'r') as json_file:
            json_serialized_books = json.load(json_file)
            for json_serialized_book in json_serialized_books:
                book_as_dictionary = json.loads(json_serialized_book)
                book = Book(0, "0", "0")
                for attribute in book_as_dictionary.keys():
                    value = book_as_dictionary[attribute]
                    book.__setattr__(attribute, value)
                super().store(book)

    def _save_file(self):
        """

        :return:
        """
        with open(self._file_name, 'w') as json_file:
            json_serialized_books = []
            books = self.get_all()
            for book in books:
                json_serialized_book = json.dumps(book.__dict__)
                json_serialized_books.append(json_serialized_book)
            json.dump(json_serialized_books, json_file)


class ClientJsonFileRepository(JsonFileRepository):
    def __init__(self, filename):
        super().__init__()
        self._file_name = filename
        self._load_file()

    def _load_file(self):
        """

        :return:
        """
        with open(self._file_name, 'r') as json_file:
            json_serialized_clients = json.load(json_file)
            for json_serialized_client in json_serialized_clients:
                client_as_dictionary = json.loads(json_serialized_client)
                client = Client(0, "0")
                for attribute in client_as_dictionary.keys():
                    value = client_as_dictionary[attribute]
                    client.__setattr__(attribute, value)
                super().store(client)

    def _save_file(self):
        """

        :return:
        """
        with open(self._file_name, 'w') as json_file:
            json_serialized_clients = []
            clients = self.get_all()
            for client in clients:
                json_serialized_client = json.dumps(client.__dict__)
                json_serialized_clients.append(json_serialized_client)
            json.dump(json_serialized_clients, json_file)


class RentalJsonFileRepository(JsonFileRepository):
    def __init__(self, filename):
        super().__init__()
        self._file_name = filename
        self._load_file()

    def _load_file(self):
        """

        :return:
        """
        with open(self._file_name, 'r') as json_file:
            json_serialized_rentals = json.load(json_file)
            for json_serialized_rental in json_serialized_rentals:
                rental_as_dictionary = json.loads(json_serialized_rental)
                rental = Rental(0, 0, 0, None, None)
                for attribute in rental_as_dictionary.keys():
                    value = rental_as_dictionary[attribute]
                    rental.__setattr__(attribute, value)
                super().store(rental)

    def _save_file(self):
        """

        :return:
        """
        with open(self._file_name, 'w') as json_file:
            json_serialized_rentals = []
            rentals = self.get_all()
            for rental in rentals:
                json_serialized_rental = json.dumps(rental.__dict__, default=str)
                json_serialized_rentals.append(json_serialized_rental)
            json.dump(json_serialized_rentals, json_file)


def test():
    books = [Book(1, "in cautarea timpului pierdut", "m. proust"), Book(2, "v s b c f m", "liviu guta")]
    book = Book(1, "in cautarea timpului pierdut", "m. proust")
    print(book.__dict__)

    with open('test_json.json', 'w') as json_file:
        data = []
        for book in books:
            data.append(json.dumps(book.__dict__))
        json.dump(data, json_file)

    with open('test_json.json', 'r') as json_file:
        data_as_json = json.load(json_file)
        for json_dict in data_as_json:
            # print(json_dict)
            py_dict = json.loads(json_dict)
            book = Book(0, "0", "0")
            for key in py_dict.keys():
                book.__setattr__(key, py_dict[key])
            #super().store(book)

test()

"""
def _load_file(self):
    with open('test_json.json', 'r') as json_file:
    

def _save_file(self):
    with open('test_json.json', 'w') as json_file:
        books = self.get_all()
        for book in books:
            json.dump(book.__dict__, json_file)
        
"""


# with open('test_json.json', 'r') as json_file:
#     data = json.load(json_file)
#     for line in data:
#         print(data)
#         print()


    # json_data = json.load(json_file)  # READ JSON FROM FILE
    # print(json_data)
    # dict_data = json.loads(json_data) # CONVERT JSON TO PYHTON DICT     print(json_data, type(json_data))
    # print(json.loads(json_data), type(json.loads(json_data),))
'''
