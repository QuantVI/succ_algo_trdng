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

DOCUMENTATION+= """
2020-02-05
I've noticed that the "crumb", an identifier/token is the same for both
the S&P500 and for the Russell 2000. Moreover, I'm seeing the same crumb
as I did on 2019-12-13. This might mean that the crumb is dtermine via
unique IP/device. If so, I should be able to append the crumb to each URL
and download the data.

using _test_price_retrieval.py, verified obtain_list_of_db_tickers() works.


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
    end_date: End date in (YYYY, M, D, H, m, s, ms)

    ~~~ A note on dthe date ~~~
    1. When we create datetime.datetime(2019,1,1) we get:
        datetime.datetime(2019,1,1,0,0)
    2. We must then get the timetuple() of this which is:
        s2019.timeetuple() #where s2019 is as in #1
        -> time.struct_time(tm_year= 2019, tm_mon=1, tm_day=1, tm_houtr=0,
                    tm_min=0, tm_sec=0, tm_wday=1, tm_yday=1, tm_isdst=-1)
    3. We can now call timegm() on this time tuple
        calendar.timegm(s2019.timetuple())
        -> 1546300800
    4. This POSIX-like time goes into the Yahoo!Finance URL.
        It represents the start of that day.
        Thus our enddate would not include that business day, since
        the POSIX would be the start of that day.

    ~~ Crumb and Cookie ~~~
    We also need a valid cookie for our session. This person
    https://stackoverflow.com/q/56698011/1327325
    encountered a similar problem. We can use the code to apply the cookie to
    the request.
    """

    # turn date into date tuple
    dt_tuples = (start_date.timetuple(), end_date.timetuple())

    # turn date tuple into POSIX time
    dt_rng = (calendar.timegm(dt_tuples[0]),
                  calendar.timegm(dt_tuples[1]) )

    # attempt to get valid cookie
        # we might want to return the cookie also.
    def get_a_valid_cookie(standard_url=1):
        pass

    # try connecting to Yahoo! Finance and obtaining the data.
    # On failure, print an error message.

    try:
        # change things like BRK.B to BRK-B
        clean_ticker = ticker.replace("_","-")
        clean_ticker = clean_ticker.replace(".","-")

        # URL Creation
        u1 = f"https://query1.finance.yahoo.com/v7/finance/download/"
        u2 = f"{ticker}?period1={dt_rng[0]}&period2={dt_rng[1]}"
        u3 = f"&interval=1d&events=history&crumb=tdXtB.G0KQQ"
        uF = f"{u1}{u2}{u3}"
        print(uF)
        
        # pandas dataframe of the historical data

        resp = requests.get(uF)

        
        #return yf_data
        return resp
    
    except Exception as e:
        print("Could not download Yahoo data: \n\t%s" %e)

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


# `-=`-=`-=`-=`-=`-=`-=`-=`-=`-=`-=
all_tickers = obtain_list_of_db_tickers()

print(all_tickers[20:40],'\n')

amzn_tckr = all_tickers[28][1]

print(amzn_tckr,'\n')

s2019 = datetime.datetime(2019,1,1)

some_data = get_daily_historic_data_yahoo(amzn_tckr, start_date=s2019)
