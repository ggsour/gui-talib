import pathlib
import tkinter
from functools import partial
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from technical_analisis.functions import TaFunctions


class DataProcessingFrame(ttk.Notebook):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filepath = None
        self.df = None
        self.search_path_var = tkinter.StringVar(value=str(pathlib.Path().absolute()))
        self.option_var = tkinter.StringVar()  # selected indicator
        """Main Tab"""

        ta_tab = ttk.Frame(self, padding=8)
        statistics_math_tab = ttk.Frame(self, padding=8)

        """Sub Tabs"""
        overlap_tab = Subtab_Gui(master=self, action=self.pick_indicator, text='Overlap')
        overlap_tab.category = overlap_tab.statistics_frame.overlap
        overlap_tab.draw()
        momentum_tab = Subtab_Gui(master=self, action=self.pick_indicator, text='Momentum')
        momentum_tab.category = momentum_tab.statistics_frame.momentum
        momentum_tab.draw()
        volume_tab = Subtab_Gui(master=self, action=self.pick_indicator, text='Volume')
        volume_tab.category = volume_tab.statistics_frame.volume
        volume_tab.draw()
        volatility_tab = Subtab_Gui(master=self, action=self.pick_indicator, text='Volatility')
        volatility_tab.category = volatility_tab.statistics_frame.volatility
        volatility_tab.draw()
        price_tab = Subtab_Gui(master=self, action=self.pick_indicator, text='Price')
        price_tab.category = price_tab.statistics_frame.price
        price_tab.draw()
        cycle_tab = Subtab_Gui(master=self, action=self.pick_indicator, text='Cycle')
        cycle_tab.category = cycle_tab.statistics_frame.cycle
        cycle_tab.draw()
        statistics_tab = Subtab_Gui(master=self, action=self.pick_indicator, text='Statistics')
        statistics_tab.category = statistics_tab.statistics_frame.statistics
        statistics_tab.draw()

        patterns_tab = Subtab_Gui(master=self, action=self.pick_indicator, text='Candle patterns')
        patterns_tab.category = patterns_tab.statistics_frame.patterns
        patterns_tab.draw()

        operators_tab = Subtab_Gui(master=self, action=self.pick_indicator, text='Math Operators')
        operators_tab.category = operators_tab.statistics_frame.math_operators
        operators_tab.draw()

        transforms_tab = Subtab_Gui(master=self, action=self.pick_indicator, text='Math Transforms')
        transforms_tab.category = transforms_tab.statistics_frame.math_transforms
        transforms_tab.draw()

        # FILE BROWSER
        input_labelframe = ttk.Labelframe(ta_tab, text='Select file to process', padding=(20, 10, 10, 5))
        input_labelframe.grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        input_labelframe.columnconfigure(0, weight=1)
        ttk.Label(input_labelframe, text='Path').grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        e1 = ttk.Entry(input_labelframe, width=100, textvariable=self.search_path_var)
        e1.grid(row=0, column=1, sticky='ew', padx=10, pady=2)
        b1 = ttk.Button(input_labelframe, text='Browse', command=self.on_browse, style='primary.TButton')
        b1.grid(row=0, column=2, sticky='ew', pady=2, ipadx=10)
        # FILE BROWSER
        input_labelframe = ttk.Labelframe(statistics_math_tab, text='Select file to process', padding=(20, 10, 10, 5))
        input_labelframe.grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        input_labelframe.columnconfigure(0, weight=1)
        ttk.Label(input_labelframe, text='Path').grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        e1 = ttk.Entry(input_labelframe, width=100, textvariable=self.search_path_var)
        e1.grid(row=0, column=1, sticky='ew', padx=10, pady=2)
        b1 = ttk.Button(input_labelframe, text='Browse', command=self.on_browse, style='primary.TButton')
        b1.grid(row=0, column=2, sticky='ew', pady=2, ipadx=10)
        #

        technical_container = ttk.Notebook(ta_tab)
        technical_container.grid(row=1, column=0, columnspan=10, sticky='ew', pady=4)
        technical_container.add(overlap_tab, text='Overlap Functions')
        technical_container.add(momentum_tab, text='Momentum Functions')
        technical_container.add(volume_tab, text='Volume Functions')
        technical_container.add(volatility_tab, text='Volatility Functions')
        technical_container.add(price_tab, text='Price Functions')
        technical_container.add(cycle_tab, text='Cycle Functions')
        technical_container.add(patterns_tab, text='Candle Patterns')
        statistics_container = ttk.Notebook(statistics_math_tab)
        statistics_container.grid(row=1, column=0, columnspan=10, sticky='ew', pady=4)
        statistics_container.add(statistics_tab, text='Statistics Functions')
        statistics_container.add(operators_tab, text='Math Operators')
        statistics_container.add(transforms_tab, text='Math Transforms')

        """Add main tab to root"""
        self.add(ta_tab, text='Technical Analisis')
        self.add(statistics_math_tab, text='Statistics and Math')

    def pick_indicator(self, menu, frame, option):
        self.option_var = option
        print(self.option_var.get())
        menu['text'] = self.option_var.get()
        if self.filepath:
            for widget in frame.winfo_children():
                widget.destroy()
            frame.check(self.filepath, self.option_var.get())

        else:
            print('error:select file first')

    def on_browse(self):
        """Callback for directory browse"""
        path = askopenfilename(title='Directory')
        if path:
            self.search_path_var.set(path)
            self.filepath = path


class Subtab_Gui(ttk.Frame):
    def __init__(self, master, action, text, **kw):
        super().__init__(master, **kw)
        self.text = text
        self.option_var = tkinter.StringVar()  # selected indicator
        self.mb_statistics = ttk.Menubutton(self, text=self.text,
                                            style='info.Outline.TMenubutton')
        self.menu_statistics = tkinter.Menu(self.mb_statistics)
        self.action = action
        # add options
        self.statistics_frame = TaFunctions(master=self)
        self.category = None

    def draw(self):
        for option in self.category:
            self.menu_statistics.add_radiobutton(
                label=option['name'],
                value=option['id'],
                variable=self.option_var,
                command=partial(self.action, self.mb_statistics, self.statistics_frame, self.option_var))

        # associate menu with menubutton
        self.mb_statistics['menu'] = self.menu_statistics
        self.mb_statistics.grid(row=1, column=0, sticky='we', pady=0, padx=(0, 10))

        self.statistics_frame.grid(row=10, column=0, sticky='we', pady=0, padx=(0, 10))
