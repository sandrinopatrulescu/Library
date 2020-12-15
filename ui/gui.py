from tkinter import Tk, Frame, Label, Button, Entry, messagebox


class StartPage1(Frame):
    def __init__(self, parent):
        super().__init__(parent)

    class Feature(Frame):
        def __init__(self, parent):
            super().__init__(parent)

        class Option(Frame):
            def __init__(self, parent):
                super().__init__(parent)

            class Action(Frame):
                def __init__(self, parent):
                    super().__init__(parent)

        def add_feature(self):
            pass


class Gui:

    def __init__(self, undo_service, book_service, client_service, rental_service):
        self._tk = Tk()
        self.frames = {}

        self._undo_service = undo_service
        self._book_service = book_service
        self._client_service = client_service
        self._rental_service = rental_service
        self.instructions_2 = {
            'Main Menu': {
                'class': Menu,
                'command': {
                    'text': '0.Quit',
                    'name': self._tk.destroy,
                    'arguments': []
                    },
                'attributes': [
                    '1. Manage clients and books.',
                    '2. Rent or return a book.',
                    '3. Search for clients or books.',
                    '4. Create statistics.',
                    '5. Unlimited undo/redo functionality.',
                ],
                'function': self.show_frame

            },

            '1. Manage clients and books.': {
                'class': Menu,
                'command': {
                    'text': "Go to previous menu",
                    'function': self.show_frame,
                    'arguments': [StartPage]
                },
                'attributes': {
                    "1. Book add",
                    "2. Book remove"
                    "3. Book update",
                    "4. Book list",
                    "5. Client add",
                    "6. Client remove",
                    "7. Client update",
                    "8. Client list",
                },
                'function': self.show_frame
            }
            # TODO: repeat lines 30 - 47 for 4 more times (features 2 - 5)

        }
        self.instructions = {
            '1. Book add': {
                'class': Read,
                'command': {
                    'name': 'show_frame',
                    'arguments': [Feature1]},
                'attributes': [
                    'id',
                    'title',
                    'author'],
                'input_record': ['Store'],
                'function': self._book_service.create,
                'message': ''},

            '2. Book remove': {
                'class': Read,
                'command': {
                    'name': 'show_frame',
                    'arguments': [Feature1]},
                'attributes': [
                    'id'],
                'input_record': ['Remove'],
                'function': self._book_service.remove,
                'message': ''},

            '3. Book update': {
                'class': Read,
                'command': {
                    'name': 'show_frame',
                    'arguments': [Feature1]},
                'attributes': [
                    'id',
                    'new_id',
                    'new_title',
                    'new_author'],
                'input_record': ['Update'],
                'function': self._book_service.update,
                'message': ''},
        }

        self.frames_structures = [
            {'class': StartPage, 'arguments': []},
            {'class': Feature1, 'arguments': []},
            {'class': Feature2, 'arguments': []},
            {'class': Feature3, 'arguments': []},
            {'class': Feature4, 'arguments': []},
            {'class': Feature5, 'arguments': []},
        ]
        for instruction in self.instructions.keys():
            frame_structure = {'class': self.instructions[instruction]['class'], 'arguments': [instruction]}
            self.frames_structures.append(frame_structure)

    def start(self):
        # creating a container
        container = Frame(self._tk)  # container -  a frame of Gui class
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # iterating through a tuple consisting
        # of the different page layouts
        for frame_structure in self.frames_structures:
            Class = frame_structure['class']
            # print(Class, type(Class))
            # print(dir(Class))
            arguments = [container, self, *frame_structure['arguments']]
            frame = Class(*arguments)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[Class] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        self.frames[StartPage].mainloop()

    # to display the current frame passed as
    # parameter
    def show_frame(self, class_name):
        frame = self.frames[class_name]
        frame.tkraise()


"""
class Feature_Factory:
    F1 - O1 -> O8 - input + output
    F2 - O1 -> O2 - input + output
    F3 - O1 -> O2 - input + output
    F4 - 01 -> 03 - outputs
    F5 - 01 -> 02 - outputs?
"""
"""
        wigets = w1, w2, w3, w4, w5, ...
        wk= {'type': Label, 'arguments': [self, text="0. Quit", font="Times", command=self.controller._tk.destroy]}
        x = WIDGET(self, TEXT)
        wiget = {'type': , 'arguments': [self, text="0. Quit", font="Times", command=self.controller._tk.destroy]}
"""


