import matplotlib.pyplot as plt
import pandas as pd


def plot_data(data, price = None):
    result = data
    plt.close()

    if not price.empty:
        #result = pd.concat([
         #   pd.DataFrame({'Close': price}),
         #   result], axis=1)
        plt.subplot(2,1,1)
        plt.plot(price)
    plt.subplot(2,1,2)
    plt.plot(result)
    plt.legend(result)
    plt.show()

