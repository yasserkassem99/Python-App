import tkinter as tk
from utility.textparser import arabic


class Scratch(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame1 = tk.Frame(self, width=100, height=100)
        frame1.pack(fill=tk.X, padx=10, pady=10)
        # label
        label = tk.Label(frame1, text=arabic('رقم الشاحنة'), font='Arial 25')
        label.pack()
        # input
        self.tn = tk.StringVar()
        tn_input = tk.Entry(frame1, textvariable=self.tn, font='Arial 25')
        tn_input.pack(padx=10, pady=10)

        # button
        tn_search = tk.Button(frame1, text=arabic('بحث'), font='Arial 25', command=self.search_tn, bg='#97c666',
                              fg='#fff')
        tn_search.pack()

    def search_tn(self):
        tn = self.tn.get()
        print(tn)
