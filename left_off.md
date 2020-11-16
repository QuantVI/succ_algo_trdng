# Where I left-off
### Edit this file after each session, to make it easier to resume working next time.


#### Possible things to include

- what did you last do
- what did you test?
- where did you test it?
- what worked or didn't?
- what to do next time?
- __what page in the book is this?__

this is like "relase notes"

2019-02-15

##### recap
it seems the last things I did was make a prototype file for price retrival.py

in the book, `requests` is used, but we can use `pandas.datareader` which also has a way, though obscrued, to read from Yahoo! Finance without supplying the direct url for manipulation.

Book Page 56 (65/208) "Price Retrieval"

we will continue working with the _price retrieval_ file.

##### intermediate
considering having an entire test directory.

##### conclusion
need to complete price retrieval to store things in databse. However, need to test current functionality first.

2019-02-16

##### recap
need to test `price_retrieval.py` functionality.

##### intermediate
for now, i will test files using a (possibly matching) single file. so for each .py used in the applicaiton, there will be another .py with tests for that file.

##### conclusion
with the test file in place, the next thing to do would be to add the approprate code to put the dataframe data into the MySQL database, symbol by symbol.

2019-12-13
##### recap
needed to test price_retrieval

##### intermediate
`import price_retrieval as pr` in my test file causes an issue. This has been traced to `import pandas_datareader.data as web` not working. The error is `ImportError: cannot import name 'StringIO'`.

This worked previously. However, we wil have to revert the the books verions, or midification thereof, to download data from Yahoo!Finance.

`_test_price_retrieval.py` can be ignored.

In the original price_retrieval.py, you could get Yahoo!Finance data from [ichart.finance.yahoo.com](). This is no longer the case. The new type of URL uses Unix timestamps.

2020-02-05
Working with price_retrieval.py

1. We will have to hit a normal URL, sush as this one for the [S&P 500 (^GSPC)](https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC).

1. However, I've noticed that the "crumb", an identifier/token is the same for both the S&P500 and for the Russell 2000. Moreover, I'm seeing the same crumb as I did on 2019-12-13. This might mean that the crumb is dtermine via unique IP/device. If so, I should be able to append the crumb to each URL and download the data.

1. Thankfully, it looks like the 500 constituent stocks have normal ticker representations in general and on Yahoo!Finance. This means that while the S&P500 is ^GSPC as a ticker, and %5GSPC in a URL, we won't need these types of conversions for the stocks.

1. Additional problem of needing a valid cookie. Found a possible solution on [here](https://stackoverflow.com/q/56698011/1327325).

1. Yahoo!Finance is a no-go. We will switch to a full API version instead of trying to web-scrape, as this method has become highly protected.

1. After a random retry, I was able to get pandas datareader installed. It's been broken and I haven't been able to reinstall it for a while. Now we are back to the 2nd method for data ingestion.

1. historical data retrieval is working, Moving to code the storage of data in the MySQL db.

2020-02-06

1. Have moved to the daily quotes storage pieces. In the original, the fetched data was more or less in text format. After using .split() its indexable. We however, have fetched directly into a DataFrame, and must retrieve the right quantitiy of each row differently.
2. Some tiker symbols will either not be in the Yahoo Finance data, or given an error when being retrieved. We will manually ignore these tickers. 
  3. Since the `executemany()` statement is used to insert data into the database, if even one symbol is missing data, then nothing is commited to the db.
  4. This is okay, since we'd otherwise have duplicate data if we start the process over again. However, it does have other problems. A more robust solution would check the db for data for the current time(span) for a symbol, and also remove irretrievable symbols from the current list of symbols we need to download data for.
  5. Then the process could retry until successful, as we would either remove all symbol for mthe list as unobtainable, see that the db already has todays (span of) data, or get and insert everything.
6. Changed two method to print the bad ticker and continue. Needing to restart the process 280+ tickers in is crazy.
7. Have to redo the entire pull becuase I need ot use `commit()` to flush full transaction to the db. Closing the connection is not enough.
8. While 11 tickers have been left out, data was succesfully downloaded from Yahoo Finance and saved intot he MySQL db. A total of 2,267,811 rows of data for 494 companies dating from 2000-01-01 until 2020-02-06. This means `price_retrieval.py` is complete and successful.
9. Next. From Chp 8 on. Decide whether or not to make Quandl data pull. Skip IQFeed section, and continuous futures.
10. continued 2020-06-20



2020-11-16

- Need to write `retrieving_data.py`
  - this will also go into the sql_db ...folder

