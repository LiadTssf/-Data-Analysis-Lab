from Contants import  *
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Utilities import *
import matplotlib.ticker as ticker
import numpy as np
from scipy.stats import chi2_contingency

coreSpecTypes = {
    "i3": "Intel",
    "i5": "Intel",
    "i7": "Intel",
    "i9": "Intel",
    "Ryzen 3": "AMD",
    "Ryzen 5": "AMD",
    "Ryzen 7": "AMD",
    "Ryzen 9": "AMD"
}

def analyseCoreSpecs(laptops_df):
    laptops_df = laptops_df.copy()
    laptops_df['CoreBrand'] = laptops_df[CORE_COL].map(coreSpecTypes)
    laptops_df['CoreBrand'] = laptops_df['CoreBrand'].fillna('Other')

    contingency = pd.pivot_table(
        laptops_df,
        index=BRAND_COL,
        columns='CoreBrand',
        values=QUANTITY_COL,
        aggfunc='sum',
        fill_value=0
    )

    # Chi-square test
    chi2, p, dof, expected = chi2_contingency(contingency)

    # Plot stacked bar chart
    custom_colors = ['#50C2E5', '#D46600']
    ax = contingency.plot(kind='bar', stacked=False, width = 0.8, figsize=(8, 5), color = custom_colors)
    plt.title('Core Brand Distribution by Producer Brand (Weighted by Quantity)')
    plt.xlabel('Producer Brand')
    plt.ylabel('Total Quantity Sold')
    plt.legend(title='Core Brand')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig("Output_Graphs/9CoreBrand_Distribution_by_Producer_Brand.png")
