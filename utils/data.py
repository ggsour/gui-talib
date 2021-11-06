import pandas as pd


def save(file_path, data):
    df = pd.read_csv(file_path)
    to_combine = [df, data]
    combined = pd.concat(to_combine, axis=1)
    combined.to_csv(file_path, index=False, mode='w', header=True)


def load(file_path):
    df = pd.read_csv(file_path)
    inputs = {
        'open': df['Open'].to_numpy(),
        'high': df['High'].to_numpy(),
        'low': df['Low'].to_numpy(),
        'close': df['Close'].to_numpy(),
        'volume': df['Volume'].to_numpy()
    }
    return df, inputs
