#!/usr/bin/python
# -*- coding: utf-8 -*-

# insert_symbols.py

import datetime
from math import ceil

import bs4
import mysql.connector as mdb
import requests

def obtain_parse_wiki_snp500():
    """
    Download and parse the Wikipedia list of S&P500
    constituents using requests and BeautifulSoup.

    Returns a list of tuples for to add to MySQL.
    """
    # Stores the current time for the created_at record
    now = datetime.datetime.utcnow()

    # Use request and BeautifulSoup to download the list
    # of the S&P500 companies and obtain the symbol table
    response = requests.get(
        "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        )
    soup = bs4.BeautifulSoup(response.text,'html')
    
    # This selects the first table, using CSS Selector syntax
    # and then ignore the header row ([1:])
    symbolslist = soup.select('table')[0].select('tr')[1:]
    
    # Obtain the symbol information for each row
    # in the S&P500 constituent table
    symbols = []
    for i, symbol in enumerate(symbolslist):
        tds = symbol.select('td')

        symbols.append(
            (
                tds[0].select('a')[0].text, # Ticker
                'stock',
                tds[1].select('a')[0].text, # Name
                tds[3].text, # sector
                'USD', now, now
                )
            )
    return symbols

def insert_snp500_symbols(symbols):
    """
    Insert the S&P500 symbols into the MySQL database.
    """
    # Connect to the MySQL database
    import db_connection_info as dbci
    #db_host = 'localhost'
    #db_user = 'sec_user'
    #db_pass = 'password'
    #db_name = 'securities_master'
    con = mdb.connect(
        host=dbci.db_host, user=dbci.db_user,
        passwd=dbci.db_pass, db=dbci.db_name
        )

    # Create the insert strings
    column_str = """ticker, instrument, name, sector, currency,
                created_date, last_updated_date"""
    insert_str = ("%s, " * 7)[:-2]
    final_str = "INSERT into symbol (%s) VALUES (%s)" % \
                (column_str, insert_str)

    # Using the MySQL connection, carry out an INSERT INTO
    # for every symbol
    cur = con.cursor()
    cur.executemany(final_str,symbols)
    con.commit()
    con.close()

    print(final_str)

if __name__ == "__main__":
    symbols = obtain_parse_wiki_snp500()
    insert_snp500_symbols(symbols)
    print("%s symbols were successfully added." % len(symbols))
