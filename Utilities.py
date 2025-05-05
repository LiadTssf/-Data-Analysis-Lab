from Contants import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def format_k_m(x, pos):
    if x >= 1_000_000_000:
        return f'{int(x/1_000_000_000)}B'
    if x >= 1_000_000:
        return f'{int(x/1_000_000)}M'
    elif x >= 1_000:
        return f'{int(x/1_000)}K'
    else:
        return f'{int(x)}'

def compute_cumulative(df):
    df = df.copy()
    df['date_range'] = df.apply(lambda row: pd.date_range(row[INWARD_DATE_COL], row[DISPATCH_DATE_COL], freq='D'), axis=1)
    df = df.explode('date_range')
    df['daily_quantity'] = df[QUANTITY_COL]  / (df[DISPATCH_DATE_COL] - df[INWARD_DATE_COL]).dt.days.add(1)
    df['daily_profit'] = (df[QUANTITY_COL] * df[PRICE_COL]) / (df[DISPATCH_DATE_COL] - df[INWARD_DATE_COL]).dt.days.add(1)
    daily_quantity = df.groupby('date_range')['daily_quantity'].sum().sort_index()
    daily_profit = df.groupby('date_range')['daily_profit'].sum().sort_index()
    cumulative_quantity = daily_quantity.cumsum()
    cumulative_profit = daily_profit.cumsum()
    return cumulative_quantity, cumulative_profit


def plot_heatmap(df, col, title, save):
    matrix = df.groupby(['Region', col])[QUANTITY_COL].sum().unstack().fillna(0)
    normalized = matrix.div(matrix.sum(axis=1), axis=0) * 100

    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(
        normalized,
        annot=normalized,
        fmt='.1f',
        cmap='Blues',
        cbar_kws={'label': 'Normalized % of Max'}
    )
    plt.title(title)
    plt.xlabel(col)
    plt.ylabel('Region')
    plt.tight_layout()
    plt.savefig(save)
    plt.close()