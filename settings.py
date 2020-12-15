from domain.book import Book
from domain.client import Client
from domain.rental import Rental
from repository.binaryfile import BinaryFileRepository
from repository.jsonfile import JsonFileRepository
from repository.repo import Repository, IterableBasedRepository
from repository.textfile import FileRepository
from ui.console import Console
from ui.gui import Gui


class Settings:
    string_to_class = {
        'Book': Book,
        'Client': Client,
        'Rental': Rental,
        'Repository': Repository,
        'IterableBasedRepository': IterableBasedRepository,
        'FileRepository': FileRepository,
        'BinaryFileRepository': BinaryFileRepository,
        'JsonFileRepository': JsonFileRepository,
        'Console': Console,
        'Gui': Gui
    }

    def __init__(self, filename):
        self._file_name = filename
        self._repository = None
        self._books = None
        self._clients = None
        self._rentals = None
        self._ui = None
        self.file_parse()

    def file_parse(self):
        with open(self._file_name, 'r') as settings:
            for line in settings:
                if '=' in line:
                    name, value = line.split('=', 2)
                    self.__setattr__("_" + name.strip(), value.strip())

    # book_repository = settings.create('Book')
    def create(self, class_name, arguments=None):
        name, attributes = None, None
        if arguments is None:
            arguments = []
        if class_name == 'ui':
            name = self.string_to_class[self._ui]
            attributes = arguments
        if 'File' in self._repository:
            if class_name == 'Book':
                name = self.string_to_class[self._repository]
                attributes = [self._books, self.string_to_class['Book']] + arguments
            if class_name == 'Client':
                name = self.string_to_class[self._repository]
                attributes = [self._clients, self.string_to_class['Client']] + arguments
            if class_name == 'Rental':
                name = self.string_to_class[self._repository]
                attributes = [self._rentals, self.string_to_class['Rental']] + arguments
        else:
            if class_name == 'Book':
                name = self.string_to_class[self._repository]
                attributes = [self.string_to_class['Book']] + arguments
            if class_name == 'Client':
                name = self.string_to_class[self._repository]
                attributes = [self.string_to_class['Client']] + arguments
            if class_name == 'Rental':
                name = self.string_to_class[self._repository]
                attributes = [self.string_to_class['Rental']] + arguments
        if name is attributes is None:
            print("Invalid format for class instantiation")
        else:
            return self.instantiate(name, attributes)

    def instantiate(self, name, attributes):
        instance = name(*attributes)
        return instance


    """
    Main: book_repository = ClassFactory("Book_repository", attributes_list)
    """

    def class_factory(self, class_type, attributes_list=[]):
        if class_type.find("_") != -1:
            entity_setting, class_setting = class_type.split("_", 2)
        else:
            class_setting = class_type
        class_name, class_attributes = None, []
        # getattr(self, "_" + class_setting) - what is stored in settings.properties
        # what's after '==' - the name given at calling in main
        # - class_setting - first name from
        if getattr(self, "_" + class_setting) == 'Console':
            class_name = getattr(self, "_" + class_setting)
            class_attributes = attributes_list
        if getattr(self, "_" + class_setting) == 'Gui':
            class_name = getattr(self, "_" + class_setting)
            class_attributes = attributes_list
        if getattr(self, "_" + class_setting) == 'Repository':
            class_name = 'Repository'
            class_attributes = attributes_list
            if getattr(self, "_" + class_setting) == 'IterableBasedRepository':
                class_name = 'IterableBasedRepository'
                class_attributes = attributes_list
        if getattr(self, "_" + class_setting) == 'FileRepository':
            class_name = entity_setting + getattr(self, "_" + class_setting)
            file_name = getattr(self, "_" + entity_setting.lower() + 's')
            class_attributes = [file_name]
        if getattr(self, "_" + class_setting) == 'BinaryFileRepository':
            class_name = getattr(self, "_" + class_setting)
            file_name = getattr(self, "_" + entity_setting.lower() + 's')
            class_attributes = [file_name]
        if getattr(self, "_" + class_setting) == 'JsonFileRepository':
            class_name = entity_setting + getattr(self, "_" + class_setting)
            file_name = getattr(self, "_" + entity_setting.lower() + 's')
            class_attributes = [file_name]

        instance_creator = InstanceCreator(class_name, class_attributes)
        instance = instance_creator.create()
        return instance


class InstanceCreator:
    classes_dictionary = {
        'Repository': Repository,
        'IterableBasedRepository': IterableBasedRepository,
        'FileRepository': FileRepository,
        'BinaryFileRepository': BinaryFileRepository,
        'JsonFileRepository': JsonFileRepository,
        'Console': Console,
        'Gui': Gui
    }

    def __init__(self, class_name, class_attributes):
        self._class_name = class_name
        self._class_attributes = class_attributes

    def create(self):
        instance = self.classes_dictionary[self._class_name](*self._class_attributes)
        return instance


"""
features = {'Feature0': Feature0, 'options': }, 'Feature1': Feature1, 'Feature2': Feature2, 'Feature3': Feature3, 'Feature4': Feature4, 'Feature5': Feature5}
options =  {'Feat}


"""

"""
    ClassFormulator(class_type(repository/ui), entity(Book, Client, Rental)) :
    self.__getattr__("_" + class_type) -> settings : ex: FileRepository, books.txt, 
                                                         repo_type, books_file, clients_file, re_file, ui
    if  self_repoistory == "Repsitory":
        create class instace(class_name=Repository, attributes=[])
    if self_repository == FileRepository:
       create class instance(class name=entit+class_type, attributes=[self.__getattr__("_" + lower(entity) + 's')])
    ii self_repository == BinaryFileREpository:
       create class instance(class name=self.repository, attributes= [])
    
    if self.ui == "Console"
      create class instance(class name = self.ui, attributes=[])
            
    class_name(Book/Client/Rental/Console/Gui) - determined on settingss
     
"""