def add_classes():
    all_classes = {StartPage: [Label(StartPage(Frame, Gui), text='Main Menu').grid(row=0, column=4, padx=10, pady=10)],
                   Feature1: 0,
                   Feature2: 0,
                   Feature3: 0,
                   Feature4: 0,
                   Feature5: 0
                   }

    return all_classes


class Menu(Frame):
    def __init__(self, parent, controller, instruction):
        super().__init__(self, parent)
        self.controller = controller
        self.instruction = instruction
        self.list = []

        self.list.append()


class StartPage(Frame):
    """
    parent - used for initializing the widget of the main menu's frame
    """
    def __init__(self, parent, controller):
        super().__init__(parent)  # turn StartPage into a Frame instance with the master parent (will be main frame)
        self.controller = controller

        lbl_title = Label(self, text='Main Menu')
        lbl_title.grid(row=0, column=4, padx=10, pady=10)

        btn_feature_0 = Button(self, text="0. Quit", font="Times", command=self.controller._tk.destroy)
        btn_feature_0.grid(row=1, column=1, padx=10, pady=10)

        btn_feature_1 = Button(self, text="1. Manage clients and books.", command=lambda: self.controller.show_frame(Feature1))
        btn_feature_1.grid(row=2, column=1, padx=10, pady=10)

        btn_feature_2 = Button(self, text="2. Rent or return a book.", command=lambda: self.controller.show_frame(Feature2))
        btn_feature_2.grid(row=3, column=1, padx=10, pady=10)

        btn_feature_3 = Button(self, text="3. Search for clients or books.", command=lambda: self.controller.show_frame(Feature3))
        btn_feature_3.grid(row=4, column=1, padx=10, pady=10)

        btn_feature_4 = Button(self, text="4. Create statistics.", command=lambda: self.controller.show_frame(Feature4))
        btn_feature_4.grid(row=5, column=1, padx=10, pady=10)

        btn_feature_5 = Button(self, text="5. Unlimited undo/redo functionality.", command=lambda: self.controller.show_frame(Feature5))
        btn_feature_5.grid(row=6, column=1, padx=10, pady=10)


class Feature1(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="1. Manage clients and books.")
        title.grid(row=0, column=4)

        btn_option_0 = Button(self, text="Go to previous menu", command=lambda: self.controller.show_frame(StartPage))
        btn_option_0.grid(row=1, column=1)

        btn_option_1 = Button(self, text="1. Book add", command=lambda: self.controller.show_frame(Read))
        btn_option_1.grid(row=2, column=1)

        btn_option_2 = Button(self, text="2. Book remove", command=lambda: self.controller.show_frame(Read))
        btn_option_2.grid(row=3, column=1)

        btn_option_3 = Button(self, text="3. Book update", command=lambda: self.controller.show_frame(Read))
        btn_option_3.grid(row=4, column=1)

        btn_option_4 = Button(self, text="4. Book list", command=lambda: self.controller.show_frame(StartPage))
        btn_option_4.grid(row=5, column=1)

        btn_option_5 = Button(self, text="5. Client add", command=lambda: self.controller.controller.show_frame(Read))
        btn_option_5.grid(row=6, column=1)

        btn_option_6 = Button(self, text="6. Client remove", command=lambda: self.controller.scontroller.show_frame(Read))
        btn_option_6.grid(row=7, column=1)

        btn_option_7 = Button(self, text="7. Client update", command=lambda: self.controller.controller.show_frame(Read))
        btn_option_7.grid(row=8, column=1)

        btn_option_8 = Button(self, text="8. Client list", command=lambda: self.controller.show_frame(StartPage))
        btn_option_8.grid(row=9, column=1)


