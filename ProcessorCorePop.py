import pandas as pd
import matplotlib.pyplot as plt
from Contants import INWARD_DATE_COL, DISPATCH_DATE_COL, QUANTITY_COL, PRICE_COL, CORE_COL, PROCESSOR_COL
from Utilities import compute_cumulative, format_k_m
import numpy as np
def proccessorCorePop(base_df, laptops, mobiles):
    coresAnalysis(laptops, 'Laptops')
    coresAnalysis(mobiles, 'Mobiles')
    df = base_df.copy()
    conditions = [
        df[PROCESSOR_COL].str.startswith('i', na=False),
        df[PROCESSOR_COL].str.startswith('Snapdragon', na=False),
        df[PROCESSOR_COL].str.startswith('MediaTek', na=False),
        df[PROCESSOR_COL].str.startswith('Apple', na=False),
        df[PROCESSOR_COL].str.startswith('Samsung', na=False),
        df[PROCESSOR_COL].str.startswith('Ryzen', na=False)
    ]

    choices = ['Intel', 'Snapdragon', 'MediaTek', 'Apple','Samsung', 'AMD']

    # Create new column
    df['Processor Brand'] = np.select(conditions, choices, default='Other')
    coreBrandAnalysis(df)



def coreBrandAnalysis(df):
    working_df = df.copy()
    working_df['Month'] = working_df[DISPATCH_DATE_COL].dt.to_period('M').dt.to_timestamp()
    months_sorted = sorted(working_df['Month'].unique())
    valid_months = months_sorted[1:-1]
    working_df = working_df[working_df['Month'].isin(valid_months)]
    grouped = working_df.groupby(['Month', 'Processor Brand'])[QUANTITY_COL].sum().unstack()
    plt.figure(figsize=(14, 6))
    grouped.plot(ax=plt.gca(), linewidth=2, marker='o')
    plt.title(f'Processor Brand Popularity Over 2-Month Intervals')
    plt.xlabel('2-Month Interval')
    plt.ylabel('Units Sold')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.legend(title='Processor Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f"Output_Graphs/Analyse Processor and Core Popularity Over Time/Processor Brand Popularity Over 2-Month Intervals.png")
    plt.close()

def coresAnalysis(df, type):
    working_df = df.copy()
    working_df['Month'] = working_df[DISPATCH_DATE_COL].dt.to_period('M').dt.to_timestamp()
    months_sorted = sorted(working_df['Month'].unique())
    valid_months = months_sorted[1:-1]
    working_df = working_df[working_df['Month'].isin(valid_months)]
    month_to_bin = {
        month: f"{valid_months[i].strftime('%b')}–{valid_months[i + 1].strftime('%b %Y')}"
        for i in range(0, len(valid_months) - 1, 2)
        for month in [valid_months[i], valid_months[i + 1]]
    }
    working_df['Month_Bin'] = working_df['Month'].map(month_to_bin)
    grouped = working_df.groupby(['Month_Bin', PROCESSOR_COL])[QUANTITY_COL].sum().unstack()
    plt.figure(figsize=(14, 6))
    grouped.plot(kind='bar', ax=plt.gca())
    plt.title(f'Processor Type Popularity Over 2-Month Intervals ({type})')
    plt.xlabel('2-Month Interval')
    plt.ylabel('Units Sold')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.legend(title='Processor Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f"Output_Graphs/Analyse Processor and Core Popularity Over Time/Processor Type Popularity Over 2-Month Intervals ({type}).png")
    plt.close()