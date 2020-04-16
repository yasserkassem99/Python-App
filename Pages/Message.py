import tkinter as tk
from utility.textparser import arabic
from utility.constants import minagateTheme



class Message(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame1 = tk.Frame(self, width=100, height=100, bg='red')
        frame1.pack(expand=True)

        # label
        label = tk.Label(frame1, text=arabic('تمت العملية بنجاح'), font='Arial 50', fg=minagateTheme['SECONDARY'])
        label.pack()


