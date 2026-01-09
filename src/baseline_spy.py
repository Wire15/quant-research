from pathlib import Path
import pandas as pd
from utils import download_data, data_quality, plot_equity

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
FIG_DIR = ROOT / 'figures'

# Make sure folders exist
DATA_DIR.mkdir(exist_ok=True)
FIG_DIR.mkdir(exist_ok=True)

if __name__ == "__main__":
    tickers = DATA_DIR / 'universe.csv'
    tickers = pd.read_csv(tickers)['ticker'].tolist()
    startDate = '2013-01-01'
    close, returns = download_data(tickers, startDate)
    report = data_quality(close)

    # Remove tickers with more than 5% missing data
    close = close.drop(columns=report['tickers_to_remove'])
    returns = returns[close.columns]

    # Save data to CSV files
    close.to_csv(DATA_DIR / f'universe_close_prices_{startDate}.csv')
    returns.to_csv(DATA_DIR / f'universe_returns_{startDate}.csv')

    # Plot equity curves & save figures
    # plot_equity(equity, 'Cumulative Returns of SPY, QQQ, and IWM since 2010-01-01', 'Cumulative Return', 'cumulative_returns_spy_qqq_iwm.png')