class Read(Frame):
    def __init__(self, parent, controller, instruction):
        Frame.__init__(self, parent)
        self.controller = controller
        self.instruction = instruction
        self.list = []

        """
        every Read frame will print at first the button pressed before and the go back button
        thus the list comprehension starts from 2
        """
        self.list.append(Button(self, text=self.instruction, command=lambda: getattr(self.controller, controller.instructions[self.instruction]['command']['name'])(*controller.instructions[self.instruction]['command']['arguments'])))
        self.list[0].grid(row=0, column=4)
        # self.list.append(Button(self, text="1. Book add", command=lambda: self.controller.show_frame(Feature1)))
        # self.list[0].grid(row=0, column=4)

        self.list.append(Button(self, text="Go to previous menu", command=lambda: self.controller.show_frame(Feature1)))
        self.list[1].grid(row=1, column=1)

        row = 2  # where input fields start from row == len(self.list) + 1
        for attribute in controller.instructions[self.instruction]['attributes']:  # getting the keys
            # self.list.append(Button(self, text=instruction[self.instruction]['attributes'][attribute]))
            input_field = {'label': Label(self, text=attribute), 'entry': Entry(self)}
            input_field['label'].grid(row=row, column=1)
            input_field['entry'].grid(row=row, column=2)
            self.list.append(input_field)
            row = row + 1

        # TODO: maybe add to list, then change size in self.execute TOO
        for input_message in controller.instructions[self.instruction]['input_record']:
            input_record = Button(self, text=input_message, command=self.execute)
            input_record.grid(row=row, column=2)
            row = row + 1

        # self.list.append(Label(self, text="ID:"))
        # self.list[1].grid(row=2, column=1)
        # self.list.append(Entry(self))
        # self.list[2].grid(row=2, column=2)
        #
        # self.list.append(Label(self, text="Title:"))
        # self.list[3].grid(row=3, column=1)
        # self.list.append(Entry(self))
        # self.list[4].grid(row=3, column=2)
        #
        # self.list.append(Label(self, text="Author:"))
        # self.list[5].grid(row=4, column=1)
        # self.list.append(Entry(self))
        # self.list[6].grid(row=4, column=2)

        # self.list.append(Button(self, text='Store', command=self.eval))
        # self.list[7].grid(row=5, column=2)

    def execute(self):
        try:
            parameters = []
            for input_field in self.list[2:len(self.list)]:
                parameter = input_field['entry'].get()
                parameters.append(parameter)
            result = self.controller.instructions[self.instruction]['function'](*parameters)
            messagebox.showinfo("Success", "Result: %s " % result)
        except Exception as e:
            raise e
            messagebox.showinfo("Error", "Error:" + str(e))


class Feature2(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="2. Rent or return a book.")
        title.grid(row=0, column=4)

        btn_option_0 = Button(self, text="Go to previous menu", command=lambda: self.controller.show_frame(StartPage))
        btn_option_0.grid(row=1, column=1)

        btn_option_1 = Button(self, text="1. Rent book", command=lambda: self.controller.show_frame(StartPage))
        btn_option_1.grid(row=2, column=1)

        btn_option_2 = Button(self, text="2. Return book", command=lambda: self.controller.show_frame(StartPage))
        btn_option_2.grid(row=3, column=1)


class Feature3(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="3. Search for clients or books.")
        title.grid(row=0, column=4)

        btn_option_0 = Button(self, text="Go to previous menu", command=lambda: self.controller.show_frame(StartPage))
        btn_option_0.grid(row=1, column=1)

        btn_option_1 = Button(self, text="1. Search book (id/title/author)", command=lambda: self.controller.show_frame(StartPage))
        btn_option_1.grid(row=2, column=1)

        btn_option_2 = Button(self, text="2. Search client (id/name)", command=lambda: self.controller.show_frame(StartPage))
        btn_option_2.grid(row=3, column=1)


class Feature4(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="4. Create statistics.")
        title.grid(row=0, column=4)

        btn_option_0 = Button(self, text="Go to previous menu", command=lambda: self.controller.show_frame(StartPage))
        btn_option_0.grid(row=1, column=1)

        btn_option_1 = Button(self, text=" 1. Most rented books", command=lambda: self.controller.show_frame(StartPage))
        btn_option_1.grid(row=2, column=1)

        btn_option_2 = Button(self, text=" 2. Most active clients", command=lambda: self.controller.show_frame(StartPage))
        btn_option_2.grid(row=3, column=1)

        btn_option_3 = Button(self, text=" 3. Most rented author", command=lambda: self.controller.show_frame(StartPage))
        btn_option_3.grid(row=4, column=1)


class Feature5(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="5. Unlimited undo/redo functionality.")
        title.grid(row=0, column=4)

        btn_option_0 = Button(self, text="Go to previous menu", command=lambda: self.controller.show_frame(StartPage))
        btn_option_0.grid(row=1, column=1)

        btn_option_1 = Button(self, text="1. Undo", command=lambda: self.controller.show_frame(StartPage))
        btn_option_1.grid(row=2, column=1)

        btn_option_2 = Button(self, text="2. Redo", command=lambda: self.controller.show_frame(StartPage))
        btn_option_2.grid(row=3, column=1)
