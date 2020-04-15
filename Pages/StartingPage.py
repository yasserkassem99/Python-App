import tkinter as tk
from utility.textparser import arabic
from utility.api import Api
from tkinter import ttk
import threading

minagateTheme = {
    'SECONDARY': '#397aa5',
    'PRIMARY': '#97c666',
    'DANGER': '#aa2a2a',
}


class SearchForTnForm(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame1 = tk.Frame(self, width=100, height=100)
        frame1.pack(fill=tk.X, )
        # label
        tn_label = tk.Label(frame1, text=arabic('رقم الشاحنة'), font='Arial 25')
        tn_label.pack()
        # tn input
        self.tn = tk.StringVar()
        tn_input = tk.Entry(frame1, textvariable=self.tn, font='Arial 30', justify='right')
        tn_input.pack(padx=10, pady=15)
        # button
        tn_search = tk.Button(frame1, text=arabic('بحث'), font='Arial 25', command=self.search_in_tn, bg='#97c666',
                              fg='#fff')
        tn_search.pack()

        # error frame
        self.error_value = tk.StringVar()
        error_label = tk.Label(frame1, textvariable=self.error_value, fg='#aa2a2a', font=' Arial 25')
        error_label.pack(pady=5)

        # loading indicator
        loading_frame = tk.Frame(frame1)
        loading_frame.pack(pady=5, side=tk.TOP)
        self.loadingBar = ttk.Progressbar(frame1, orient='horizontal', length=200)

        # result frame
        self.frame2 = tk.Frame(frame1, width=100, height=100)
        # label
        trn_label = tk.Label(self.frame2, text=arabic('رقم المقطورة'), font='Arial 25')
        trn_label.pack()
        # trn input
        self.trn = tk.StringVar()
        trn_input = tk.Entry(self.frame2, textvariable=self.trn, font='Arial 30', justify='right')
        trn_input.pack(pady=20)
        # label
        nn_label = tk.Label(self.frame2, text=arabic('الرقم الوطني'), font='Arial 25')
        nn_label.pack()

        # nn input
        self.nn = tk.StringVar()
        nn_input = tk.Entry(self.frame2, textvariable=self.nn, font='Arial 30', justify='right')
        nn_input.pack(pady=20)

        # change nn button
        nn_search = tk.Button(self.frame2, text=arabic('نغيير الرقم الوطني'), font='Arial 20',
                              command=self.search_in_nn,
                              bg='#97c666',
                              fg='#fff')
        nn_search.pack(pady=10)

        # label
        name_frame = tk.Frame(self.frame2)
        name_frame.pack(pady=5)
        self.name = tk.StringVar()
        name_label = tk.Label(name_frame, text=arabic('السائق :'), font='Arial 25')
        name_label.pack(side=tk.RIGHT, padx=3)
        name_value = tk.Label(name_frame, textvariable=self.name, font='Arial 25', fg=minagateTheme['SECONDARY'])
        name_value.pack(side=tk.RIGHT)

        # label
        cargo_frame = tk.Frame(self.frame2)
        cargo_frame.pack(pady=45)
        self.cargo = tk.StringVar()
        cargo_label = tk.Label(cargo_frame, text=arabic('الحمولة :'), font='Arial 25')
        cargo_label.pack(side=tk.RIGHT, padx=3)
        cargo_value = tk.Label(cargo_frame, textvariable=self.cargo, font='Arial 25', fg=minagateTheme['SECONDARY'])
        cargo_value.pack(side=tk.RIGHT)

        # label
        dest_frame = tk.Frame(self.frame2)
        dest_frame.pack(pady=5)
        self.dest = tk.StringVar()
        dest_label = tk.Label(dest_frame, text=arabic('الوجهة :'), font='Arial 25')
        dest_label.pack(side=tk.RIGHT, padx=3)
        dest_value = tk.Label(dest_frame, textvariable=self.dest, font='Arial 25', fg=minagateTheme['SECONDARY'])
        dest_value.pack(side=tk.RIGHT)

    def search_tn(self):
        try:
            tn = int(self.tn.get())
            result = Api(
                path='waybill_order',
                method='searchTruckTripByTerminal',
                params={'tn': tn}).get()
            print(result)
            # if there is error
            self.loadingBar.pack_forget()
            if result.get('ERRORCODE') and result['ERRORCODE'] == 500:
                self.error_value.set(arabic(result['CODE']))
                self.frame2.pack_forget()
            else:
                self.error_value.set('')
                self.trn.set(result['trn'])
                self.nn.set(result['driver_nn'])
                self.cargo.set(arabic(result["cargo_name"]))
                self.dest.set(arabic(result['destination_name']))
                self.name.set(arabic(result['driver_name']))
                self.frame2.pack(padx=10, pady=10, side=tk.BOTTOM)

        except (ValueError, SyntaxError):
            self.error_value.set(arabic('الرجاء ادخال رقم صحيح'))
            self.loadingBar.pack_forget()

    def search_nn(self):
        try:
            nn = int(self.nn.get())
            print(nn)
            result = Api(
                path='driver',
                method='driverAutoCompleteForTerminal',
                params={'user_answer': nn}).get()
            print(result)
            # if there is error
            self.loadingBar.pack_forget()
            if not result:
                self.error_value.set(arabic('الرقم الوطني غير صحيح'))
            else:
                self.error_value.set('')
                self.name.set(arabic(result))
        except (ValueError, SyntaxError):
            self.error_value.set(arabic('الرجاء ادخال رقم وطني صحيح'))
            self.loadingBar.pack_forget()

    def loading(self):
        self.loadingBar.pack()
        self.loadingBar.start()

    def search_in_tn(self):
        x0 = threading.Thread(target=self.loading)
        x0.start()
        x1 = threading.Thread(target=self.search_tn)
        x1.start()

    def search_in_nn(self):
        x0 = threading.Thread(target=self.loading)
        x0.start()
        x1 = threading.Thread(target=self.search_nn)
        x1.start()
