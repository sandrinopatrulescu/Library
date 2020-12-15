import os
import pickle

from domain.book import Book
from repository.repo import Repository, IterableBasedRepository


class BinaryFileRepository(IterableBasedRepository):
    def __init__(self, filename, entity_type):
        super().__init__(entity_type)
        self._file_name = filename
        self._load_file()

    def _load_file(self):

        if os.path.getsize(self._file_name) != 0:
            with open(self._file_name, 'rb') as file:
                for item in pickle.load(file):
                    self.store(item)
                file.close()

    def _save_file(self):
        with open(self._file_name, 'wb') as file:
            items = super().get_all()
            pickle.dump(items, file)
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
    repo = BinaryFileRepository('test_file.bin', Book)
    book0 = Book(0, 'da', '500')
    print(repo.store(Book(1, "1", "11")))
    repo.store(Book(99, 'idk', 'idk2'))
    print(repo.store(Book(2, "2", "22")))
    print(repo.store(Book(3, "3", "33")))
    print(repo.update_by_attribute('title', 'idk', Book(2, 'nu', 'nu')))
    print(repo.remove_by_attribute('id', 2))

    repo.store(Book(55, 'test', 'da, test'))

    repo.store(book0)
    print(repo.__str__())


#test()


# books = [Book(1, "in cautarea timpului pierdut", "m. proust"), Book(2, "v s b c f m", "liviu guta")]
# file = open("binary.pickle", 'wb')
# pickle.dump(books, file)
# file.close()
#
# file = open('binary.pickle', 'rb')
# for l in pickle.load(file):
#     print(l.__str__())

# repo = BinaryFileRepository('binary.pickle')
# repo.store(Book(9, "ceai", "deliric"))
# print(repo.__str__())
# repo.store(Book())

