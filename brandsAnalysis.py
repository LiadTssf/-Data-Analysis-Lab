from statistics import quantiles

from Utilities import *
from Contants import *
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
def analyze_brands_sales(base_df):
    brands = {name: brands for name, brands in base_df.groupby(BRAND_COL)}
    quantiles = dict()
    sales = dict()
    for brand, df in brands.items():
        df = df.copy()
        quantiles[brand], sales[brand] = compute_cumulative(df)

    for brand, df in quantiles.items():

        # Pivot to heatmap shape (1 row: brand, many cols: dates)
        heatmap_data = df.pivot_table(index=pd.Index([brand]), columns='date_range', values='daily_quantity', fill_value=0)

        # Plot heatmap with matplotlib
        fig, ax = plt.subplots(figsize=(12, 2))  # 1 row per brand
        cax = ax.imshow(heatmap_data.values, aspect='auto', cmap='YlGnBu')

        ax.set_title(f"Sales Heatmap – {brand}")
        ax.set_yticks([0])
        ax.set_yticklabels([brand])
        ax.set_xticks(np.arange(len(heatmap_data.columns)))
        ax.set_xticklabels(heatmap_data.columns.strftime('%m-%Y'), rotation=45, ha='right')

        fig.colorbar(cax, ax=ax, label='Sales')
        plt.tight_layout()
        plt.show()
