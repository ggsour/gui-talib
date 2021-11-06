# gui-Talib

Unofficial Simple tool/frontend for [TA-lib ](https://github.com/mrjbq7/ta-lib) made with python3 and [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap/tree/0.5).

# Dependencies
TA-Lib
pandas
numpy
matplotlib
ttkbootstrap

Install de the packages from requirements.txt with.(replace $path with yours)  
```
pip install -r /$path/requirements.txt

```
# Usage

1) launch with
```
~/python3 gui-talib.py

```
2) Open a csv file with OHLCV columns, For now only .csv files ar supported

![1](https://github.com/enedsour/gui-talib/tree/master/docs/images/1.png)

3) Choose one of TA-lib's functions, in this example i will use the moving average(MA)

![2](https://github.com/enedsour/gui-talib/tree/master/docs/images/2.png)

4) Modify the parameters or leave it empty to use defaults.

![3](https://github.com/enedsour/gui-talib/tree/master/docs/images/3.png)
5) Visualize or append directly to the file as a new column.