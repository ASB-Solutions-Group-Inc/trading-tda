import pandas as pd
import pandas_ta as ta
from arima import convert_dataframe 
from watchlist import Watchlist

def recent_bars(df, tf: str = "1y"):
    # All Data: 0, Last Four Years: 0.25, Last Two Years: 0.5, This Year: 1, Last Half Year: 2, Last Quarter: 4
    yearly_divisor = {"all": 0, "10y": 0.1, "5y": 0.2, "4y": 0.25, "3y": 1./3, "2y": 0.5, "1y": 1, "6mo": 2, "3mo": 4}
    yd = yearly_divisor[tf] if tf in yearly_divisor.keys() else 0
    return int(ta.RATE["TRADING_DAYS_PER_YEAR"] / yd) if yd > 0 else df.shape[0]

def run_Strategy():
    portfolio_dataframe = pd.DataFrame()
    df = portfolio_dataframe.ta.ticker("AAPL", kind="info", lc_cols=True)
    print(df)
    # Used for example Trend Return Long Trend Below
    macd_ = ta.macd(df["close"])
    macdh = macd_[macd_.columns[1]]

    print(macdh.tail())
    # tf = "D"
    # watch = Watchlist("AAPL", tf=tf, ds_name="yahoo", timed=True)
    # watch.strategy = ta.CommonStrategy # If you have a Custom Strategy, you can use it here.  
    # watch.load("AAPL", analyze=True, verbose=False)
    # duration = "1y"
    # asset = "AAPL"
    # recent = recent_bars(asset, duration)
    # asset.columns = asset.columns.str.lower()
    # asset.drop(columns=["dividends", "split"], errors="ignore", inplace=True)
    # asset = asset.copy().tail(recent)
    # print(asset)
    # NonMPStrategy = ta.Strategy(
    # name="EMAs, BBs, and MACD",
    # description="Non Multiprocessing Strategy by rename Columns",
    # ta=[
    #     {"kind": "ema", "length": 8},
    #     {"kind": "ema", "length": 21},
    # ]
    # )
    # # Run it
    # portfolio_dataframe.ta.strategy(NonMPStrategy)

run_Strategy()