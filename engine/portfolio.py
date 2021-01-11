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
    """
    
