#!/usr/bin/python
# -*- coding: utf-8 -*-

# price_retrieval.py

import datetime
import warnings

import mysql.connector as mdb
import requests

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

# sample url to download Microsoft dailt historical data
# from 2018-01-13 to 2019-01-13
    # https://query1.finance.yahoo.com/v7/finance/download/MSFT?
    # period1=1544723038&period2=1547401438&interval=1d
    # &events=history&crumb=IMF/v130KPT

def get_daily_historic_data_yahoo( \
    ticker, start_date=(2000,1,1),
    end_date=datetime.date.today().timetuple()[0:3]):
    # print(start_date,end_date)
    """Obtains data from Yahoo Finanace returns, and a list of tuples.

    ticker: Yahoo Finance ticker symbol, e.g. "GOOG" for Google, Inc.
    start_date: Start date in (YYYY, M, D) format
    end_date: End date in (YYYY, M, D) format"""

    # Construct the Yahoo URL with the correct integer query parameters
    # for start and end dates. Note that some parameters are zero-based.

    ticker_tup = (
        ticker, start_date[1]-1, start_date[2], start_date[0],
        end_date[1]-1,end_date[2],end_date[0])
    yahoo_url = "http://ichart.finance.yahoo.com/table.csv"
    yahoo_url+= "?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s"
    yahoo_url = yahoo_url % ticker_tup

    print(yahoo_url)
