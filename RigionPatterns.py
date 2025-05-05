from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
from Contants import *
from Utilities import plot_heatmap

def plot_quantity_distribution(df, title, save_as):
    grouped = df.groupby(['Region', 'Quantity Sold']).size().unstack().fillna(0)

    grouped.T.plot(kind='bar', figsize=(12, 6))
    plt.title(title)
    plt.xlabel('Quantity Sold')
    plt.ylabel('Number of Transactions')
    plt.legend(title='Region', loc = 'lower center')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(save_as)
    plt.close()


def generateRagionPatterns(base_df, laptops, mobiles):
    plot_heatmap(base_df, 'RAM', "Diffusion Matrix Ram vs Region","Output_Graphs/Identify Regional Transaction Patterns/Diffusion Matrix Ram vs Region.png")
    plot_heatmap(base_df, 'ROM', "Diffusion Matrix ROM vs Region","Output_Graphs/Identify Regional Transaction Patterns/Diffusion Matrix ROM vs Region.png")
    plot_heatmap(laptops, 'SSD',"Diffusion Matrix SSD vs Region (Laptops Only)", "Output_Graphs/Identify Regional Transaction Patterns/Diffusion Matrix SSD vs Region (Laptops Only).png")
    plot_quantity_distribution(laptops,"Quantity Sold Frequency by Region (Laptops)", "Output_Graphs/Identify Regional Transaction Patterns/Quantity Sold Frequency by Region (Laptops).png")
    plot_quantity_distribution(mobiles,"Quantity Sold Frequency by Region (Mobiles)", "Output_Graphs/Identify Regional Transaction Patterns/Quantity Sold Frequency by Region (Mobiles).png")
