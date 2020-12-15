from dataclasses import dataclass


from domain.entitywithid import EntityWithId


@dataclass
class Client(EntityWithId):
    def __init__(self, id_, name):
        super().__init__(id_)
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def __str__(self):
        result = "client_id: " + str(self.id) + ','
        result = result + " name: " + str(self.name)
        return result
