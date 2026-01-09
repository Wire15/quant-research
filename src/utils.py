from pathlib import Path
import yfinance as yf
import pandas as pd 
from matplotlib import pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
FIG_DIR = ROOT / 'figures'

# Make sure folders exist
DATA_DIR.mkdir(exist_ok=True)
FIG_DIR.mkdir(exist_ok=True)

# Function for pulling ticker prices
def download_data(tickers, startDate):
    df = yf.download(tickers=tickers, start=startDate, progress=False, group_by='column', auto_adjust=True)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    close = df.xs('Close', axis=1, level=0)
    returns = close.pct_change()
    return close, returns

# Function for plotting equity curves
def plot_equity(equity, title, ylabel, filename):
    ax = equity.plot(figsize=(10, 6))
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Date')
    ax.legend(title='Ticker')
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=300)

def data_quality(close):
    """Function to check data quality by calculating the percentage of missing values for each ticker."""
    num_rows = close.shape[0]
    num_columns = close.shape[1]
    start_date = close.index.min().strftime('%Y-%m-%d')
    end_date = close.index.max().strftime('%Y-%m-%d')
    missing_data = close.isna().mean().sort_values(ascending=False)
    missing_pct = (missing_data * 100).round(2)
    top_missing = missing_pct.head(10)
    # If ticker above 5% missing, remove it from dataset
    tickers_to_remove = missing_pct[missing_pct > 5].index.tolist()
    duplicated_dates = close.index[close.index.duplicated()].unique()
    # Ensure index is sorted
    if not close.index.is_monotonic_increasing:
        close = close.sort_index()

    print ("Data Quality Report:")
    print (f"Date Range: {start_date} to {end_date}")
    print (f"Number of Rows: {num_rows}")
    print (f"Number of Columns (Tickers): {num_columns}")
    print (f"Overall Missing Data: {missing_pct.mean():.2f}%")
    print (f"Top 10 Tickers by Missing Data Percentage: {top_missing.to_dict()}")
    print (f"Tickers to Remove (>5% missing): {tickers_to_remove}")
    print (f"Duplicated Dates in Index: {duplicated_dates.tolist()}")

    report = {
        'num_rows': num_rows,
        'num_columns': num_columns,
        'start_date': start_date,
        'end_date': end_date,
        'top_missing': top_missing,
        'tickers_to_remove': tickers_to_remove,
        'duplicated_dates': duplicated_dates,
    }
    return report