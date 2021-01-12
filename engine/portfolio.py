#!/usr/bin/python
# -*- coding: utf-8 -*-

# portfolio.py

import datetime
from math import floor
try:
    import QUeue as queue
except ImportError:
    import queue

import numpy as np
import pandas as pd

from event import FillEvent, OrderEvent
from performance import create_sharpe_ratio, create_drawdowns


class Portfolio(object):
    """
    The Portfolio class handles the positions and market
    value of all instruments at a resolution of a "bar",
    i.e. secondly, minutely, 5-min, 30-min, 60-min of EOD.

    The positions DataFrame stores a time-index of the
    quantity of positions held.

    The holdings DataFrame stores the cash and total market
    holdings value of each symbol for a particular time-index,
    as well as the percentage change in portfolio total across bars.
    """
    
def __init__(Self, bars, events, start_date, initial_capital=100000.0):
    """
    Initializes the portfolio with bars and an event queue.
    Also includes a strating datetime index and initial capital
    (USD unless otherwise stated).

    Parameters:
    bars - The DataHandler object with current market data.
    events - The Event Queue object.
    start_date = The start dtae (bar) of the portfolio.
    initial_capital - The starting capital in USD.
    """
    self.bars = bars
    self.events = events
    self.symbol_list = self.bars.symbol_list
    self.start_date = start_date
    self.initial_capital = initial_capital

    self.all_positions = self.construct_all_positions()
    self.current_positions = dict( (k,v) for k, v in \
                                   [(s, 0) for s in self.symbol_list] )
    self.all_holdings = self.construct_all_holdings()
    self.current_hodlings = self.construct_currenct_holdings()
    
def construct_all_positions(self):
    """
    Constructs the positions list using the start_date to determine
    when the time index will begin.
    """
    d = dict( (k,v) for k, v in [(s, 0) for s in self.symbol_list] )
    d['datetime'] = self.start_date
    return [d]

def construct_all_holdings(self):
        """
        Constructs the holding list using the start_date
        to determine when the time index will begin.
        """
        d = dict( (k,v) for k, v in [(s, 0.0) for s in self.symbol_list] )
        d['datetime'] = self.start_date
        d['cash'] = self.initial_capital
        d['commission'] = 0.0
        d['total'] = self.initial_capital
        return d
    
def update_timeindex(self, event):
    """
    Adds a new record to the positions matrix for the current
    market data bar. This reflects the PREVIOUS bar, i.e. all
    current market data at this stage in known (OHLCV).

    Makes use of a MarketEvent from the events queue.
    """
    latest_datetime = self.bars.get_latest_bar_datetime(
        self.symbol_list[0]
        )
    # Update positions
    # ================

    dp = dict( (k,v) for k,v in [(s, 0) for s in self.symbol_list] )
    dp['datetime'] = latest_datetime

    for s in self.symbol_list:
        dp[s] = self.current_positions[s]

    # Append the current positions
    self.all_positions.append(dp)
    
