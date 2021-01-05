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
  - completed
- Also created the db and tables in the Windows system
- Got symbols
- Added S&P 500 constituent data (yr 2000+)  into the database. Of 505, Missing:
  - Could not make data rows for ticker 315
  - Could not make data rows for ticker 322
  - Could not make data rows for ticker 325
  - Could not make data rows for ticker 326
  - Could not make data rows for ticker 338
  - Could not make data rows for ticker 340
  - [315,322,325,326,338,340]
  - (315, 'MGM')
    (322, 'MDLZ')
    (325, 'MS')
    (326, 'MOS')
    (338, 'NEE')
    (340, 'NKE')
  - not a big deal
- Start in 8.2 (pg 63)

2020-11-17

- quandl data on futures is now premium. skip
- skip DTN IQFeed
- go to Ch.9 --> re-read, with notes
- tested `retrieving_data.py` - working

2020-12-28

- Chapter 10 - Time Series Analysis
  - 10.1 Testing for Mean Reversion; with example standalone code
  - 10.2 Testing for Stationarity; with standalone code for Hurst exponent
  - 10.3 Cointegration; with cointegrated Augmented Dickey-Fuller Test code **[cadf.py]**
  - 10.4 Why Statistical Testing?
- Chapter 11 - Forecasting
  - 11.1 Measuring Forecasting Accuracy; Hit Rate and Confusion Matrix
  - 11.2 Factor Choice; Lagged Price Factors and Volume, External Factors
  - 11.3 Classification Models
    - Logistic Regression
    - Discriminant Analysis
    - Support Vector Machines
    - Decision Trees and Random Forests
    - Principal Components Analysis
    - Which Forecaster?
  - 11.4 Forecasting Stock Index Movement
    - Python Implementations: **[forecast.py]**

Part V

- Chapter 12 - Performance Measurement
  - 12.1 Trade Analysis
    - Total & Average Period - PnL, Max/Min Period Profit/Loss, Average Period Profit/Loss
    - Winning/Losing Periods, Percentage Win/Loss Periods
  - 12.2 Strategy and Portfolio Analysis; Returns, Risk/Reward, and Drawdown - Analysis
    - __[sharpe.py]__
- Chapter 13 - Risk and Money Management
  - 13.1 Sources of Risk: Strategy, Portfolio, Counterparty, Operational - Risk
  - 13.2 Money Management
  - 13.3 Risk Management
  - 13.4 Advantages and Disadvantages
    - Methods of Calculation, Variance-Covariance Method
    - __[var.py]__ for Value-at-Risk

Part VI - Automated Trading

- Chapter 14 - Event-Driven Trading Engine Implementation
  - 14.1 Event-Driven Software
  - 14.2 Compound Objects
    - Event, Event Queue, DataHandler, Strategy, Portfolio, ExecutionHandler, Backtest
    - start of __[event.py]__ for all event types
    - __[data.py]__ the data-handler
    - __[strategy.py]__ for calculation on market data
    - __[performance.py]__
    - __[portfolio.py]__ - bulk of the code is here
    - __[execution.py]__

2020-12-31

- Planning to skip __cadf.py__  (Ch 10) as it doesn't seem to be linked overall
- Next would be to write __forecast.py__
  - Figure out if this is part of a large structure, such as to have a folder for it
  - Review Chapter 11 where the code comes from.
  - Notes in the code about the math involved will be helpful

2020-01-04

Still reviewing Chapter 11. Ready to start 11.4 - implementation of __forecast.py__

2020-01-05

Started on __forecast.py__. No _compile_ errors.

Continuing with __forecast.py__

