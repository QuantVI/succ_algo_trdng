#!/usr/bin/python
# -*- coding: utf-8 -*-

# snp_forecast.py

import pandas as pd
# from sklearn.qda import QDA # this is for Python 2
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA

# Since this is in the forecaster folder, we preface imports
# with the folder name for the file related to our engine.

from engine.strategy import Strategy
from engine.event import SignalEvent
from engine.backtest import Backtest
from engine.data import HistoricCSVDataHandler
from engine.execution import SimulatedExecutionHandler
from engine.portfolio import Portfolio

# create_lagged_series is a function within forecast.py
# forecast.py is in the forecaster folder, with this script
from forecast import create_lagged_series

class SPYDailyForecastStrategy(Strategy):
    """
    S&P500 forecast straegy. It uses a Quadratic Discriminant Analyzer
    to predict the returns for a subsequent time periods
    and then generated long/exit signals based on the prediction.
    """
