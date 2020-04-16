import time
import tkinter as tk
from utility.textparser import arabic
from utility.api import Api
from tkinter import ttk
import threading
from utility.constants import minagateTheme
import subprocess

def how_many():
    x = threading.enumerate()
    print(x)


class SearchForTnForm(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.tn = tk.StringVar()
        self.error_value = tk.StringVar()
        self.trn = tk.StringVar()
        self.nn = tk.StringVar()
        self.nn_error_value = tk.StringVar()
        self.name = tk.StringVar()
        self.cargo = tk.StringVar()
        self.dest = tk.StringVar()
        self.result_error = tk.StringVar()
        self.waybill = None
        self.controller = controller
        frame1 = tk.Frame(self)
        frame1.pack(fill=tk.X, )
        # label
        tn_label = tk.Label(frame1, text=arabic('رقم الشاحنة'), font='Arial 25')
        tn_label.pack()

        # tn input
        tn_input = tk.Entry(frame1, textvariable=self.tn, font='Arial 30', justify='right')
        tn_input.focus()
        tn_input.pack(pady=10)

        # button
        tn_search = tk.Button(frame1, text=arabic('بحث'), font='Arial 25', command=self.search_in_tn, bg='#97c666', fg='#fff')
        tn_search.pack()

        # error frame
        error_label = tk.Label(frame1, textvariable=self.error_value, fg='#aa2a2a', font=' Arial 25')
        error_label.pack(pady=5)

        # loading indicator
        loading_frame = tk.Frame(frame1)
        loading_frame.pack(side=tk.TOP)
        self.loadingBar = ttk.Progressbar(frame1, orient='horizontal', length=200)

        # result frame
        self.frame2 = tk.Frame(frame1)
        # label
        trn_label = tk.Label(self.frame2, text=arabic('رقم المقطورة'), font='Arial 25')
        trn_label.pack()

        # trn input
        trn_input = tk.Entry(self.frame2, textvariable=self.trn, font='Arial 30', justify='right')
        trn_input.pack(pady=10)
        # label
        nn_label = tk.Label(self.frame2, text=arabic('الرقم الوطني'), font='Arial 25')
        nn_label.pack()

        # nn input
        nn_input = tk.Entry(self.frame2, textvariable=self.nn, font='Arial 30', justify='right')
        nn_input.pack(pady=10)

        # change nn button
        nn_search = tk.Button(self.frame2,
                              text=arabic('نغيير الرقم الوطني'),
                              font='Arial 20',
                              command=self.search_in_nn,
                              bg='#97c666',
                              fg='#fff')
        nn_search.pack()

        # error frame
        nn_error_label = tk.Label(self.frame2, textvariable=self.nn_error_value, fg='#aa2a2a', font=' Arial 25')
        nn_error_label.pack(pady=10)

        # label
        name_frame = tk.Frame(self.frame2)
        name_frame.pack()
        name_label = tk.Label(name_frame, text=arabic('السائق :'), font='Arial 25')
        name_label.pack(side=tk.RIGHT, padx=3)
        name_value = tk.Label(name_frame, textvariable=self.name, font='Arial 25', fg=minagateTheme['SECONDARY'])
        name_value.pack(side=tk.RIGHT)

        # label
        cargo_frame = tk.Frame(self.frame2)
        cargo_frame.pack(pady=35)
        cargo_label = tk.Label(cargo_frame, text=arabic('الحمولة :'), font='Arial 25')
        cargo_label.pack(side=tk.RIGHT, padx=3)
        cargo_value = tk.Label(cargo_frame, textvariable=self.cargo, font='Arial 25', fg=minagateTheme['SECONDARY'])
        cargo_value.pack(side=tk.RIGHT)

        # label
        dest_frame = tk.Frame(self.frame2)
        dest_frame.pack()
        dest_label = tk.Label(dest_frame, text=arabic('الوجهة :'), font='Arial 25')
        dest_label.pack(side=tk.RIGHT, padx=3)
        dest_value = tk.Label(dest_frame, textvariable=self.dest, font='Arial 25', fg=minagateTheme['SECONDARY'])
        dest_value.pack(side=tk.RIGHT)

        # resutl error
        result_error_label = tk.Label(self.frame2, textvariable=self.result_error, fg='#aa2a2a', font=' Arial 25')
        result_error_label.pack(pady=10)

        # button
        save_button = tk.Button(self.frame2,
                                text=arabic('حفظ وطباعة'),
                                font='Arial 25',
                                command=self.submit,
                                bg='#97c666',
                                fg='#fff')
        save_button.pack()

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
                self.nn_error_value.set('')
                self.trn.set(result['trn'])
                self.nn.set(result['driver_nn'])
                self.cargo.set(arabic(result["cargo_name"]))
                self.dest.set(arabic(result['destination_name']))
                self.name.set(arabic(result['driver_name']))
                self.waybill = result
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
            if not result.get('name'):
                self.nn_error_value.set(arabic('الرقم الوطني غير صحيح'))
            else:
                self.nn_error_value.set('')
                self.name.set(arabic(result['name']))
        except (ValueError, SyntaxError):
            self.nn_error_value.set(arabic('الرجاء ادخال رقم وطني صحيح'))
            self.loadingBar.pack_forget()

    # save result to system
    def save_result(self):
        if self.nn_error_value.get():
            self.loadingBar.pack_forget()
            return

        if self.waybill['type'] == 'WAYBILL_ORDER':
            waybill_order_id = self.waybill['waybill_order_id']
            try:
                result = Api(
                    path='waybill_order',
                    method='closeWaybillOrderByTerminal',
                    params={'waybill_order_id': waybill_order_id,
                            'driver_nn': self.nn.get(),
                            'trn': self.trn.get()}).get()
                print(result)
                # if there is error
                self.loadingBar.pack_forget()
                if not result:
                    self.nn_error_value.set(arabic('الرقم الوطني غير صحيح'))
                else:
                    self.controller.show_frame('1')
                    self.reser_form()
                    time.sleep(1.5)
                    self.controller.show_frame('0')
            except:
                self.result_error.set(arabic('حدث خطأ ما, الرجاء اعادة المحاولة'))
                self.loadingBar.pack_forget()
        elif self.waybill['type'] == 'WAYBILL':
            waybill_id = self.waybill['waybill_id']
            try:
                result = Api(
                    path='waybill',
                    method='activateWaybillByTerminal',
                    params={'waybill_id': waybill_id,
                            'driver_nn': self.nn.get(),
                            'trn': self.trn.get()}).get()
                print(result)
                # if there is error
                self.loadingBar.pack_forget()
                if result.get('ERRORCODE') and result['ERRORCODE'] == 500:
                    self.result_error.set(arabic(result['CODE']))
                else:
                    self.controller.show_frame('1')
                    self.reser_form()
                    time.sleep(1.5)
                    self.controller.show_frame('0')
            except:
                self.result_error.set(arabic('حدث خطأ ما, الرجاء اعادة المحاولة'))
                self.loadingBar.pack_forget()

    # for loading indicator only
    def loading(self):
        self.loadingBar.pack()
        self.loadingBar.start(interval=11)

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

    def submit(self):
        x0 = threading.Thread(target=self.loading)
        x0.start()
        x1 = threading.Thread(target=self.save_result)
        x1.start()

    def reser_form(self):
        self.tn.set('')
        self.error_value.set('')
        self.trn.set('')
        self.nn.set('')
        self.nn_error_value.set('')
        self.name.set('')
        self.cargo.set('')
        self.dest.set('')
        self.result_error.set('')
        self.frame2.pack_forget()
        self.waybill = None

