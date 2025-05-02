import pandas as pd
import matplotlib.pyplot as plt

from Contants import *

def analyze_technical_specs(laptops_df, mobiles_df, base_df):
    laptops = laptops_df.copy()
    mobiles = mobiles_df.copy()
    df = base_df.copy()

    # ---------- Helper Functions ----------
    def bar_plot_grouped(data, title, xlabel, ylabel, rotation=0, save_as=None):
        ax = data.plot(kind='bar', figsize=(10, 6))
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=rotation)
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        if save_as:
            plt.savefig(save_as)
        else:
            plt.show()
        plt.close()

    def plot_rom_ssd_by_brand():
        # Group ROM and SSD by Brand
        rom_grouped = df.groupby([BRAND_COL, ROM_COL])[QUANTITY_COL].sum().unstack().fillna(0)
        ssd_grouped = laptops[laptops[SSD_COL] != "N/A"].groupby([BRAND_COL, SSD_COL])[QUANTITY_COL].sum().unstack().fillna(0)

        brands = sorted(set(df[BRAND_COL].unique()) & set(laptops[BRAND_COL].unique()))
        for brand in brands:
            fig, ax = plt.subplots(figsize=(12, 6))
            # Plot ROM in blue
            if brand in rom_grouped.index:
                rom_grouped.loc[brand].plot(
                    kind='bar', position=0, width=0.4, label='ROM', ax=ax, color='skyblue'
                )

            # Plot SSD in orange
            if brand in ssd_grouped.index:
                ssd_grouped.loc[brand].plot(
                    kind='bar', position=1, width=0.4, label='SSD', ax=ax, color='orange'
                )
            plt.title(f"ROM and SSD Distribution for {brand}")
            plt.xlabel("Storage Size")
            plt.ylabel("Units Sold")
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.savefig(f"Output_Graphs/OutputTest/ROM SSD Distribution By Brand/ROM_SSD_Distribution_{brand}.png")
            plt.close()

    def plot_by_group(col_name, group_by, title_prefix, product_filter=None):
        subset = df
        if product_filter == 'laptop':
            subset = laptops
        elif product_filter == 'mobile':
            subset = mobiles

        grouped = subset.groupby([group_by, col_name])[QUANTITY_COL].sum().unstack().fillna(0)
        for group in grouped.index:
            bar_plot_grouped(
                grouped.loc[[group]].T,
                title=f"{title_prefix} by {group_by.capitalize()} - {group}",
                xlabel=col_name.replace('_', ' ').title(),
                ylabel="Units Sold",
                rotation=45,
                save_as=f"Output_Graphs/OutputTest/{title_prefix}/{title_prefix}_by_{group_by}_{group}.png"
            )

    def plot_group_comparison_by_category(col_name, group_by, title, product_filter=None, save_as=None):
        subset = df
        if product_filter == 'laptop':
            subset = laptops
        elif product_filter == 'mobile':
            subset = mobiles

        grouped = subset.groupby([group_by, col_name])[QUANTITY_COL].sum().unstack().fillna(0)
        grouped.T.plot(kind='bar', figsize=(12, 6))
        plt.title(title)
        plt.xlabel(col_name.replace('_', ' ').title())
        plt.ylabel("Units Sold")
        plt.xticks(rotation=45)
        plt.legend(title=group_by.title())
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        if save_as:
            plt.savefig(save_as)
        else:
            plt.show()
        plt.close()
    def diffusion_matrix(col1, col2, weight_col=None, normalize=False, title=None, laptop_df=False, mobile_df=False):
        working_df = df
        if laptop_df and mobile_df:
            working_df = df
        elif laptop_df and not mobile_df:
            working_df = laptops
        elif not laptop_df and mobile_df:
            working_df = mobiles
        if weight_col:
            matrix = pd.crosstab(working_df[col1], working_df[col2], values=working_df[weight_col], aggfunc='sum').fillna(0)
        else:
            matrix = pd.crosstab(working_df[col1], working_df[col2])
        if normalize:
            matrix = matrix.div(matrix.sum(axis=1), axis=0)

        plt.figure(figsize=(10, 6))
        plt.imshow(matrix, cmap='Blues', aspect='auto')
        plt.colorbar(label='Weighted Frequency' if weight_col else 'Count')
        plt.xticks(range(len(matrix.columns)), matrix.columns, rotation=45)
        plt.yticks(range(len(matrix.index)), matrix.index)
        plt.title(title or f"Diffusion Matrix: {col1} vs {col2}")
        plt.xlabel(col2.replace('_', ' ').title())
        plt.ylabel(col1.replace('_', ' ').title())
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig(f"Output_Graphs/OutputTest/{title}.png")
        plt.close()

    # ---------- General Distributions ----------
    bar_plot_grouped(df.groupby(RAM_COL)[QUANTITY_COL].sum(), "Total RAM Distribution", "RAM Size (GB)", "Units Sold", save_as="Output_Graphs/OutputTest/Total_RAM_Distribution.png")
    bar_plot_grouped(df.groupby(ROM_COL)[QUANTITY_COL].sum(), "Total ROM Distribution", "ROM Size (GB)", "Units Sold", save_as="Output_Graphs/OutputTest/Total_ROM_Distribution.png")

    bar_plot_grouped(laptops.groupby(CORE_COL)[QUANTITY_COL].sum(), "Laptop Core Spec Distribution", "Core Model", "Units Sold", 45, save_as="Output_Graphs/OutputTest/Laptop_Core_Spec_Distribution.png")
    bar_plot_grouped(mobiles.groupby(PROCESSOR_COL)[QUANTITY_COL].sum(), "Mobile Processor Spec Distribution", "Processor Model", "Units Sold", 45, save_as="Output_Graphs/OutputTest/Mobile_Processor_Spec_Distribution.png")

    bar_plot_grouped(
        laptops[laptops[SSD_COL] != "N/A"].groupby(SSD_COL)[QUANTITY_COL].sum(),
        "Laptop SSD Distribution", "SSD Size", "Units Sold", 45, save_as="Output_Graphs/OutputTest/Laptop_SSD_Distribution.png"
    )

    # ---------- Grouped by Region ----------
    plot_group_comparison_by_category(SSD_COL, REGION_COL, "SSD Distribution by Region", product_filter='laptop',
                                      save_as="Output_Graphs/OutputTest/SSD_Distribution_by_Region_ALL.png")
    plot_group_comparison_by_category(PROCESSOR_COL, REGION_COL, "Mobile Processor Spec Distribution by Region",
                                      product_filter='mobile',
                                      save_as="Output_Graphs/OutputTest/Mobile_Processor_Spec_Distribution_by_Region_ALL.png")
    plot_group_comparison_by_category(CORE_COL, REGION_COL, "Laptop Core Spec Distribution by Region",
                                      product_filter='laptop',
                                      save_as="Output_Graphs/OutputTest/Laptop_Core_Spec_Distribution_by_Region_ALL.png")
    plot_group_comparison_by_category(RAM_COL, REGION_COL, "Laptop Core Spec Distribution by Region",
                                      save_as="Output_Graphs/OutputTest/RAM_Distribution_by_Region_ALL.png")
    plot_group_comparison_by_category(ROM_COL, REGION_COL, "Laptop Core Spec Distribution by Region",
                                      save_as="Output_Graphs/OutputTest/ROM_Distribution_by_Region_ALL.png")
    # ---------- Grouped by Brand (except ROM/SSD combined handled separately) ----------
    plot_by_group(RAM_COL, BRAND_COL, "RAM Distribution")
    plot_by_group(CORE_COL, BRAND_COL, "Laptop Core Spec Distribution", product_filter='laptop')
    plot_by_group(PROCESSOR_COL, BRAND_COL, "Mobile Processor Spec Distribution", product_filter='mobile')

    # ---------- Combined ROM + SSD by Brand ----------
    plot_rom_ssd_by_brand()

    # ---------- Diffusion Matrices ----------
    diffusion_matrix(RAM_COL, REGION_COL, weight_col=QUANTITY_COL, title="RAM vs Region (Weighted)")
    diffusion_matrix(ROM_COL, BRAND_COL, weight_col=QUANTITY_COL, title="ROM vs Brand (Weighted)")
    diffusion_matrix(CORE_COL, BRAND_COL, weight_col=QUANTITY_COL, title="Core Spec vs Brand (Laptops)", laptop_df=True)
    diffusion_matrix(PROCESSOR_COL, REGION_COL, weight_col=QUANTITY_COL, title="Processor Spec vs Region (Mobiles)", mobile_df=True)
