import tkinter as tk
from Pages.StartingPage import SearchForTnForm


# from Pages.scratch import Scratch


class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.title(self, "Minagate")
        # tk.Tk.attributes(self, '-fullscreen', True)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10, )
        container.grid_rowconfigure(0, weight=1,minsize=1000)
        container.grid_columnconfigure(0, weight=1,minsize=1000)

        '''
        here is the pages of our App
        '''
        self.frames = {}
        for page in (SearchForTnForm,):
            frame = page(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[page] = frame

        self.show_frame(SearchForTnForm)

    # to show pages (routing)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


app = MainApp()
app.mainloop()
