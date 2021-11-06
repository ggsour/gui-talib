
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from interface.process_data_widget import DataProcessingFrame


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('GUI-TAlib')
        self.style = Style('pulse')
        self.cleaner = Sour(self)
        self.cleaner.pack(fill='both', expand=True)

        # custom styles
        self.style.configure('header.TLabel', background=self.style.colors.secondary, foreground=self.style.colors.info)

        # do not allow window resizing
        self.resizable(False, False)


class Sour(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        action_frame = ttk.Frame(self)
        action_frame.grid(row=0, column=0, sticky='nsew')
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=1, sticky='nsew', pady=(25, 0))
        self.process_data()

        # results frame
        results_frame = ttk.Frame(self)
        results_frame.grid(row=0, column=2, sticky='nsew')

        ## result cards
        cards_frame = ttk.Frame(results_frame, name='cards-frame', style='secondary.TFrame')
        cards_frame.pack(fill='both', expand='yes')

    def process_data(self):
        for child in self.notebook.winfo_children():
            child.destroy()
        # form variables
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=1, sticky='nsew', pady=(25, 0))
        x = DataProcessingFrame(self.notebook)
        x.pack(fill='both', expand='yes')


if __name__ == '__main__':
    Application().mainloop()
