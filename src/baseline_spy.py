from pathlib import Path
import pandas as pd
import yfinance as yf   
from matplotlib import pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
FIG_DIR = ROOT / 'figures'

# Make sure folders exist
DATA_DIR.mkdir(exist_ok=True)
FIG_DIR.mkdir(exist_ok=True)

# Function for pulling prices
def download_prices(tickers, startDate):
    df = yf.download(tickers=tickers, start=startDate, progress=False, group_by='column', auto_adjust=True)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    close = df.xs('Close', axis=1, level=0)
    returns = close.pct_change()

    #print (close.head())
    #print (close.isna().mean().sort_values(ascending=False).head())
    equity = (1 + returns).cumprod()
    return close, returns, equity

# Function for plotting equity curves
def plot_equity(equity, title, ylabel, filename):
    ax = equity.plot(figsize=(10, 6))
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Date')
    ax.legend(title='Ticker')
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=300)

if __name__ == "__main__":
    tickers = ['SPY']
    startDate = '2010-01-01'
    close, returns, equity = download_prices(tickers, startDate)
    # Save data to CSV files
    close.to_csv(DATA_DIR / 'spy_close_prices.csv')
    returns.to_csv(DATA_DIR / 'spy_returns.csv')
    # Plot equity curves & save figures
    plot_equity(equity, 'Cumulative Returns of SPY since 2010-01-01', 'Cumulative Return', 'cumulative_returns_spy.png')