import pandas as pd
import numpy as np


def normalize_csv(path):
    df = pd.read_csv(path)
    df_pre = df.select_dtypes(include=['float64', 'int64'])
    df_pre = df_pre.drop(columns=['material ID', 'category', 'hierarchy category', 'level'])
    df_norm = df_pre.apply(
        lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)) if (np.max(x) - np.min(x)) != 0 else 0)
    df_head = list(df_norm.columns)
    df[df_head] = df_norm
    df.to_csv(path_or_buf='../csvData/raw/pistonsNormal.csv', sep=",", index=False)


if __name__ == "__main__":
    PATH = '../csvData/raw/pistons.csv'
    normalize_csv(PATH)
