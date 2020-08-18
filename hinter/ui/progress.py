from tkinter import *
from tkinter.ttk import *


class Progress:
    popup: Toplevel = None
    bar: Progressbar = None
    current_percentage: int = 0
    status_text: Label = None

    def __init__(self, percentage: int, current_status: str):
        # Make sure percentage is 1-100
        if not 0 <= percentage <= 100:
            print('hinter.ui.Progress: progress percentage not usable')
            return

        self.current_percentage = percentage
        self.popup = Toplevel()

        Label(self.popup, text='Downloading Game data ...').grid(row=0, column=0, padx=20)
        self.status_text = Label(self.popup, text=current_status)
        self.status_text.grid(row=3, column=0, padx=20)

        self.bar = Progressbar(self.popup, orient=HORIZONTAL, length=100, mode='determinate')
        self.bar['value'] = self.current_percentage
        self.bar.grid(row=2, column=0)

    def update(self, percentage: int, current_status: str):
        # Make sure percentage is 1-100
        if not 0 <= percentage <= 100:
            print('hinter.ui.Progress.update: progress percentage not usable')
            return

        self.current_percentage = percentage
        self.status_text.config(text=current_status)
        self.bar['value'] = self.current_percentage

        self.bar.grid(row=2, column=0)
        self.status_text.grid(row=3, column=0, padx=20)
