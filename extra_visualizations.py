# extra_visualizations.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def generate_extra_graphs(df: pd.DataFrame):
    output_dir = Path("Output_Graphs/Extra")
    output_dir.mkdir(parents=True, exist_ok=True)

    #  Boxplot of Unit Price by Product
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x='Product', y='Unit_Price')
    plt.title("Unit Price Distribution by Product")
    plt.tight_layout()
    plt.savefig(output_dir / "UnitPrice_by_Product.png")
    plt.close()


    #  Monthly Sales Trend (Quantity Sold over Time)
    monthly_sales = df.groupby('Inward Month')['Quantity Sold'].sum()
    plt.figure(figsize=(12, 5))
    monthly_sales.plot(kind='line', marker='o')
    plt.title("Total Quantity Sold Over Time")
    plt.xlabel("Month")
    plt.ylabel("Units Sold")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "Monthly_Sales_Trend.png")
    plt.close()

    print("✅ Extra visualizations generated.")
