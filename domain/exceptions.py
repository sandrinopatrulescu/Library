

class LibraryException(Exception):
    """
    General Exception class used for Library problem
    """
    pass


class StoreException(LibraryException):
    pass


class ServiceException(LibraryException):
    pass


class BookServiceException(ServiceException):
    pass


class BookSearchException(BookServiceException):
    pass


class ClientServiceException(ServiceException):
    pass


class ClientSearchException(ClientServiceException):
    pass
