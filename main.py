from loading import load_base_dataset
import numpy as np
import pandas as pd
from Contants import  *
from brandsAnalysis import *
from salesMobilesLaptopsComparison import *
from brandMainFinancialProfit import *
from CoreSpecAnalysis import *
from memoriesAnalysis import *
import os
import glob
from pathlib import Path
import logging              
from data_quality import clean_and_audit   
from extra_visualizations import generate_extra_graphs
from GeneralAnalysis import *

def to_gb(val):
    val = str(val).strip().upper()
    if 'TB' in val:
        return int(val.replace('TB', '').strip()) * 1024
    elif 'GB' in val:
        return int(val.replace('GB', '').strip())
    return np.nan

def get_fixed_base_dataframes(base_df):
    string_columns = [BRAND_COL, PRODUCT_ID_COL,PRODUCT_DISCRIPTION_COL , CUSTOMER_COL,LOCATION_COL, REGION_COL, PROCESSOR_COL,CORE_COL  ]
    date_columns = [INWARD_DATE_COL, DISPATCH_DATE_COL]
    memory_columns = [RAM_COL, ROM_COL, SSD_COL]

    for col in string_columns: base_df[col] = base_df[col].astype(str)
    for col in date_columns: base_df[col] = pd.to_datetime(base_df[col], dayfirst=True, errors='coerce', format='mixed')
    for col in memory_columns: base_df[col] = base_df[col].map(to_gb).fillna(0).astype(int)
    # --- Feature Engineering ---
    base_df['has_ssd'] = base_df['SSD'].notna().astype(int)
    base_df['Unit_Price'] = base_df['Price'] / base_df['Quantity Sold']
    base_df['Inward Month'] = base_df['Inward Date'].dt.to_period('M')
    base_df['Inward Year'] = base_df['Inward Date'].dt.year
    return base_df[base_df[PRODUCT_COL] == 'Mobile Phone'] , base_df[base_df[PRODUCT_COL] == 'Laptop'], base_df


def delete_all_pngs(path):
    # Use glob to find all .png files recursively
    png_files = glob.glob(os.path.join(path, '**', '*.png'), recursive=True)

    for file_path in png_files:
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")


if __name__=="__main__":
    base_df = load_base_dataset()
    delete_all_pngs("Output_Graphs")

    # ---------- NEW step: quality audit ----------
    Path("EDA_Reports").mkdir(exist_ok=True)   # creates folder once

    # --- Set up logging (writes cleaning.log) ---
    logging.basicConfig(
        filename="EDA_Reports/cleaning.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    
    #base_df1 = clean_and_audit(base_df.copy())

    mobile_df, laptop_df , base_df = get_fixed_base_dataframes(base_df)
    general_analysis(mobile_df, laptop_df, base_df)
    analyze_mobile_laptop_sales(mobile_df, laptop_df)

    analyze_technical_specs(laptop_df, mobile_df, base_df)
    #base_df.to_csv('base_df.csv', index=False)
    getBrandsMainFinancialProfit(base_df)
    brands_avg_quantity_and_price(base_df)
    analyseCoreSpecs (laptop_df)
    generate_extra_graphs(base_df)


