# Code Changes
Attempt to keep track of, mostly, major changes to the code fomr the book.

Due to the fact that both the internet, and various software, etc are constantly evolving, both minor and major changes to the given code were needed in order to get things working and deployed.

## Major
### In General
###### sql_conn:
I have to use a different connector to MySQL. The book uses the package `MySQLdb`. In its place, I use `mysql.connector`.

###### yahoo_finance:
The url for downloading csvs from Yahoo! Finance has changed. Instead of direct construction of this URL, I've decided to employ a package for this.

The package/module is `pandas_datareader.data`. I used it in a previous script, when going through some examples by Sentdex (on YouTube).

The video [Sentdex - Py4Fin vid06](https://www.youtube.com/watch?v=baCAFPHb1o4&index=6&list=PLQVvvaa0QuDcOdF96TBtRtuQksErCEBYZ) shows the module, getting data from Yahoo! Finance. Modifications to the Sentdex script include adding a retry funciton, as there's a decent rate of timeouts and errors.

### In *price_retrieval.py*
- Changes to [getting data from Yahoo! Finance](/NOTES.md#yahoo_finance)
- Due to the first change, we have dataframe not a `requests` object. Thus we insert into MySql differently - a big rewrite.

### In *insert_symbols.py*
- Changes to [db connection](/NOTES.md#sql_conn)
- The `with` functionality does not work with our connector. It's purpose is to `.close()` the connection once the indented lines of the with are completed.
- In place of `with con:`, I use, in order, `cursor`, `executemany`, `commit`, `close`.

## Minor
### MySQL database creation
A separate file was made for the creation of each table in the sql database. In the book, these were held in one ddl file called <u>securities_master.sql</u>

