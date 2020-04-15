import tkinter as tk
from utility.textparser import ArabicText, arabic,TextInput
import requests
import logging
import threading
import time

class SearchForTnForm(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame1 = tk.Frame(self, width=100, height=100)
        frame1.pack(fill=tk.X, padx=10, pady=10)
        # label
        tn_label = tk.Label(frame1, text=arabic('رقم الشاحنة'), font='Arial 25')
        tn_label.pack()
        # tn input
        self.tn = tk.StringVar()
        tn_input = tk.Entry(frame1, textvariable=self.tn, font='Arial 30')
        tn_input.pack(padx=10, pady=10)
        # button
        tn_search = tk.Button(frame1, text=arabic('بحث'), font='Arial 25', command=self.search_tn, bg='#97c666',
                              fg='#fff')
        tn_search.pack(pady=15)
        # label
        trn_label = tk.Label(frame1, text=arabic('رقم المقطورة'), font='Arial 25')
        trn_label.pack()
        # trn input
        self.trn = tk.StringVar()
        trn_input = tk.Entry(frame1, textvariable=self.trn, font='Arial 30')
        trn_input.pack(padx=10, pady=10)
        # label
        nn_label = tk.Label(frame1, text=arabic('الرقم الوطني'), font='Arial 25')
        nn_label.pack()
        # trn input
        self.nn = tk.StringVar()
        nn_input = tk.Entry(frame1, textvariable=self.nn, font='Arial 30')
        nn_input.pack(padx=10, pady=10)

        frame2 = tk.Frame(frame1, width=100, height=100)
        frame2.pack(padx=10, pady=10)
        # label
        cargo_label = tk.Label(frame2, text=arabic('الحمولة'), font='Arial 25')
        cargo_label.pack(side=tk.RIGHT,pady=10)
        cargo_label.destroy()



    def search_tn(self):
        try:
            tn = self.tn.set('مرحبا')
            print(tn)
            x = threading.Thread(target=self.re, args=(1,))
            logging.info("Main    : before running thread")
            x.start()

        except ValueError:
            print(arabic('الرجاء'))

    def re(self):
        data = {'method': 'searchTruckTripByTerminal', 'tn': 6014660,
                'integration_token': 'tMkHWUvtBtMXf22fmy4mBLuAqvQX4kDw'}
        r = requests.get('https://api-dev-dot-waybill-project.appspot.com/waybill_order', params=data)
        print(r.json())