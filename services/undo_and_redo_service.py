

class UndoAndRedoService:
    def __init__(self):
        self._history = []
        self._index = -1

    def record(self, operation):
        self._history.append(operation)
        self._index = self._index + 1

    def undo(self):
        if self._index == -1:
            return "No more undos"

        self._history[self._index].undo()  # self._history[self._index] - Operation instance
        self._index = self._index - 1
        return "Undo executed successfully"

    def redo(self):
        if self._index == len(self._history) - 1:
            return "No more redos"

        self._index = self._index + 1
        self._history[self._index].redo()
        return "Redo executed successfully"

    def __str__(self):
        result = ""
        for record_index in range(0, len(self._history)):
            result += str(record_index) + ": " + self._history[record_index].__str__() + '\n'
        return result


class Operation:
    """ Operation() is an entity with a function name and parameters, it can be called"""

    def __init__(self, undo_function_call, redo_function_call):
        self.undo_function_call = undo_function_call
        self.redo_function_call = redo_function_call

    def undo(self):
        self.undo_function_call()

    def redo(self):   # let op = Operation(undo1, redo1) => op.undo() = performing undo1 / calling the function
        self.redo_function_call()

    def __str__(self):
        return "UNDO:" + self.undo_function_call.__str__() + " REDO: " + self.redo_function_call.__str__()


class CascadeOperation:
    def __init__(self, *operations):
        self._operations = operations

    def undo(self):
        for operation in self._operations:
            operation.undo()

    def redo(self):
        for operation in self._operations:
            operation.redo()

    def __str__(self):
        result = ""
        for operation in self._operations:
            result += operation.__str__()
        return result


class FunctionCall:
    def __init__(self, function_reference, *function_parameters):
        self.function_reference = function_reference
        self.function_parameters = function_parameters

    def call(self):
        # self.function_reference.__self__._caller = "undo"

        instance_of_function = self.function_reference.__self__
        instance_of_function._caller = "undo"
        # print(type(self.function_parameters), len(self.function_parameters), self.function_parameters)
        x = [*self.function_parameters]

        return self.function_reference(*self.function_parameters)

    def __call__(self):
        return self.call()  # self.call = self.function_reference(*self.function_parameters)
                            # because '()' - is the function call operator

    def __str__(self):
        return str(self.function_reference) + "(" + str(self.function_parameters) + ")"
