#!/usr/bin/python
# -*- coding: utf-8 -*-

# forecast.py

import datetime
import numpy as np
import pandas as pd
import sklearn

import pandas_datareader.data as web
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import confusion_matrix
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.svm import LinearSVC, SVC


def create_lagged_series(symbol, start_date, end_date, lags=5):
    """
    This creates a Pandas DataFrame that stores the percentage returns
    of the adjusted closing value of a stock obtained from Yahoo Finance,
    along with a number of lagged returns from the prior trading days
    (lags defaults to 5 days). Trading volume, as well as the Direction
    from the previos day, are also included.
    """

    # Obtain stock information from Yahoo Finance
    ts = DataReader(symbol, "yahoo", start_date - datetime.timedelta(days=365),
                    end_date)

    # Create the new lagged DataFrame
    tslag = pd.DataFrame(index=ts.index)
    tslaf["Today"] = ts["Adj Close"]
    tslag["Volume"] = ts["Volume"]

    # Create the shifted series of prior trading period close values
    for i in range(0, lags):
        tslag["Lag%s" % str(i+1)] = ts["Adj Close"].shift(i+1)

    # Create the returns DataFrame
    tsret = pd.DataFrame(index=tslag.index)
    tsret["Volume"] = tslag["Volume"]
    tsret["Today"] = tslag["Today"].pct_change()*100.0

    # If any of the values of percentage returns equal zero, set them to
    # a small number (stops issues with QDA model in Scikit-Learn)
    for i,x in enumerate(tsret["Today"]):
        if (abs(x) < 0.0001):
            tsret["Today"][i] = 0.0001

    # Create the lagged percentage returns columns
    for i in range(0, lags):
        tsret["Lag%s" % str(i+1)] = \
                      tslag["Lag%s" % str(i+1)].pct_change()*100.0

    # Create the "Direction" column (+1 or -1) indicating an up/down day
    tsret["Direction"] = np.sign(tsret["Today"])
    tsret = tsret[tsret.index >= start_date]

    return tsret

if __name__ == "__main__":
    # Create a lagged series of the S&P500 US stock market index
    snpret = create_lagged_series(
        "^GSPC", datetime.datetime(2001,1,10),
        datetime.datetime(2005,12,31), lags=5
        )

    # Use the prior two days of returns as predictor
    # values, with direction as the response
    X = snpret[["Lag1", "Lag2"]]
    y = snpret["Direction"]

    















