import tkinter
from tkinter import ttk
from functools import partial
import pandas as pd
from talib import abstract
from utils import data, plot


class AbstractIndicators:
    def __init__(self, name=None, params=None, inputs=None):
        self.name = name
        self.params = params
        self.inputs = inputs
        self.defaults = {}
        self.info = self.get_info()
        self.output_names = self.info['output_names']

    def get_info(self):
        print(self.name)
        return abstract.Function(self.name, None).info

    def get_params(self):
        pp = {}
        defaults = self.info['parameters']
        for p in defaults:
            pp[f'{p}'] = tkinter.StringVar()

            if p == 'nbdevup':
                self.defaults[f'{p}'] = float(defaults[f'{p}'])
            elif p == 'nbdevdn':
                self.defaults[f'{p}'] = float(defaults[f'{p}'])
            elif p == 'penetration':
                self.defaults[f'{p}'] = float(defaults[f'{p}'])

            elif p == 'nbdev':
                self.defaults[f'{p}'] = float(defaults[f'{p}'])
            else:
                self.defaults[f'{p}'] = int(defaults[f'{p}'])

        self.params = self.defaults
        return pp

    def get_indicator(self):
        inputs = self.inputs
        indicator = abstract.Function(self.name, inputs)
        if self.params:
            print(self.params)
            indicator.parameters = self.params
        print(f'{self.name}')
        return indicator()


