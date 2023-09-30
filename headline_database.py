# %%
from data import db_path
import pandas as pd
import sqlite3
from ticker_data import stocks as tickers


connection = sqlite3.connect(db_path)
database = pd.Series(index=tickers)
for ticker in tickers:
    query = "SELECT * FROM " + ticker + "_"
    database[ticker] = pd.read_sql_query(query, connection)

connection.close()
# %%
headlines = {}
for ticker in tickers:
    headlines[ticker] = database[ticker][["datetime", "headline", "url"]].copy()
    headlines[ticker]["date"] = pd.to_datetime(
        headlines[ticker]["datetime"], unit="s"
    ).dt.date
    headlines[ticker]["time"] = pd.to_datetime(
        headlines[ticker]["datetime"], unit="s"
    ).dt.time
    del headlines[ticker]["datetime"]
    headlines[ticker] = headlines[ticker][["date", "time", "headline", "url"]]

# %%
