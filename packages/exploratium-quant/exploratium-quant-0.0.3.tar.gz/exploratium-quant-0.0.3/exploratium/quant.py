import datetime as dt
import numpy as np
import pandas as pd


class Quant(object):
    @staticmethod
    def get_daily_returns(values: pd.Series) -> pd.Series:
        """Compute and return the daily return values."""
        return values.pct_change(1).fillna(0)

    @staticmethod
    def get_CAGR(values: pd.Series, traded_days: int = 252) -> pd.Series:
        """Calculates the Compound Annual Growth Rate."""
        return ((1 + values.pct_change()).cumprod()) ** (traded_days / len(values)) - 1

    @staticmethod
    def get_volatility(values: pd.Series, traded_days: int = 252) -> pd.Series:
        """Calculates the daily Volatility over a year, given a number of traded days."""
        return values.pct_change().std() * np.sqrt(traded_days)

    @staticmethod
    def get_sharpe(values: pd.Series, traded_days: int = 252, rf: pd.Series = None) -> pd.Series:
        """Sharpe ratio. RF = risk free rate. If not specified then rf=zero"""
        if not rf:
            rf = np.array([0] * len(values))

        return (Quant.get_CAGR(values, traded_days) - rf) / Quant.get_volatility(values, traded_days)

    @staticmethod
    def get_rolling_mean(values: pd.Series, window: int = 20) -> pd.Series:
        """Return rolling mean of given values, using specified window size."""
        return values.rolling(window=window, center=False).mean()

    @staticmethod
    def get_rolling_std(values: pd.Series, window: int = 20) -> pd.Series:
        """Return rolling standard deviation of given values, using specified window size."""
        return values.rolling(window=window, center=False).std()

    @staticmethod
    def get_bollinger_bands(rm: pd.Series, rstd: pd.Series) -> pd.Series:
        """Return upper and lower Bollinger Bands."""
        upper_band = rm + (rstd * 2)
        lower_band = rm - (rstd * 2)

        return upper_band, lower_band
