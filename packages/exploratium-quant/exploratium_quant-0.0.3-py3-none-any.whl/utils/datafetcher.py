import sys
sys.path.append("..")
from exploratium.quant import Quant as q
from typing import List, Tuple
import datetime as dt
import pandas as pd
import pandas_datareader as pdr


def load_ticker_data(
    tickers: List[str],
    start: str = (dt.datetime.today() + dt.timedelta(-365)).isoformat(),
    end: str = dt.datetime.today().isoformat(),
) -> List[Tuple[str, pd.DataFrame]]:
    """Saves current enriched dataframes to disk.

    Keyword arguments:
    tickers -- the symbols to save (default)
    """

    ticker_data = []

    for ticker in tickers:
        ticker_data.append((ticker, pdr.get_data_yahoo(ticker, start, end)))

    return ticker_data


def transform_ticker_data(
    tickers: List[pd.DataFrame],
    out_dir: str = "./data",
    traded_days: int = 252,
    field: str = "Adj Close"
) -> List[str]:
    """Saves current enriched dataframes to disk.

    Keyword arguments:
    tickers -- the symbols to save (default)
    """

    ticker_files = []

    for ticker, df in tickers:
        df["ma7"] = q.get_rolling_mean(df[field], 7)
        df["ma30"] = q.get_rolling_mean(df[field], 30)
        df["ma90"] = q.get_rolling_mean(df[field], 90)

        df["upper_bollinger_band"], df["lower_bollinger_band"] = q.get_bollinger_bands(
            q.get_rolling_mean(df[field]), q.get_rolling_std(
                df[field])
        )

        df["daily_returns"] = q.get_daily_returns(df[field])
        df["sharpe"] = q.get_sharpe(df[field], traded_days)

        path = "{}/{}.csv".format(out_dir, ticker)
        df.to_csv(path)
        ticker_files.append(path)

    return ticker_files
