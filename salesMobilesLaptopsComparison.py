from Contants import  *
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Utilities import *
import matplotlib.ticker as ticker
import numpy as np
def analyze_mobile_laptop_sales(mobiles_df, laptops_df):
    mobiles_cumulative_quantity, mobiles_cumulative_profit = compute_cumulative(mobiles_df)
    laptops_cumulative_quantity, laptops_cumulative_profit = compute_cumulative(laptops_df)
    plt.figure(figsize=(15, 5))
    mobiles_cumulative_quantity.plot(label='Mobiles')
    laptops_cumulative_quantity.plot(label='Laptops')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Quantity Sold')
    plt.title('Cumulative Sold Pieces Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # Show every month
    plt.xticks(rotation=30)  # Optional: rotate for readability
    plt.ticklabel_format(style='plain', axis='y')
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(format_k_m))
    plt.savefig("Output_Graphs/1Cumulative_Sold_Pieces_Over_Time.png")

    diff = mobiles_cumulative_quantity - laptops_cumulative_quantity
    pos_diff = diff.where(diff >= 0, 0).abs()
    neg_diff = diff.where(diff < 0, 0).abs()
    plt.figure(figsize=(12, 6))
    plt.fill_between(diff.index, 0, pos_diff.values, label='Mobiles Sales Greater Than Laptops', color='green', alpha=0.2)
    plt.fill_between(diff.index, 0, neg_diff.values, label='Laptops Sales Greater Than Mobiles', color='blue', alpha=0.2)
    plt.title("Absolute Difference in Cumulative Sold Pieces")
    plt.xlabel("Date")
    plt.ylabel("Absolute Difference in Quantity")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.ticklabel_format(style='plain', axis='y')
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(format_k_m))
    plt.savefig("Output_Graphs/2Absolute_Difference_in_Cumulative_Sold_Pieces.png")


    plt.figure(figsize=(14, 6), constrained_layout=True)
    mobiles_cumulative_profit.plot(label='Mobiles')
    laptops_cumulative_profit.plot(label='Laptops')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Financial Profit')
    plt.title('Cumulative Financial Profit Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # Show every month
    plt.xticks(rotation=30)  # Optional: rotate for readability
    plt.ticklabel_format(style='plain', axis='y')
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(format_k_m))
    plt.savefig("Output_Graphs/3Cumulative_Financial_Profit_Over_Time.png")

    diff = mobiles_cumulative_profit - laptops_cumulative_profit
    pos_diff = diff.where(diff >= 0, 0).abs()
    neg_diff = diff.where(diff < 0, 0).abs()
    plt.figure(figsize=(16, 6), constrained_layout=True)
    plt.fill_between(diff.index, 0, pos_diff, label='Mobiles Sales Greater Than Laptops', color='green', alpha=0.2)
    plt.fill_between(diff.index, 0, neg_diff, label='Laptops Sales Greater Than Mobiles', color='blue', alpha=0.2)
    plt.title("Absolute Difference in Cumulative Financial Profit")
    plt.xlabel("Date")
    plt.ylabel("Absolute Difference in Quantity")
    plt.yticks(rotation=90)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.ticklabel_format(style='plain', axis='y')
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(format_k_m))
    plt.savefig("Output_Graphs/4Absolute_Difference_in_Cumulative_Financial_Profit.png")


