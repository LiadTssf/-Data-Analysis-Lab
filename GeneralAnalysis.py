import matplotlib.pyplot as plt
from fontTools.ttx import process

from Contants import BRAND_COL, QUANTITY_COL, PRICE_COL, RAM_COL, ROM_COL, COSTOMER_COL, SSD_COL
import pandas as pd
import numpy as np
def general_analysis(mobiles, laptops, base_df):
    getNumericStats(base_df)
    generateStatsGraphs(mobiles, laptops, base_df, BRAND_COL)
    generateStatsGraphs(mobiles, laptops, base_df, RAM_COL)
    generateStatsGraphs(mobiles, laptops, base_df, ROM_COL)
    generateSSDHistogram(laptops)

def generateSSDHistogram(laptops):
    df = laptops[SSD_COL].value_counts().reset_index()
    df = df.sort_values(by=SSD_COL).reset_index(drop=True)
    df.columns = [SSD_COL, 'Count']
    res = df[SSD_COL]
    x = np.arange(len(res))
    width = 0.4

    plt.figure(figsize=(12, 6))
    plt.bar(df.index, df['Count'], width=width, label='Laptops', color='blue', alpha=0.7)
    for i, row in enumerate(df.itertuples()):
        plt.text(x[i], row.Count + 30, f"{int(row.Count)}", ha='center', va='bottom', color='blue', fontsize=10)
    plt.title(f'Transaction Count by {SSD_COL}')
    plt.xlabel(SSD_COL)
    plt.ylabel('Count')
    plt.xticks(x, res, rotation=45)
    plt.legend( loc='lower center')
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"Output_Graphs/General/Transaction Count by {SSD_COL}.png")
    plt.close()

def generateStatsGraphs(mobiles, laptops, base_df, col):
    brand_counts_mobiles = mobiles[col].value_counts().reset_index()
    brand_counts_mobiles.columns = [col, 'Count']

    brand_counts_laptops = laptops[col].value_counts().reset_index()
    brand_counts_laptops.columns = [col, 'Count']
    # Merge them on the brand names to align
    merged = pd.merge(brand_counts_mobiles, brand_counts_laptops, on=col, how='outer',
                      suffixes=('_Mobiles', '_Laptops')).fillna(0)
    res = merged[col]
    x = np.arange(len(res))
    width = 0.4

    plt.figure(figsize=(12, 6))
    plt.bar(x - width / 2, merged['Count_Mobiles'], width=width, label='Mobiles', color='green', alpha=0.7)
    plt.bar(x + width / 2, merged['Count_Laptops'], width=width, label='Laptops', color='blue', alpha=0.7)

    plt.title(f'Transaction Count by {col}')
    plt.xlabel(col)
    plt.ylabel('Count')
    plt.xticks(x, res, rotation=45)
    plt.legend( loc='lower center')
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"Output_Graphs/General/Transaction Count by {col}.png")
    plt.close()


def getNumericStats(base_df):
    working_df = base_df.copy()
    working_df = working_df[[QUANTITY_COL, PRICE_COL, 'Unit_Price']]
    print(working_df.describe())
    print(working_df.var())
    working_df[PRICE_COL].plot(kind='hist', bins=30, density=True, alpha=0.5, label='Histogram')
    working_df[PRICE_COL].plot(kind='kde', label='KDE')
    plt.title('KDE of Price')
    plt.xlabel('Price')
    plt.ylabel('Density')
    plt.grid(True)
    plt.savefig("Output_Graphs/General/Price KDE.png")
    plt.close()
    working_df['Unit_Price'].plot(kind='hist', bins=30, density=True, alpha=0.5, label='Histogram')
    working_df['Unit_Price'].plot(kind='kde', label='KDE')
    plt.title('KDE of Price per Unit')
    plt.xlabel('Price')
    plt.ylabel('Density')
    plt.grid(True)
    plt.savefig("Output_Graphs/General/Unit Price KDE.png")
    plt.close()
