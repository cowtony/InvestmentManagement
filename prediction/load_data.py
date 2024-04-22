import pandas as pd


def loadStockData(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)    # Load the CSV file into a pandas DataFrame

    df['Date'] = pd.to_datetime(df['Date'])  # Convert the 'Date' column to datetime

    df.set_index(['Date', 'Symbol'], inplace=True)  # Set the 'Date' column as the index of the DataFrame

    return df
