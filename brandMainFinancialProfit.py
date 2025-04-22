from statistics import quantiles

from Utilities import *
from Contants import *
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
import os
def getBrandsMainFinancialProfit(base_df):
    # ---------- Group by Brand & Product ----------
    brands_dfs = {brand: df for brand, df in base_df.groupby(BRAND_COL)}
    for brand, df in brands_dfs.items():
        mobiles_cumulative_quantity, mobiles_cumulative_profit = compute_cumulative(df[df[PRODUCT_COL] == 'Mobile Phone'])
        laptops_cumulative_quantity, laptops_cumulative_profit = compute_cumulative(df[df[PRODUCT_COL] == 'Laptop'])
        diff = mobiles_cumulative_quantity - laptops_cumulative_quantity
        pos_diff = diff.where(diff >= 0, 0).abs()
        neg_diff = diff.where(diff < 0, 0).abs()
        plt.figure(figsize=(12, 6))
        plt.fill_between(diff.index, 0, pos_diff.values, label='Mobiles Sales Greater Than Laptops', color='green',
                         alpha=0.2)
        plt.fill_between(diff.index, 0, neg_diff.values, label='Laptops Sales Greater Than Mobiles', color='blue',
                         alpha=0.2)
        plt.title(f"Absolute Difference in Cumulative Sold Pieces for {brand}")
        plt.xlabel("Date")
        plt.ylabel("Absolute Difference in Quantity")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.ticklabel_format(style='plain', axis='y')
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(format_k_m))
        plt.savefig(f"Output_Graphs/Brands_Profitability/{brand}/Absolute_Difference_in_Cumulative_Sold_Pieces_{brand}.png")

        diff = mobiles_cumulative_profit - laptops_cumulative_profit
        pos_diff = diff.where(diff >= 0, 0).abs()
        neg_diff = diff.where(diff < 0, 0).abs()
        plt.figure(figsize=(16, 6), constrained_layout=True)
        plt.fill_between(diff.index, 0, pos_diff, label='Mobiles Sales Greater Than Laptops', color='green', alpha=0.2)
        plt.fill_between(diff.index, 0, neg_diff, label='Laptops Sales Greater Than Mobiles', color='blue', alpha=0.2)
        plt.title(f"Absolute Difference in Cumulative Financial Profit for {brand}")
        plt.xlabel("Date")
        plt.ylabel("Absolute Difference in Quantity")
        plt.yticks(rotation=90)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.ticklabel_format(style='plain', axis='y')
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(format_k_m))
        plt.savefig(f"Output_Graphs/Brands_Profitability/{brand}/Absolute_Difference_in_Cumulative_Financial_Profit_{brand}.png")