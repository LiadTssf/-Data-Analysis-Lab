from loading import load_base_dataset
import numpy as np
import pandas as pd
from Contants import  *
from brandsAnalysis import *
from salesMobilesLaptopsComparison import *
from brandMainFinancialProfit import *
from CoreSpecAnalysis import *
def to_gb(val):
    val = str(val).strip().upper()
    if 'TB' in val:
        return int(val.replace('TB', '').strip()) * 1024
    elif 'GB' in val:
        return int(val.replace('GB', '').strip())
    return np.nan

def get_fixed_base_dataframes(base_df):
    string_columns = [BRAND_COL, PRODUCT_ID_COL,PRODUCT_DISCRIPTION_COL , COSTUMER_COL,LOCATION_COL, REGION_COL, PROCESSOR_COL,CORE_COL  ]
    date_columns = [INWARD_DATE_COL, DISPATCH_DATE_COL]
    memory_columns = [RAM_COL, ROM_COL, SSD_COL]

    for col in string_columns: base_df[col] = base_df[col].astype(str)
    for col in date_columns: base_df[col] = pd.to_datetime(base_df[col], dayfirst=True, errors='coerce', format='mixed')
    for col in memory_columns: base_df[col] = base_df[col].map(to_gb).fillna(0).astype(int)

    return base_df[base_df[PRODUCT_COL] == 'Mobile Phone'] , base_df[base_df[PRODUCT_COL] == 'Laptop'], base_df




if __name__=="__main__":
    base_df = load_base_dataset()
    mobile_df, laptop_df , base_df = get_fixed_base_dataframes(base_df)
    analyseCoreSpecs (laptop_df)
    base_df.to_csv('base_df.csv', index=False)
    getBrandsMainFinancialProfit(base_df)
    analyze_mobile_laptop_sales(mobile_df, laptop_df)
    brands_avg_quantity_and_price(base_df)



