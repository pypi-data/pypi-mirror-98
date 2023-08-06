# ETL library to download and pre-process financial data.

This tools process and enrichs data screpped from Yahoo Finance into a sets of CSV files. It was conceived as a CI component to generate static data for testing purposes.

## Installation

### Requirements

- `click`
- `blessed` 
- `pandas-datareader`

### PIP
```console
pip install exploratium-quant
```

## Usage

```console
Usage: quant-cli [OPTIONS]

Options:
  -t, --tickers TEXT   Tickers to analyse.
  -o, --out-dir PATH   Path to save results.
  --verbose / --quiet  Verbosity on/off.
  --help               Show this message and exit.
```

### Example

By calling:
```console
quant-cli -t "BTC-USD,SPY,ETH-USD,GME"
```

The tool will save a daily OHLC timeseries for the ticker along the following generated metrics:

- **ma7**: 7 days moving average
- **ma30**: 30 days moving average
- **ma90**: 90 days moving average
- **upper_bollinger_band**: Upper Bollinger Band
- **lower_bollinger_band**: Lower Bollinger Band
- **daily_returns**: Daily returns
- **sharpe**: Sharpe ratio

