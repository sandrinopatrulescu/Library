from datetime import date

from a10_module.filter import filtering_function


class Console(object):
    def __init__(self, undo_service, book_service, client_service, rental_service):
        self.__undo_service = undo_service
        self.__book_service = book_service
        self.__client_service = client_service
        self.__rental_service = rental_service

    # TODO: print extra messages for successfulness

    def _print_options(self, options):
        print()
        for option in options.items():
            print(option[1][0])
        print()

    def _book_add(self):
        id_ = input("book id: ").strip()
        title = input("title: ").strip()
        author = input("author: ").strip()
        book = self.__book_service.create(id_, title, author)
        print(book)

    def _book_remove(self):
        id_ = input("book id: ").strip()
        old_book = self.__book_service.remove(id_)
        print(old_book)

    def _book_update(self):
        id_ = input("book id: ").strip()
        new_id = input("new id: ").strip()
        new_title = input("new title: ").strip()
        new_author = input("new author: ").strip()
        self.__book_service.update(id_, new_id, new_title, new_author)

    def _book_list(self):
        books = self.__book_service.list()
        # instance._classname__classattribute
        print(books)

    def _client_add(self):
        id_ = input("client id: ").strip()
        name = input("name: ").strip()
        client = self.__client_service.create(id_, name)
        print(client)

    def _client_remove(self):
        id_ = input("client id: ").strip()
        client = self.__client_service.remove(id_)
        print(client)

    def _client_update(self):
        id_ = input("client id: ").strip()
        new_id = input("new id: ").strip()
        new_name = input("new name: ").strip()
        self.__client_service.update(id_, new_id, new_name)

    def _client_list(self):
        clients = self.__client_service.list()
        print(clients)

    def functionality1_options(self):
        return {1: ("  1. Book add", self._book_add),
                2: ("  2. Book remove", self._book_remove),
                3: ("  3. Book update", self._book_update),
                4: ("  4. Book list", self._book_list),
                5: ("  5. Client add", self._client_add),
                6: ("  6. Client remove", self._client_remove),
                7: ("  7. Client update", self._client_update),
                8: ("  8. Client list", self._client_list),
                }

    def _rent_book(self):
        id_ = int(input("rental id: ").strip())
        book_id = int(input("book id: ").strip())
        client_id = int(input("client id: ").strip())
        rental = self.__rental_service.rent_book(id_, book_id, client_id)
        print(rental)

    def _return_book(self):
        id_ = int(input("rental id: ").strip())
        book_id = int(input("book id: ").strip())
        client_id = int(input("client id: ").strip())
        rental = self.__rental_service.return_book(id_, book_id, client_id, date.today())
        print(rental)

    def functionality2_options(self):
        return {1: ("  1. Rent book", self._rent_book),
                2: ("  2. Return book", self._return_book),
                }

    def _book_search(self):
        attribute = input("field: ").strip()
        value = input("value: ").strip()
        found_book = "No such books found"
        # found_books = self.__book_service.search(value, attribute)
        found_books = self.__book_service.filter(attribute, value)
        print(found_books)

    def _client_search(self):
        attribute = input("field: ").strip()
        value = input("value: ").strip()
        found_clients = "No such clients found"
        # found_clients = self.__client_service.search(value, attribute)
        found_clients = self.__client_service.filter(attribute, value)
        print(found_clients)

    def functionality3_options(self):
        return {1: ("  1. Search book (id/title/author)", self._book_search),
                2: ("  2. Search client (id/name)", self._client_search),
                }

    def _most_rented_books(self):
        print(self.__rental_service.most_rented_books())

    def _most_active_clients(self):
        print(self.__rental_service.most_active_clients())

    def _most_rented_author(self):
        print(self.__rental_service.most_rented_author())

    def functionality4_options(self):
        return {1: ("  1. Most rented books", self._most_rented_books),
                2: ("  2. Most active clients", self._most_active_clients),
                3: ("  3. Most rented author", self._most_rented_author),
                }

    def _undo(self):
        undo = self.__undo_service.undo()
        print(undo)

    def _redo(self):
        redo = self.__undo_service.redo()
        print(redo)

    def functionality5_options(self):
        return {1: ("  1. Undo", self._undo),  # TODO: Implement for Week 10: 1th of Dec
                2: ("  2. Redo", self._redo)}

    def menu_options(self):
        return {0: ("    0. Quit", 0),
            1: ("    1. Manage clients and books.", self.functionality1_options),
            2: ("    2. Rent or return a book.", self.functionality2_options),
            3: ("    3. Search for clients or books.", self.functionality3_options),
            4: ("    4. Create statistics.", self.functionality4_options),
            5: ("    5. Unlimited undo/redo functionality.", self.functionality5_options)}

    def start(self):

        while True:
            print('\n\nChoose functionality:')
            try:
                # used for printing the history
                # print(self.__undo_service.__str__())
                # print("INDEX AT:", self.__undo_service._index)
                tier1_options = self.menu_options()
                self._print_options(tier1_options)
                option = input("Selected functionality: ").strip()
                try:
                    option = int(option)
                except ValueError as ve:
                    raise ValueError("Option number must be a natural number!")
                if option == 0:
                    return
                elif option in tier1_options.keys():
                    # self.menu_options() -> dictionary
                    # self.menu_options()[option] -> dictionary value
                    # self.menu_options()[option][1] -> dictionary value[1] - function call
                    function = 1
                    tier2_options = self.menu_options()[option][function]()
                    self._print_options(tier2_options)
                    child_option = input("Selected feature: ").strip()
                    try:
                        child_option = int(child_option)
                    except ValueError as ve:
                        raise ValueError("Feature number must be a natural number!")
                    if child_option in tier2_options:
                        tier2_options[child_option][function]()
                    else:
                        raise ValueError("Invalid feature number")
                else:
                    raise TypeError("Invalid option number")
            except Exception as e:
                print(e)  # print(e, " str(error)=", str(e))
                # raise e

