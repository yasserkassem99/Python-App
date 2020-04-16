import tkinter as tk
from Pages.StartingPage import SearchForTnForm
from Pages.Message import Message



class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.title(self, "Minagate")
        # tk.Tk.attributes(self, '-fullscreen', True)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10, )
        container.grid_rowconfigure(0, weight=1, )
        container.grid_columnconfigure(0, weight=1,)

        '''
        here is the pages of our App
        '''
        self.frames = {}
        for i,page in enumerate((SearchForTnForm, Message)):
            frame = page(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[f'{i}'] = frame

        self.show_frame('0')

    # to show pages (routing)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


app = MainApp()
app.mainloop()
