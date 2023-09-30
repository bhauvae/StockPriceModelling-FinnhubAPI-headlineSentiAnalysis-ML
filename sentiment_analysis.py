# %%
from headline_database import headlines
from stock_database import technical_data
from ticker_data import stocks as tickers
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# %%
combined_headlines = {}
for ticker in tickers:
    combined_headlines[ticker] = (
        headlines[ticker].groupby(["date"])["headline"].apply(" ".join).reset_index()
    )
    combined_headlines[ticker].rename(
        columns={"headline": "combined_headlines"}, inplace=True
    )
    combined_headlines[ticker].set_index("date", inplace=True)

# %%
data = {}
for ticker in tickers:
    data[ticker] = pd.merge(
        combined_headlines[ticker],
        technical_data[ticker],
        how="left",
        left_index=True,
        right_index=True,
    )
    data[ticker] = data[ticker].dropna()


# %%
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity


def getPolarity(text):
    return TextBlob(text).sentiment.polarity


def getSIA_scores(text):
    return SentimentIntensityAnalyzer().polarity_scores(text)


# %%
for ticker in tickers:
    data[ticker]["subjectivity"] = data[ticker]["combined_headlines"].apply(
        getSubjectivity
    )
    data[ticker]["polarity"] = data[ticker]["combined_headlines"].apply(getPolarity)

    data[ticker]["SIA_scores"] = data[ticker]["combined_headlines"].apply(getSIA_scores)
    data[ticker]["compound"] = data[ticker]["SIA_scores"].apply(lambda x: x["compound"])
    data[ticker]["negative"] = data[ticker]["SIA_scores"].apply(lambda x: x["neg"])
    data[ticker]["neutral"] = data[ticker]["SIA_scores"].apply(lambda x: x["neu"])
    data[ticker]["positive"] = data[ticker]["SIA_scores"].apply(lambda x: x["pos"])
    labels = data[ticker]["label"].copy()
    del data[ticker]["label"]
    del data[ticker]["SIA_scores"]
    del data[ticker]["combined_headlines"]

    data[ticker]["label"] = labels


# %%
