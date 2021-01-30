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
    - _continued 2020-01-14_
    - __backtest.py__ pg 152 - 155
  - 14.3 Event-Driven Execution
    - __ib_execution.py__ - skip because we can only use  backtester
      - 156 - 161

- Chapter 15 - Trading Strategy Implementation

  - 15.1 Moving Average Crossover Strategy
    - __mac.py__  pg 164-166
  - 15.2 S&P Forecasting Trade
    - __snp_forecast.py__ pg 168-171
  - 15.3 Mean-Reverting Equity Pairs Trade
    - __intraday_mr.py__ pg 173-178
  - 15.4 Plotting Performance
    - __plot_performance.py__ pg 179-180

- Chapter 16 - Strategy Optimization

  - 16.1 Parameter Optimization
  - 16.2 Model Selection
    - __train_test_split.py__ pg 183-185
    - __k_fold_cross_val.py__ pg 186-187
    - __grid_search.py__ pg 189-190
  - 16.3 Optimizing Strategies
    - __intraday_mr.py__ pg 191-192
    - __backtest.py__ revision pg 192-193
    - __plot_sharpe.py__ pg 195-196
    - __plot_drawdown.py__ pg 196

- ## Bibliography

  - DONE !





2020-12-31

- Planning to skip __cadf.py__  (Ch 10) as it doesn't seem to be linked overall
- Next would be to write __forecast.py__
  - Figure out if this is part of a large structure, such as to have a folder for it
  - Review Chapter 11 where the code comes from.
  - Notes in the code about the math involved will be helpful

2021-01-04

Still reviewing Chapter 11. Ready to start 11.4 - implementation of __forecast.py__



2021-01-05

Started on __forecast.py__. No _compile_ errors.

Continuing with __forecast.py__



2021-01-06

__forecast.py__ is working. Output is nearly the same. Radial SVM is supposed to differ a bit.

Now moving to __Part V__



2021-01-09

__Part V__

#### Chapter 12 Performance Measurement

Performance should be measured at multiple levels of granularity.

- Assess at the level of trades, strategies and portfolios.

- Assess
  - does strategy give consistent return? is there positive backtest performance?
  - does strategy maintain positive performance in live implementation?
  - compare multiple startegies/portfolios, to reduce opportunity cost associated with allocation
- Quantitative Analysis performance items
  - Returns - percentage gain since inception; either in a backtest or live trading environment
    - Total Return and Compound Annual Growth Rate (CAGR)
  - Drawdowns - a period of negative performance, defined from a prior high-water mark
  - Risk - specifically risk of capital loss (e.g. drawdowns), and volatility of returns (annualized stanard deviation of returns)
  - Risk/Reward Ratio - risk-adjusted returns. Quantify how much risk is taken per unit of return.
    - Sharpe Ratio, Sortino Ratio, CALMAR Ratio
  - Trade Analysis - performance at the individual trade level, versus strategy and portfolio measures above
    - Number of winning/loosing trades, mean profit per trade, win/loss ratio

Beginning __sharpe.py__

Note

> from pandas.io.data import DataReader 
>
> ##### used as
>
> ts = DataReader( symbol, "yahoo", start_date-datetime.timedelta( days = 365 ), end_date ) 

or

> import pandas.io.data as web 
>
> ##### used as
>
> arex = web.DataReader("AREX", "yahoo", start, end) 

should be

> import pandas_datareader.data as web
>
> ##### used as
>
> ts = web.DataReader( symbol, "yahoo", start_date - datetime.timedelta( days = 365 ), end_date )



The Google Finance api for DataReader doesn't work. Switching to Yahoo!

- switching to source of Yahoo! worked.
- `equity_sharpe('GOOG')` returns `0.7023895327537455`

-  `market_neutral_sharpe('GOOG', 'SPY')` returns `0.8283145638608274`



#### Chapter 13 Risk and Money Management

Intrinsic sources of risk and Extrinsic sources of risk

Strategy Risk, Portfolio Risk, Market Risk, Counterparty Risk, Operational Risk

