#!/usr/bin/python
# -*- coding: utf-8 -*-

# price_retrieval.py

import datetime
import warnings

import mysql.connector as mdb
import requests

#import pandas_datareader.data as web
import time
import calendar

# documentation
DOCUMENTATION = """
2019-12-13 update
    due to issues with pandas datareader, we will download
    yahoo finance data in a more manual way.

A sample download URL for the S&P 500, tick ^GSPC, looks like this:

https://query1.finance.yahoo.com/v7/finance/download/%5EGSPC?period1=1544717379&period2=1576253379&interval=1d&events=history&crumb=tdXtB.G0KQQ

Using the calendar module, we can convert a time tuple into a POSIX timestamp.
One problem is that it appears the URL contains a time-sensitive cookie,
    such as: crumb=tdXtB.G0KQQ
Thus crumb has to be obtained at some point, and used for subsequent downloads.
It's unknow how long the crumb is good for. However, some manual exploration in downloading quotes
confirmed that even if you open a new tab/window and go fina a different ticker to download
the crumb is the same. Can we capture this part of the url by using the requests module?
"""


# Connect to the MySQL instance
db_host = 'localhost'
db_user = 'sec_user'
db_pass = 'password'
db_name = 'securities_master'
con = mdb.connect(host=db_host,
                  user=db_user,
                  passwd=db_pass,
                  db=db_name)

def obtain_list_of_db_tickers():
    """ Obtain a list of the ticker symbols in the database."""
    cur = con.cursor()
    cur.execute("SELECT id, ticker FROM symbol")
    data = cur.fetchall()
    con.close()
    # return a list of tuples of id and ticker
    return [(d[0], d[1]) for d in data]
    
#z = obtain_list_of_db_tickers()

def get_daily_historic_data_yahoo( \
    ticker,
    start_date=datetime.datetime(2000,1,1),
    end_date=datetime.datetime.today()):
    # print(start_date,end_date)
    """Obtains data from Yahoo Finance, and returns a list of tuples.

    ticker: Yahoo Finance ticker symbol, e.g. "GOOG" for Google, Inc.
    start_date: Start date in (YYYY, M, D, H, m, s, ms)
    end_date: End date in (YYYY, M, D, H, m, s, ms)"""

    dt_rng = (calendar.timegm(start_date),
                  calendar.timegm(end_date) )

    # try connecting to Yahoo! Finance and obtaining the data.
    # On failure, print an error message.

    try:
        # change things like BRK.B to BRK-B
        clean_ticker = ticker.replace("_","-")
        clean_ticker = clean_ticker.replace(".","-")

        # URL Creation
        u1 = f"https://query1.finance.yahoo.com/v7/finance/download/"
        u2 = f"{ticker}?period1={dt_rng[0]}&period2={dt_rng[1]}"
        u3 = f"&interval=1d&events=history&crumb="

        # pandas dataframe of the historical data

        

        
        return yf_data
    except Exception as e:
        print("Could not download Yahoo data: %s" %e)

def insert_daily_data_into_db(data_vendor_id, symbol_id, daily_data):
    """
    Takes a dataframe of daily data and adds it to the MySQL database.
    Appends the vendor ID and symbol ID to the data.

    daily_data: pandas dataframe of OHLC data (with adj_close and volume)
    """

    # Create the time now
    now = datetime.datetime.now()

    # Amend the data to include the vendor ID and symbol ID
    # use df['new_col'] = 'repeat string in every row'
    # to add new columns with those ids
    
