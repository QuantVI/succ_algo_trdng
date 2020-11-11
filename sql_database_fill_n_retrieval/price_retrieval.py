#!/usr/bin/python
# -*- coding: utf-8 -*-

# price_retrieval.py

import datetime
import warnings

import mysql.connector as mdb
import requests

import pandas_datareader.data as web
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

DOCUMENTATION+= """
2020-02-05
I've noticed that the "crumb", an identifier/token is the same for both
the S&P500 and for the Russell 2000. Moreover, I'm seeing the same crumb
as I did on 2019-12-13. This might mean that the crumb is dtermine via
unique IP/device. If so, I should be able to append the crumb to each URL
and download the data.

using _test_price_retrieval.py, verified obtain_list_of_db_tickers() works.

2020-02-06
Randomly tried reinstalling pandas.datareader from pip, and it worked.
The elongated workaround of using an API from a different vendor may not
be needed now. Reverting the code to use datareader.

Try Except was added to the db writer as well. Since the Yahoo pull may return
no data for a symbol, the db write can't attempt to make rwos from NULL data.

Moreover, both of the Try Except, print the error, and use `pass` to move on.
I've taken not of bad symbols, and remove them in subsequent runs, by adding
them to an ignore list which excludes them via filtering all tickers.
"""


# Connect to the MySQL instance
db_host = 'localhost'
db_user = 'sec_user'
db_pass = 'password'
db_name = 'securities_master'
# Moving global connection. will conect as needed per function.
#con = mdb.connect(host=db_host,
#                  user=db_user,
#                  passwd=db_pass,
#                  db=db_name)

def obtain_list_of_db_tickers():
    """ Obtain a list of the ticker symbols in the database."""
    # start individual connection
    con = mdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name)
    # use connection
    cur = con.cursor()
    cur.execute("SELECT id, ticker FROM symbol")
    data = cur.fetchall()
    # close connection
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
    end_date: End date in (YYYY, M, D, H, m, s, ms)
    """

    # try connecting to Yahoo! Finance and obtaining the data.
    # On failure, print an error message.

    try:
        # change things like BRK.B to BRK-B
        clean_ticker = ticker.replace("_","-")
        clean_ticker = clean_ticker.replace(".","-")
        
        # pandas dataframe of the historical data

        yf_data = web.DataReader(clean_ticker,"yahoo",start_date,end_date)
        time.sleep(0.05)
        
        return yf_data
    
    except Exception as e:
        print("Could not download Yahoo data: \n\t%s" %e)
        pass

    # the returned dataframe will have its values taken and put into MySQL.

def insert_daily_data_into_db(data_vendor_id, symbol_id, daily_data):
    """
    Takes a dataframe of daily data and adds it to the MySQL database.
    Appends the vendor ID and symbol ID to the data.

    daily_data: pandas dataframe of OHLC data (with adj_close and volume)
    """

    # Create the time now
    now = datetime.datetime.now()
    # Amend the data to include the vendor ID and symbol ID
    # Generates a tuple of length 2:
        # 0: TimeStamp : <class 'pandas._libs.tslibs.timestamps.Timestamp'>
        # 1: Series with our 6 columns : <class 'pandas.core.series.Series'>
            # Series indexable by int
            # Series indexable by name
    EXAMPLE_A = """
        >>> sdl[0][0]
        Timestamp('2020-01-02 00:00:00')
        >>> sdl[0][1]
        High         1.898010e+03
        Low          1.864150e+03
        Open         1.875000e+03
        Close        1.898010e+03
        Volume       4.029000e+06
        Adj Close    1.898010e+03
        Name: 2020-01-02 00:00:00, dtype: float64
        >>> sdl[0][1][0]
        1898.010009765625
        >>> sdl[0][1]["High"]
        1898.010009765625
        """
    try:
        df_to_rows = [row for row in daily_data.iterrows()]

        # creaing the row-by-row data
        # prefer to reference by item name, than by index
        row_data = [(data_vendor_id, symbol_id, dfr[0],
                            now, now, # created and last updated dates
                            dfr[1]["Open"], dfr[1]["High"],
                            dfr[1]["Low"], dfr[1]["Close"],
                            dfr[1]["Volume"], dfr[1][5] # adj close has a space
                            ) for dfr in df_to_rows
                           ]

        # create the insert strings
        column_str = """data_vendor_id, symbol_id, price_date, created_date,
                        last_updated_date, open_price, high_price, low_price,
                        close_price, volume, adj_close_price"""
        
        insert_str = ("%s, " * 11)[:-2]
        begin_str = "INSERT INTO securities_master.daily_price ({}) VALUES ({})"
        final_str = begin_str.format(column_str, insert_str)
        
        # print('\n\t',final_str,'\n')

        # Using a MyQL connection, execute the INSERT statement for every symbol
        con = mdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name)
        cur = con.cursor()
        cur.executemany(final_str, row_data)
        # quite necessary
        con.commit()
        cur.close()
        con.close()

    except Exception as f:
        print(f"Could not make data rows for ticker {symbol_id}")
        pass



# [][][][][][][][][][]
# Main Area
# [][][][][][][][][][]

if __name__ == "__main__":
    # Loop over tickers and insert the daily historical data into the db
    tickers = obtain_list_of_db_tickers()
    # Manually creating a list of tickers to ignore
    skip_tickers = ["APC","BHGE","DWDP","HRS","HCP","LLL","NFX","RHT",
                    "SYMC","TMK","TSS"]
    # NFX seemed to be a date error. Probably didn't exist as early as 2000.


    tickers = [tkpair for tkpair in tickers if tkpair[1] not in skip_tickers]
    
    lentickers = len(tickers)
    prntstr_1 = "Adding data for {}: {} out of {}"
    prntstr_2 = "Successfully added Yahoo!Finance pricing data to DB."
    for i, t in enumerate(tickers):
        print(prntstr_1.format(t[1], i+1, lentickers))

        # with no other arugment, we pull from the year 2000, forward.
        yf_data = get_daily_historic_data_yahoo(t[1])
        # Pause, so we don't hit the end point too quickly
        time.sleep(0.05)
        # Yahoo!Finance is consdered vendor 1
        insert_daily_data_into_db('1', t[0], yf_data)

    print(prntstr_2)

# `-=`-=`-=`-=`-=`-=`-=`-=`-=`-=`-=
# Test Area
# `-=`-=`-=`-=`-=`-=`-=`-=`-=`-=`-=

def run_tests(fr=1,to=None):
    all_tests=[]
    def test_1():
        all_tickers = obtain_list_of_db_tickers()
        print(all_tickers[20:40],'\n')
        
        amzn_tckr = all_tickers[28][1]
        print(amzn_tckr,'\n')
        
        s2019 = datetime.datetime(2020,1,1)
        
        some_data = get_daily_historic_data_yahoo(amzn_tckr, start_date=s2019)

        print(some_data.head())

    all_tests.append(test_1)

    def test_2():
        """returns something if print(final_str) uncommented in
        insert_daily_data_into_db()
        """
        all_tickers = obtain_list_of_db_tickers()
        amzn_tckr = all_tickers[28][1]
        s2020 = datetime.datetime(2020,1,1)
        some_data = get_daily_historic_data_yahoo(amzn_tckr, start_date=s2020)
        rez = insert_daily_data_into_db(9999, 'TEST02', some_data)
        return {'t':all_tickers,
                'dt':s2020,
                'sdata':some_data,
                'test_rez':rez}
    all_tests.append(test_2)
        
    
    if to is None:
        for t in all_tests: return t()
    else:
        return all_tests[fr-1]()
