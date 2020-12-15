class EntityWithId:
    """
    Objects of this type have an id property used to uniquely identify them
    """

    def __init__(self, id_):
        self._id = id_

    @property
    def id(self):
        return self._id
