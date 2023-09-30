# %%
import yfinance as yf
import datetime
from ticker_data import stocks as tickers
import pandas as pd
from data import END_DATE

# %%

start_date = datetime.datetime(2010, 1, 1)
end_date = END_DATE

# %%
technical_data = {}

for ticker in tickers:
    technical_data[ticker] = pd.DataFrame(
        yf.download(ticker, start=start_date, end=end_date)
    )

    technical_data[ticker]["Next Day"] = technical_data[ticker]["Close"].shift(-1)
    technical_data[ticker]["label"] = (
        technical_data[ticker]["Next Day"] >= technical_data[ticker]["Close"]
    ).astype(int)

    del technical_data[ticker]["Next Day"]


# %%
horizons = [2, 5, 60, 250, 1000]


def indicators(data):
    for horizon in horizons:
        rolling_avg = data["Close"].rolling(horizon).mean()

        ratio_column = f"Close_Ratio_{horizon}"
        data[ratio_column] = data["Close"] / rolling_avg

        trend_column = f"Trend_{horizon}"
        data[trend_column] = data["label"].shift(1).rolling(horizon).sum()


# %%

for ticker in tickers:
    indicators(technical_data[ticker])
    technical_data[ticker] = technical_data[ticker].dropna()

# %%
