import tkinter as tk
from tkinter import ttk

LARGEFONT = ("Verdana", 35)


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):
            frame = F(container, self)
            print(F, type(F))
            print(dir(F))

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # first window frame startpage


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="Startpage", font=LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="Page 2",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)

    # second window frame page1


class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 1", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="StartPage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text="Page 2",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)

    # third window frame page2


class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 2", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Startpage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)

    # Driver Code


app = tkinterApp()
app.mainloop()

"""
from tkinter import Tk, Frame, Label, Button


class Gui:
    def __init__(self, undo_service, book_service, client_service, rental_service):
        self.tk = Tk()  # self.tk - the instance of Tk()
        self.frame = None
        self._undo_service = undo_service
        self._book_service = book_service
        self._client_service = client_service
        self._rental_service = rental_service

        container = Frame(self)
        container.pack()

        self.frames = {}

        for frame_class in (StartPage, Page1, Page2):
            frame = frame_class(container, self)
            self.frames[frame_class] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def main_menu(self):
        self.title("Library")

        # frame = Frame(self.tk, bg='blue', relief="raised")  # self.tk = None - an empty window
        # frame.pack()
        #frame.pack(fill='both')  # if not used it will give a small size to the window

        frame = Frame(self.tk, bg='blue', relief="flat")
        frame.pack()
        self.frame = frame

        feature1_frame = Frame(frame)
        feature1_option1 = Button(text="1. Book add").pack()
        feature1_option1 = Button(text="2. Book remove").pack()
        feature1_option1 = Button(text="3. Book update").pack()
        feature1_option1 = Button(text="4. Book list").pack()
        feature1_option1 = Button(text="5. Client add").pack()
        feature1_option1 = Button(text="6. Client remove").pack()
        feature1_option1 = Button(text="7. Client update").pack()
        feature1_option1 = Button(text="8. Client list").pack()

        feature0 = Button(frame, text="0. Quit.", command=self.destroy).pack()
        feature1 = Button(frame, text="1. Manage clients and books.", command=feature1_frame.pack()).pack()
        feature2 = Button(frame, text="2. Rent or return a book.").pack()
        feature3 = Button(frame, text="3. Search for clients or books.").pack()
        feature4 = Button(frame, text="4. Create statistics.").pack()
        feature5 = Button(frame, text="5. Unlimited undo/redo functionality.").pack()


        self.mainloop()
    def run(self):


class StartPage(Frame):
    def __init__(self):
        pass


# second window frame page1
class Page1(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = tLabel(self, text="Page 1", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = Button(self, text="StartPage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button2 = Button(self, text="Page 2",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)

    # third window frame page2


class Page2(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Page 2", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = tButton(self, text="Startpage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)

def test():
    main_window = Tk()  # Tk(screenName=None,  baseName=None,  className="Window Title",  useTk=1)

    main_window.geometry("300x400+0+300")  # width x height + pixels_from_top_right_on_x + pixels_from_top_right_on_y
    main_window.title("This is the title")  # - title

    start_message = Label(main_window, text="Library", bg='purple')
    second_message = Label(main_window, text="Da, chiar asa", bg='green')
        # padx=? - extend label size on horizontal
        # pady=? - extend label size on veritcal
    start_message.pack(fill="y", side="left", padx=500, pady=350)
    second_message.pack(fill="both", side="top", padx=100)
    main_window.mainloop()


# test()

"""