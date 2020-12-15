import datetime

from domain.book import Book
from domain.client import Client
from domain.rental import Rental
from domain.validators import BookValidator, RentalValidator, ClientValidator
from repository.repo import Repository, IterableBasedRepository
from services.book_service import BookService
from services.client_service import ClientService
from services.rental_service import RentalService
from services.undo_and_redo_service import UndoAndRedoService
from settings import Settings
from ui.console import Console


def add_entries():

    # book_repository.remove_all()
    # client_repository.remove_all()
    # rental_repository.remove_all()
    book_service.create(1, "Meditations", "Marcus Aurelius")

    book_service.create(2, "War and Peace", "Leo Tolstoy")
    book_service.create(3, "Crime and Punishment", "Dostoevsky")
    book_service.create(4, "The Idiot", "Dostoevsky")
    book_service.create(5, "A Confession", "Leo Tolstoy")
    book_service.create(11, "Critique of Pure Reason", "Immanuel Kant")
    book_service.create(12, "Republic", "Plato")
    book_service.create(13, "Man’s Search for Meaning", "Viktor Frankl")
    book_service.create(14, "Paltinis Diary", "Gabriel Liiceanu")
    book_service.create(15, "Demons", "Dostoevsky")
    
    client_service.create(101, "Hermione Kline")
    client_service.create(102, "Felix Fox")
    client_service.create(103, "Eden Clements")
    client_service.create(104, "Lowkey Tesseract")
    client_service.create(105, "Annie Copeland")
    client_service.create(111, "Rosie Simpson")
    client_service.create(112, "Kyla Chan")
    client_service.create(113, "Scarlet Lane")
    client_service.create(114, "Scarlet Lane 2")
    client_service.create(115, "Mark Jefferson")

    rental_service.rent_book(53, 11, 104)
    rental_service.__getitem__(53).rented_date = datetime.date(2020, 10, 1)
    rental_service.return_book(53, 11, 104)
    rental_service.__getitem__(53).returned_date = datetime.date(2020, 11, 21)

    rental_service.rent_book(51, 15, 104)
    date = datetime.date(2020, 11, 1)
    rental_service.__getitem__(51).rented_date = date

    rental_service.rent_book(52, 3, 111)
    date = datetime.date(2020, 10, 9)
    rental_service.__getitem__(52).rented_date = date

    client_service.create(0, 0)
    client_service.update(0, 7, 7)
    # print("After updating client 0: client 0 becomes client 7")
    # print(client_service.list())
    
    undo_service.undo()
    # print("After undo : client 0 is back")
    # print(client_service.list())

    undo_service.redo()
    # print("After redo: client 0 becomes client 7")
    # print(client_service.list())

    client_service.update(7, 66, "working")
    # print("we change client 7 to client 66")
    # print(client_service.list())

    # print(rental_service.list())

    rental_service.rent_book(901, 1, 101)
    rental_service.return_book(901, 1, 101)
    rental_service.rent_book(902, 1, 101)
    rental_service.return_book(902, 1, 101)
    rental_service.rent_book(903, 1, 101)
    rental_service.return_book(903, 1, 101)


    '''
    undo_service.undo()
    undo_service.undo()
    undo_service.undo()
    undo_service.undo()
    undo_service.undo()
    undo_service.undo()
    undo_service.undo()
    # undo_service.redo()
    rental_service.rent_book(60, 14, 114)
    undo_service.undo()
    undo_service.undo()
    undo_service.redo()

    # print(rental_service.list())

    # book_service.create(7, "da", "da")
    # book_service.update(7, 8, "nu", "nu")
    '''


if __name__ == "__main__":

    """
    Inheritance:
    
    UI(Console/GUI) -> UndoAndRedoService
    
                    -> RentalService -> UndoAndRedoService
                                     -> RentalValidator
                                     -> Repository (rental/book/client)
                             
                    -> BookService -> UndoAndRedoService
                                   -> RentalService
                                   -> BookValidator
                                   -> Repository (book)

                    -> ClientService -> UndoAndRedoService
                                     -> RentalService
                                     -> ClientValidator
                                     -> Repository (client)
            
    """
    # initiating instances of the services with the required validators and repositories


    # if settings._repository == Repository or settings._repository == IterableBasedRepository:
    #     book_repository = settings._repository(Book)
    #     client_repository = settings._repository(Client)
    #     rental_repository = settings._repository(Rental)
    # else:
    #     book_repository = settings._repository(settings._books, Book)
    #     client_repository = settings._repository(settings._clients, Client)
    #     rental_repository = settings._repository(settings._rentals, Rental)

    """ Universal instances required for services"""

    undo_service = UndoAndRedoService()
    book_validator = BookValidator()
    client_validator = ClientValidator()
    rental_validator = RentalValidator()

    settings = Settings("settings.properties")
    book_repository = settings.create('Book')
    client_repository = settings.create('Client')
    rental_repository = settings.create('Rental')

    rental_service = RentalService(undo_service, rental_validator, rental_repository, book_repository,
                                   client_repository)
    book_service = BookService(undo_service, rental_service, book_validator, book_repository)
    client_service = ClientService(undo_service, rental_service, client_validator, client_repository)

    ui = settings.create('ui', [undo_service, book_service, client_service, rental_service])
    # ui = settings._ui(*[[undo_service, book_service, client_service, rental_service]])
    """ Settings-dependent instances, required for services"""

    '''
    # TODO: replace ..._repository=
    # book_repository = Repository()
    # client_repository = Repository()
    # rental_repository = Repository()
    book_repository = settings.class_factory("IterableBasedRepository", [Book])
    client_repository = settings.class_factory("IterableBasedRepository", [Client])
    rental_repository = settings.class_factory("IterableBasedRepository", [Rental])

    # TODO: check if rental_service needs access to book/client service or book/client_repository is enough
    rental_service = RentalService(undo_service, rental_validator, rental_repository, book_repository,
                                   client_repository)
    book_service = BookService(undo_service, rental_service, book_validator, book_repository)
    client_service = ClientService(undo_service, rental_service, client_validator, client_repository)
    
    # TODO: replace ui=
    #ui = Console(undo_service, book_service, client_service, rental_service)
    ui = settings.class_factory("ui", [undo_service, book_service, client_service, rental_service])
    ui.start()
    '''

    # DO NOT CALL add_entries when using file repository which is non_empty
    add_entries()  # adding initial entries
    # print(book_service.list()) - working


    '''
    Set up done, starting program
    '''
    ui.start()
    # try:
    #     ui.start()
    # except Exception as e:
    #     print(e)

    # except ValueError:
    #     print(e, str(e))

    print("bye")
