from statistics import quantiles

from Utilities import *
from Contants import *
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np

def brands_avg_quantity_and_price(base_df):
    # ---------- Group by Brand & Product ----------
    agg_df = base_df.groupby(['Product', 'Brand']).agg({
        'Price': 'mean',
        'Quantity Sold': 'mean'
    }).reset_index()

    # ---------- Separate and Sort ----------
    mobile_df = agg_df[agg_df['Product'] == 'Mobile Phone'].set_index('Brand')
    laptop_df = agg_df[agg_df['Product'] == 'Laptop'].set_index('Brand')

    # Sort by average price
    mobile_sorted = mobile_df.sort_values(by='Price', ascending=False)
    laptop_sorted = laptop_df.sort_values(by='Price', ascending=False)

    mobile_brands = mobile_sorted.index
    laptop_brands = laptop_sorted.index

    # ---------- Plot Mobiles ----------
    x_mob = np.arange(len(mobile_brands))
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(x_mob - 0.15, mobile_sorted['Price'], width=0.8, label='Avg Price')

    ax.set_ylabel('Value')
    ax.set_title('Mobile Phones: Avg Price by Brand')
    ax.set_xticks(x_mob)
    ax.set_xticklabels(mobile_brands, rotation=45)
    ax.yaxis.set_major_locator(plt.MultipleLocator(10000))
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(format_k_m))
    plt.tight_layout()
    plt.savefig("Output_Graphs/5Avg_Price_by_Brand.png")

    # ---------- Plot Laptops ----------
    x_lap = np.arange(len(laptop_brands))
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(x_lap - 0.15, laptop_sorted['Price'], width=0.8, label='Avg Price')

    ax.set_ylabel('Value')
    ax.set_title('Laptops: Avg Price by Brand')
    ax.set_xticks(x_lap)
    ax.set_xticklabels(laptop_brands, rotation=45)
    ax.yaxis.set_major_locator(plt.MultipleLocator(10000))
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(format_k_m))
    plt.tight_layout()
    plt.savefig("Output_Graphs/6Avg_Price_by_Brand.png")



    # Sort by average price
    mobile_sorted = mobile_df.sort_values(by='Quantity Sold', ascending=False)
    laptop_sorted = laptop_df.sort_values(by='Quantity Sold', ascending=False)

    mobile_brands = mobile_sorted.index
    laptop_brands = laptop_sorted.index


    # ---------- Plot Mobiles ----------
    x_mob = np.arange(len(mobile_brands))
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(x_mob + 0.15, mobile_sorted['Quantity Sold'], width=0.8, label='Avg Quantity Sold')

    ax.set_ylabel('Value')
    ax.set_title('Mobile Phones: Avg Quantity Sold by Brand')
    ax.set_xticks(x_mob)
    ax.set_xticklabels(mobile_brands, rotation=45)
    ax.yaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(format_k_m))
    plt.tight_layout()
    plt.savefig("Output_Graphs/7Avg_Quantity_Sold_by_Brand.png")

    # ---------- Plot Laptops ----------
    x_lap = np.arange(len(laptop_brands))
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(x_lap + 0.15, laptop_sorted['Quantity Sold'], width=0.8, label='Avg Quantity Sold')

    ax.set_ylabel('Value')
    ax.set_title('Laptops: Avg Quantity Sold by Brand')
    ax.set_xticks(x_lap)
    ax.set_xticklabels(laptop_brands, rotation=45)
    ax.yaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(format_k_m))
    plt.tight_layout()
    plt.savefig("Output_Graphs/8Avg_Quantity_Sold_by_Brand.png")