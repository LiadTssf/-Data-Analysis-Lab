# data_quality.py
import logging
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats
import re

LOGGER = logging.getLogger(__name__)

def audit_missing(df: pd.DataFrame) -> pd.Series:
    """Return a Series of missing counts and log a heatmap."""
    missing = df.isna().sum().sort_values(ascending=False)
    LOGGER.info("Missing-value counts:\n%s", missing.head(10))

    out_dir = Path("EDA_Reports")
    out_dir.mkdir(exist_ok=True)
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.isna(), cbar=False)
    plt.title("Missing-value pattern")
    plt.savefig(out_dir / "missing_pattern.png", dpi=150)
    plt.close()
    missing_counts = df.isna().sum().sort_values(ascending=False)

    plt.figure(figsize=(10, 4))
    sns.barplot(x=missing_counts.index, y=missing_counts.values, palette="viridis")
    plt.xticks(rotation=45, ha='right')
    plt.title("Missing Value Count Per Column")
    plt.ylabel("Missing entries")
    plt.tight_layout()
    plt.savefig("EDA_Reports/missing_barplot.png")
    #plt.show()
    plt.close()
    # --- Missing value rate by Product type (phones vs laptops) ---
    group_missing = df.groupby("Product").apply(lambda g: g.isna().mean()).T

    plt.figure(figsize=(12, 5))
    group_missing.plot(kind="bar", figsize=(12, 5), colormap="Set2")
    plt.title("Missing Value Rate by Product Type")
    plt.ylabel("Fraction Missing")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("EDA_Reports/missing_by_product.png")
    plt.close()
    return missing

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    subset_cols = ['Product Code', 'Customer Name', 'Inward Date']
    before = len(df)
    df = df.drop_duplicates(subset=subset_cols)
    removed = before - len(df)
    LOGGER.info("Duplicates removed (subset=%s): %d", subset_cols, removed)
    return df

def detect_outliers_iqr(df: pd.DataFrame, cols, k=1.5) -> pd.DataFrame:
    """Marks rows with outliers in *any* of the listed numeric cols."""
    mask = pd.Series(False, index=df.index)
    for c in cols:
        col_values = df[c].dropna()
        if col_values.empty:
            LOGGER.warning("Skipping column '%s' — no valid numeric values", c)
            continue
        q1, q3 = np.percentile(df[c].dropna(), [25, 75])
        iqr = q3 - q1
        lower, upper = q1 - k * iqr, q3 + k * iqr
        mask |= (df[c] < lower) | (df[c] > upper)
    LOGGER.info("Outlier rows flagged: %d", mask.sum())
    flagged = df[mask].copy()
    flagged.to_csv("EDA_Reports/outliers.csv", index=False)
    return df[~mask]

def detect_outliers_z(df: pd.DataFrame, col, z_thresh=3):
    z = np.abs(stats.zscore(df[col].dropna()))
    mask = z > z_thresh
    LOGGER.info("Z-score outliers in %s: %d", col, mask.sum())
    df[mask].to_csv(f"EDA_Reports/outliers_{col}.csv", index=False)
    return df[~mask]

def to_gb(val):
    if pd.isna(val):
        return np.nan
    val = str(val).upper().strip()
    match = re.search(r"(\d+(\.\d+)?)", val)   # finds the number part
    if not match:
        return np.nan
    num = float(match.group(1))
    if "TB" in val:
        return int(num * 1024)
    if "GB" in val:
        return int(num)
    return np.nan


def clean_and_audit(df: pd.DataFrame) -> pd.DataFrame:
    
    audit_missing(df)
    for col in ["RAM", "SSD", "Price"]:
        print(f"\nUnique values in {col}:")
        print(df[col].dropna().unique()[:10])
        # Convert RAM/SSD to GB using to_gb() helper
        df["RAM"] = df["RAM"].map(to_gb)
        df["SSD"] = df["SSD"].map(to_gb)

        # Quantity Sold and Price to numeric just to be safe
        df["Quantity Sold"] = pd.to_numeric(df["Quantity Sold"], errors="coerce")
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    
    df = remove_duplicates(df)
    df = detect_outliers_iqr(df, cols=["Price", "Quantity Sold", "RAM"])
    df = detect_outliers_z(df, col='Price', z_thresh=3)
    return df
