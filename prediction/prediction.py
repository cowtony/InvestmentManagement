from datetime import timedelta
from typing import List
import numpy as np
import pandas as pd


def prediction(df: pd.DataFrame, stocks: List[str], date: str, R: np.ndarray) -> np.ndarray:
    end_date = pd.to_datetime(date)
    start_date = end_date - timedelta(days=365)

    # Filter the DataFrame to include only the relevant dates and stocks
    df_filtered = df.loc[(df.index.get_level_values('Date') > start_date) &
                         (df.index.get_level_values('Date') <= end_date) &
                         (df.index.get_level_values('Symbol').isin(stocks))]

    P = np.zeros((R.size,) * len(stocks)) + np.finfo(float).eps

    prev_adj_close = {stock: None for stock in stocks}
    # Iterate over each date prior to 'date' and within 1 year
    for current_date in pd.date_range(start=start_date, end=end_date):
        # Skip dates not in the DataFrame
        if current_date not in df_filtered.index.get_level_values('Date'):
            continue

        # Get the DataFrame for the current date
        df_current = df_filtered.loc[df_filtered.index.get_level_values('Date') == current_date]

        # Indices to update in P for the current date
        indices = []

        # For each stock name, calculate the return index
        for stock in stocks:
            # Get the stock's adjusted closing price for the current date
            adj_close = df_current.loc[df_current.index.get_level_values('Symbol') == stock, 'Adj Close'].values[0]
            if prev_adj_close[stock]:
                stock_return = (adj_close - prev_adj_close[stock]) / prev_adj_close[stock]
                print(adj_close, prev_adj_close[stock], stock_return)
                # Find the index in R that is closest to the stock_return
                return_index = np.argmin(np.abs(R - stock_return))
                indices.append(return_index)

            prev_adj_close[stock] = adj_close

        # Update the count in P for the calculated return indices
        if len(indices) == len(stocks):
            P[tuple(indices)] += 1

    P /= np.sum(P)  # Normalize

    return P