class IndicatorsUI(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.current_row = 2
        self.fast_period = tkinter.StringVar()
        self.slow_period = tkinter.StringVar()
        self.plot_btn = None
        self.save_btn = None

    def ui_label(self, indicator_name, ):
        ttk.Label(self.master, text=f'{indicator_name}').grid(row=self.current_row, column=0, columnspan=1, pady=10)
        self.current_row += 1

    def label_entry(self, text, variable):
        ttk.Label(self.master, text=f'{text}:').grid(row=self.current_row, column=0, columnspan=1, pady=10)
        period_box = ttk.Entry(self.master, style='info.TEntry', textvariable=variable)
        period_box.grid(row=self.current_row, column=1, columnspan=1, pady=10)
        self.current_row += 1

    def plot_button(self):
        self.plot_btn = ttk.Button(self.master, text='Show plot', style='info.TButton')
        self.plot_btn.grid(row=self.current_row, column=1, columnspan=1, pady=10)

    def save_button(self):
        self.save_btn = ttk.Button(self.master, text='Add to file', style='danger.TButton')
        self.save_btn.grid(row=self.current_row, column=2, columnspan=1, pady=10)


class NewInterface(ttk.Frame):
    def __init__(self,
                 master=None,
                 response_type=None,
                 file_path=None,
                 selected=None):
        super().__init__(master=master)
        self.file_path = file_path
        self.type = response_type
        self.ui = IndicatorsUI(master=self.master)
        self.df, self.inputs = data.load(file_path=self.file_path)
        self.selected = selected
        self.params = {}
        self.ui = IndicatorsUI(master=master)
        self.ui.ui_label(self.selected)
        self.abstract = AbstractIndicators(name=self.selected.lower(), inputs=self.inputs)
        self.var_params = self.get_params()
        self.draw_params()
        self.ui.plot_button()
        self.ui.plot_btn.configure(command=partial(self.action, ploter=True))
        self.ui.save_button()
        self.ui.save_btn.configure(command=partial(self.action, save=True))

    def action(self, ploter=False, save=False):
        self.get_updated_params()
        self.abstract.params = self.params
        self.get_tata(ploter, save)

    def get_params(self):
        return self.abstract.get_params()

    def get_updated_params(self):
        for k, v in self.var_params.items():
            if k == 'nbdevup':
                self.params[k] = float(v.get()) if v.get() != '' else self.abstract.defaults[k]
            elif k == 'nbdevdn':
                self.params[k] = float(v.get()) if v.get() != '' else self.abstract.defaults[k]
            elif k == 'penetration':
                self.params[k] = float(v.get()) if v.get() != '' else self.abstract.defaults[k]

            elif k == 'nbdev':
                self.params[k] = float(v.get()) if v.get() != '' else self.abstract.defaults[k]
            else:
                self.params[k] = int(v.get()) if v.get() != '' else self.abstract.defaults[k]

    def draw_params(self):

        if self.var_params is not None:
            for k, v in self.var_params.items():
                self.ui.label_entry(f'{k}', v)

    def get_tata(self, ploter=False, save=False):
        o = self.abstract.output_names
        dataframe = []
        labels = ''.join(f'-{value}' for _, value in self.params.items())
        output = [self.abstract.get_indicator()]

        if len(o) > 1:
            for i, v in enumerate(o):
                print(pd.DataFrame({f'{v}{labels}': output[0][i]}))
                dataframe.append(pd.DataFrame({f'{v}{labels}': output[0][i]}))
        else:
            for r, n in zip(output, o):
                print(pd.DataFrame({f'{self.selected.lower()}{labels}': r}))
                dataframe.append(pd.DataFrame({f'{self.selected.lower()}{labels}': r}))
        result = pd.concat(dataframe, axis=1)
        print(result)
        if ploter:
            plot.plot_data(data=result, price=self.df['Close'])
        if save:
            data.save(file_path=self.file_path, data=result)


class TaFunctions(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.overlap = [
            {'id': 'BBANDS', 'name': 'Bollinger Bands'},
            {'id': 'DEMA', 'name': 'Double Exponential Moving Average'},
            {'id': 'EMA', 'name': 'Exponential Moving Average'},
            {'id': 'HT_TRENDLINE', 'name': 'Hilbert Transform - Instantaneous Trendline'},
            {'id': 'KAMA', 'name': 'Kaufman Adaptive Moving Average'},
            {'id': 'MA', 'name': 'Moving average'},
            {'id': 'MAMA', 'name': 'MESA Adaptive Moving Average'},
            {'id': 'MAVP', 'name': 'Moving average with variable period'},
            {'id': 'MIDPOINT', 'name': ' MidPoint over period'},
            {'id': 'MIDPRICE', 'name': 'Midpoint Price over period'},
            {'id': 'SAR', 'name': 'Parabolic SAR'},
            {'id': 'SAREXT', 'name': 'Parabolic SAR - Extended'},
            {'id': 'SMA', 'name': 'Simple Moving Average'},
            {'id': 'T3', 'name': 'Triple Exponential Moving Average (T3)'},
            {'id': 'TEMA', 'name': 'Triple Exponential Moving Average'},
            {'id': 'TRIMA', 'name': 'Triangular Moving Average'},
            {'id': 'WMA', 'name': 'Weighted Moving Average'}
        ]
        self.momentum = [
            {'id': 'ADX', 'name': 'Average Directional Movement Index'},
            {'id': 'ADXR', 'name': 'Average Directional Movement Index Rating'},
            {'id': 'APO', 'name': 'Absolute Price Oscillator'},
            {'id': 'AROON', 'name': 'Aroon'},
            {'id': 'AROONOSC', 'name': 'Aroon Oscillator'},
            {'id': 'BOP', 'name': 'Balance Of Power'},
            {'id': 'CCI', 'name': ' Commodity Channel Index'},
            {'id': 'CMO', 'name': 'Chande Momentum Oscillator'},
            {'id': 'DX', 'name': 'Directional Movement Index'},
            {'id': 'MACD', 'name': 'Moving Average Convergence/Divergence'},
            {'id': 'MACDEXT', 'name': 'MACD with controllable MA type'},
            {'id': 'MACDFIX', 'name': 'Moving Average Convergence/Divergence Fix 12/26'},
            {'id': 'MFI', 'name': 'Money Flow Index'},
            {'id': 'MINUS_DI', 'name': 'Minus Directional Indicator'},
            {'id': 'MINUS_DM', 'name': ' Minus Directional Movement'},
            {'id': 'MOM', 'name': 'Momentum'},
            {'id': 'PLUS_DI', 'name': 'Plus Directional Indicator'},
            {'id': 'PLUS_DM', 'name': 'Plus Directional Movement'},
            {'id': 'PPO', 'name': 'Percentage Price Oscillator'},
            {'id': 'ROC', 'name': 'Rate of change : ((price/prevPrice)-1)*100'},
            {'id': 'ROCP', 'name': 'Rate of change Percentage: (price-prevPrice)/prevPrice'},
            {'id': 'ROCR', 'name': 'Rate of change ratio: (price/prevPrice)'},
            {'id': 'ROCR100', 'name': 'Rate of change ratio 100 scale: (price/prevPrice)*100'},
            {'id': 'RSI', 'name': 'Relative Strength Index'},
            {'id': 'STOCH', 'name': 'Stochastic'},
            {'id': 'STOCHF', 'name': 'Stochastic Fast'},
            {'id': 'STOCHRSI', 'name': ' Stochastic Relative Strength Index'},
            {'id': 'TRIX', 'name': '1-day Rate-Of-Change (ROC) of a Triple Smooth EMA'},
            {'id': 'ULTOSC', 'name': ' Ultimate Oscillator'},
            {'id': 'WILLR', 'name': 'WILLR'}
        ]
        self.volume = [
            {'id': 'AD', 'name': 'Chaikin A/D Line'},
            {'id': 'ADOSC', 'name': 'Chaikin A/D Oscillator'},
            {'id': 'OBV', 'name': ' On Balance Volume'}
        ]
        self.volatility = [
            {'id': 'ATR', 'name': 'Average True Range'},
            {'id': 'NATR', 'name': 'Normalized Average True Range'},
            {'id': 'TRANGE', 'name': 'True Range'}

        ]
        self.statistics = [
            {'id': 'BETA', 'name': 'Beta'},
            {'id': 'CORREL', 'name': 'Pearsons Correlation Coefficient (r)'},
            {'id': 'LINEARREG', 'name': 'Linear Regression'},
            {'id': 'LINEARREG_ANGLE', 'name': 'Linear Regression Angle'},
            {'id': 'LINEARREG_INTERCEPT', 'name': 'Linear Regression Intercept'},
            {'id': 'LINEARREG_SLOPE', 'name': 'Linear Regression Slope'},
            {'id': 'STDDEV', 'name': 'Standard Deviation'},
            {'id': 'TSF', 'name': 'Time Series Forecast'},
            {'id': 'VAR', 'name': 'Variance'}

        ]
        self.price = [
            {'id': 'AVGPRICE', 'name': 'Average Price'},
            {'id': 'MEDPRICE', 'name': 'Median Price'},
            {'id': 'TYPPRICE', 'name': 'Typical Price'},
            {'id': 'WCLPRICE', 'name': 'Weighted Close Price'}

        ]
        self.cycle = [
            {'id': 'HT_DCPERIOD', 'name': 'Hilbert Transform - Dominant Cycle Period'},
            {'id': 'HT_DCPHASE', 'name': 'Hilbert Transform - Dominant Cycle Phase'},
            {'id': 'HT_PHASOR', 'name': 'Hilbert Transform - Phasor Components'},
            {'id': 'HT_SINE', 'name': 'Hilbert Transform - SineWave'},
            {'id': 'HT_TRENDMODE', 'name': 'Hilbert Transform - Trend vs Cycle Mode'}

        ]
        self.patterns = [

            {'id': 'CDL2CROWS', 'name': 'Two Crows'},
            {'id': 'CDL3BLACKCROWS', 'name': 'Three Black Crows'},
            {'id': 'CDL3INSIDE', 'name': 'Three Inside Up/Down'},
            {'id': 'CDL3LINESTRIKE', 'name': 'Three-Line Strike'},
            {'id': 'CDL3OUTSIDE', 'name': 'Three Outside Up/Down'},
            {'id': 'CDL3STARSINSOUTH', 'name': 'Three Stars In The South'},
            {'id': 'CDL3WHITESOLDIERS', 'name': 'Three Advancing White Soldiers'},
            {'id': 'CDLABANDONEDBABY', 'name': 'Abandoned Baby'},
            {'id': 'CDLADVANCEBLOCK', 'name': 'Advance Block'},
            {'id': 'CDLBELTHOLD', 'name': 'Belt-hold'},
            {'id': 'CDLBREAKAWAY', 'name': 'Breakaway'},
            {'id': 'CDLCLOSINGMARUBOZU', 'name': 'Closing Marubozu'},
            {'id': 'CDLCONCEALBABYSWALL', 'name': 'Concealing Baby Swallow'},
            {'id': 'CDLCOUNTERATTACK', 'name': 'Counterattack'},
            {'id': 'CDLDARKCLOUDCOVER', 'name': 'Dark Cloud Cover'},
            {'id': 'CDLDOJI', 'name': 'Doji'},
            {'id': 'CDLDOJISTAR', 'name': 'Doji Star'},
            {'id': 'CDLDRAGONFLYDOJI', 'name': 'Dragonfly Doji'},
            {'id': 'CDLENGULFING', 'name': 'Engulfing Pattern'},
            {'id': 'CDLEVENINGDOJISTAR', 'name': 'Evening Doji Star'},
            {'id': 'CDLEVENINGSTAR', 'name': 'Evening Star'},
            {'id': 'CDLGAPSIDESIDEWHITE', 'name': 'Up/Down-gap side-by-side white lines'},
            {'id': 'CDLGRAVESTONEDOJI', 'name': 'Gravestone Doji'},
            {'id': 'CDLHAMMER', 'name': 'Hammer'},
            {'id': 'CDLHANGINGMAN', 'name': 'Hanging Man'},
            {'id': 'CDLHARAMI', 'name': 'Harami Pattern'},
            {'id': 'CDLHARAMICROSS', 'name': 'Harami Cross Pattern'},
            {'id': 'CDLHIGHWAVE', 'name': 'High-Wave Candle'},
            {'id': 'CDLHIKKAKE', 'name': 'Hikkake Pattern'},
            {'id': 'CDLHIKKAKEMOD', 'name': 'Modified Hikkake Pattern'},
            {'id': 'CDLHOMINGPIGEON', 'name': 'Homing Pigeon'},
            {'id': 'CDLIDENTICAL3CROWS', 'name': 'Identical Three Crows'},
            {'id': 'CDLINNECK', 'name': ' In-Neck Pattern'},
            {'id': 'CDLINVERTEDHAMMER', 'name': 'Inverted Hammer'},
            {'id': 'CDLKICKING', 'name': 'Kicking'},
            {'id': 'CDLKICKINGBYLENGTH', 'name': 'Kicking - bull/bear determined by the longer marubozu'},
            {'id': 'CDLLADDERBOTTOM', 'name': 'Ladder Bottom'},
            {'id': 'CDLLONGLEGGEDDOJI', 'name': ' Long Legged Doji'},
            {'id': 'CDLLONGLINE', 'name': 'Long Line Candle'},
            {'id': 'CDLMARUBOZU', 'name': 'Marubozu'},
            {'id': 'CDLMATCHINGLOW', 'name': 'Matching Low'},
            {'id': 'CDLMATHOLD', 'name': 'Mat Hold'},
            {'id': 'CDLMORNINGDOJISTAR', 'name': 'Morning Doji Star'},
            {'id': 'CDLMORNINGSTAR', 'name': 'Morning Star'},
            {'id': 'CDLONNECK', 'name': 'On-Neck Pattern'},
            {'id': 'CDLPIERCING', 'name': 'Piercing Pattern'},
            {'id': 'CDLRICKSHAWMAN', 'name': ' Rickshaw Man'},
            {'id': 'CDLRISEFALL3METHODS', 'name': 'Rising/Falling Three Methods'},
            {'id': 'CDLSEPARATINGLINES', 'name': 'Separating Lines'},
            {'id': 'CDLSHOOTINGSTAR', 'name': 'Shooting Star'},
            {'id': 'CDLSHORTLINE', 'name': 'Short Line Candle'},
            {'id': 'CDLSPINNINGTOP', 'name': 'Spinning Top'},
            {'id': 'CDLSTALLEDPATTERN', 'name': 'Stalled Pattern'},
            {'id': 'CDLSTICKSANDWICH', 'name': 'Stick Sandwich'},
            {'id': 'CDLTAKURI', 'name': 'Takuri (Dragonfly Doji with very long lower shadow)'},
            {'id': 'CDLTASUKIGAP', 'name': 'Tasuki Gap'},
            {'id': 'CDLTHRUSTING', 'name': 'Thrusting Pattern'},
            {'id': 'CDLTRISTAR', 'name': 'Tristar Pattern'},
            {'id': 'CDLUNIQUE3RIVER', 'name': 'Unique 3 River'},
            {'id': 'CDLUPSIDEGAP2CROWS', 'name': ' Upside Gap Two Crows'},
            {'id': 'CDLXSIDEGAP3METHODS', 'name': 'Upside/Downside Gap Three Methods'}
        ]
        self.math_operators = [
            {'id': 'ADD', 'name': 'Vector Arithmetic Add'},
            {'id': 'DIV', 'name': ' Vector Arithmetic Div'},
            {'id': 'MAX', 'name': 'Highest value over a specified period'},
            {'id': 'MAXINDEX', 'name': 'Index of highest value over a specified period'},
            {'id': 'MIN', 'name': 'Lowest value over a specified period'},
            {'id': 'MININDEX', 'name': 'Index of lowest value over a specified period'},
            {'id': 'MINMAX', 'name': 'Lowest and highest values over a specified period'},
            {'id': 'MINMAXINDEX', 'name': 'Indexes of lowest and highest values over a specified period'},
            {'id': 'MULT', 'name': 'Vector Arithmetic Mult'},
            {'id': 'SUB', 'name': 'Vector Arithmetic Substraction'},
            {'id': 'SUM', 'name': 'Summation'}

        ]

        self.math_transforms = [
            {'id': 'ACOS', 'name': 'Vector Trigonometric ACos'},
            {'id': 'ASIN', 'name': 'Vector Trigonometric ASin'},
            {'id': 'ATAN', 'name': 'Vector Trigonometric ATan'},
            {'id': 'CEIL', 'name': 'Vector Ceil'},
            {'id': 'COS', 'name': 'Vector Trigonometric Cos'},
            {'id': 'COSH', 'name': 'Vector Trigonometric Cosh'},
            {'id': 'EXP', 'name': 'Vector Arithmetic Exp'},
            {'id': 'FLOOR', 'name': 'Vector Floor'},
            {'id': 'LN', 'name': 'Vector Log Natural'},
            {'id': 'LOG10', 'name': 'Vector Log10'},
            {'id': 'SIN', 'name': 'Vector Trigonometric Sin'},
            {'id': 'SINH', 'name': 'Vector Trigonometric Sinh'},
            {'id': 'SQRT', 'name': ' Vector Square Root'},
            {'id': 'TAN', 'name': 'Vector Trigonometric Tan'},
            {'id': 'TANH', 'name': 'Vector Trigonometric Tanh'}

        ]
    def check(self, file_path, selected):
        NewInterface(master=self, file_path=file_path, selected=selected)
