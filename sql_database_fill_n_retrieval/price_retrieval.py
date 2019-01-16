#!/usr/bin/python
# -*- coding: utf-8 -*-

# price_retrieval.py

import datetime
import warnings

import mysql.connector as mdb
import requests

import pandas_datareader.data as web
import time

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
    end_date=datetime.datetime.today() ):
    # print(start_date,end_date)
    """Obtains data from Yahoo Finanace returns, and a list of tuples.

    ticker: Yahoo Finance ticker symbol, e.g. "GOOG" for Google, Inc.
    start_date: Start date in (YYYY, M, D) format
    end_date: End date in (YYYY, M, D) format"""

    # use pandas_datareader.data with the correct parameters
    # for start and end dates.

    # try connecting to Yahoo! Finance and obtaining the data.
    # On failure, print an error message.

    try:
        # change things like BRK.B to BRK-B
        clean_ticker = ticker.replace("_","-")
        clean_ticker = clean_ticker.replace(".","-")

        # pandas dataframe of the historical data
        yf_data = web.DataReader(clean_ticker,'yahoo',
                                 start_date,end_date)
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
    
