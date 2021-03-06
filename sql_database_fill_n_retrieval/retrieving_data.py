#!/usr/bin/python
# -*- coding: utf-8 -*-

# retrieving_data.py

import pandas as pd
import mysql.connector as mdb
import db_connection_info

db_host = db_connection_info.db_host
db_user = db_connection_info.db_user
db_pass = db_connection_info.db_pass
db_name = db_connection_info.db_name

if __name__ == "__main__":
    # Connect to the MySQL instance
    #con = mdb(dbci.db_host, dbci.db_user, dbci.db_pass, dbci.db_name)
    con = mdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name)

    # Example using Google historical data
    sql = """   select dp.price_date, dp.adj_close_price
                from symbol as sym
                inner join daily_price as dp
                    on dp.symbol_id = sym.id
                    where sym.ticker = 'GOOG'
                    order by dp.price_date ASC; """

    # create a pandas dataframe from the SQL query
    goog = pd.read_sql_query(sql, con=con, index_col=b'price_date')

    # Output the dataframe tail
    print(goog.tail())