Can review Chapter 13 later.

__var.py__ starts in 13.4

- Beginning __var.py__
- `var = var_cov_var(P, c, mu, sigma)` with P = 1e6, c = 0.99, etc returns `Value-at-Risk: $56503.11`

- This end Chapter 13 and Part V



Starting with event.py in Chapter 14

stopped end of pg 134



2021-01-10

Starting __data.py__ our Data Handler (starts on page 135)

Everything from beginning through `update_bars()` was initially tested to see the error message. This is the starting state of the DataHandler class. These functions will be filled in later.

continue from page 139 at the bottom `get_latest_bar_value`



2021-01-11

Finished most of __data.py__ up to end of page 140. Starting __strategy.py__ .

Stopped with `construct_all_holdings` on page 145. Resume from page 146, within __portfolio.py__



2021-01-12

__portfolio.py__

resume from page 146 before `# Update holdings`



2021-01-13

Finished __portfolio.py__. It "compiles". Functions not tested Moving to __exectuion.py__

Continue from page 150 with (creation of) __execution.py__

Starting __execution.py__

Finished __Executions.py__

Continue with __backtest.py__ on page 152

- finished outlines the rest of the book, above.

Continue with __backtest.py__ page 154



2021-01-17

skipping __ib_execution.py __pg 155-161

starting __mac.py__ for moving average crossover strategy

continue from  the end of __mac.py__ pg 166



2021-01-23

had to fix typos and indentation issues in a few files

- __backtest.py__
- __mac.py__

Within mac.py we will just manually download the AAPL data from Yahoo.

Within __data.py__ the `pandas.io.parsers.read_csv` which creates a _DataFrame_ does not have a `.sort()` method, but instead a `.sort_values()` method. Must specify what to sort by. Thus us of `.sort()` within the `_open_convert_csv_files()` function was changes to `.sort_values('datetime)` as there was an error stating that a _DataFrame_ doesn't (or maybe no longer) has a `.sort()` method.



Found a huge mistake

- When running __mac.py__ I got an error 

`Traceback (most recent call last):
  File "C:\Users\SSBlue\OneDrive\1_general\su_al_tr\succ_algo_trdng\engine\mac.py", line 103, in <module>
    Portfolio, MovingAverageCrossStrategy
  File "C:\Users\SSBlue\OneDrive\1_general\su_al_tr\succ_algo_trdng\engine\backtest.py", line 55, in __init__
    self._generate_trading_instances()
  File "C:\Users\SSBlue\OneDrive\1_general\su_al_tr\succ_algo_trdng\engine\backtest.py", line 73, in _generate_trading_instances
    self.initial_capital)
TypeError: object() takes no parameters`

Had to review a few files. But `generate_trading_instances`actually has to to with when we are setting the `self.portfolio` attribute within __backtest.py__. Finally, noticed this after going through many other files. The I went into __portfolio.py.__ The problem was that I didn't indent the function `def` after the Class `def` So everything below was also missing an additional indent. More importantly, this means that the Portfolio object didn't have an `__init__` function. Hence the "`object`() takes no parameters".

In __portfolio.py__ forgot to write `construct_current_holdings()` and `update_signal()` functions

After many fixes in __portfolio.py__, __mac.py__ is running. Still have an error though.

! Problem. Now that __mac.py__runs, the stats are atrocious. Return is a huge negative. Going to download the exact period for the book to compare. Some calculations may have been keyed incorrectly.

- Book period for AAPL test of __mac.py__ is 1990-01-01 to 2001-12-31

  - 1st trading day in the data is 1990-01-02 as Jan 1 there was no trading.

- Even after using the same date/data range, our results are too different.

  - There must be an issue in what was written.
  - Areas of calculation within portfolio, backtest, data and execution need to be checked
  - __mac.py__ should also be reviewed for calculation issues.




2021-01-30

Need to find the issue with __mac.py__

- __mac.py__: pg 164
  - seems okay
- __backtest.py__ pg 152
  - 



