# %%
from sentiment_analysis import data, tickers
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import numpy as np
# %%
keep_columns=["Open","High","Low","Close","Adj Close","Volume","subjectivity","polarity","compound","negative","neutral","positive","label"]
for ticker in tickers:
    data[ticker] = data[ticker][keep_columns]

# %%
model = LinearDiscriminantAnalysis()
report = {}
# %%
for ticker in tickers:
    x = np.array(data[ticker].drop(["label"], axis=1))
    y = np.array(data[ticker]["label"])

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=0
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    report[ticker] = accuracy_score(y_test, predictions)

# %%
