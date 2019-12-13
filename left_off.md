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