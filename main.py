from loading import load_base_dataset


if __name__=="__main__":
    base_df = load_base_dataset()
    a = base_df.describe()
    print(a)