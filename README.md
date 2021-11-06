# gui-Talib

Unofficial Simple tool/frontend for [TA-lib ](https://github.com/mrjbq7/ta-lib) made with python3 and [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap/tree/0.5).
for financial technical analysis.

# Dependencies
TA-Lib
pandas
numpy
matplotlib
ttkbootstrap
TA-lib
First install the TA-lib binary for your OS following the [installation Guide](https://mrjbq7.github.io/ta-lib/install.html)

Then install de the packages from requirements.txt with.(replace $path with yours)  
```
pip3 install -r /$path/requirements.txt

```
# Usage
For more information about Functions and parameters please refer to [Ta-lib documentation](https://mrjbq7.github.io/ta-lib/doc_index.html)
1) launch with
```
~/python3 gui-talib.py

```
2) Open a csv file with OHLCV columns, For now only .csv files ar supported

![1](/docs/images/1.png)

3) Choose one of TA-lib's functions, in this example i will use the moving average(MA)

![2](/docs/images/2.png)

4) Modify the parameters or leave it empty to use defaults.

![3](/docs/images/3.png)

5) Visualize or append directly to the file as a new column.