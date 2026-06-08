import pandas as pd

FILE_PATH = "data/raw/rtt_incomplete_pathways.xlsx"

def load_data():
    df = pd.read_excel(FILE_PATH)
    return df

if __name__ == "__main__":
    df = load_data()
    print(df.head())
    print(df.shape)
