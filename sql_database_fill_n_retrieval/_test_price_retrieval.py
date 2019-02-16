# _test_price_retrieval.py
# should be in same directory as the file without _test_

import price_retrieval as pr

# A list of output messages
om = ['\n\tTest {} has no specific message.\n']

# # # # Test Message Area # # # #
m1 = '''\n\t[01] Tesiting obtain_list_of_db_tickers()
It will put all tickers from the db into a list, tupled with their db ID.
\n'''

m2 = ''

m3 = '''\n\t[03] all_tickers[28] should be (1051, 'AMZN') for Amazon.
We'll try to retrieve some Amazon data from Yahoo! Finance.
The item returned should be a Pandas DataFrame.

This may fail due to Yahoo! Finance timeouts. For example

\t Unable to read URL: https://query1.finance.yahoo.com/v7/finance/download/AMZN?period1=1546297200&period2=1550357999&interval=1d&events=history&crumb=.BQ%5Cu002FwvsdaZu
\n

Feel free to retry.
\n'''

# add test message to output message list, in order.
om.append( m1 )
om.append( m2 )
om.append( m3 )


# tm : Test Message function
# making it easier to get a test message print for each test
def tm(test_number, message_list = om):
    if test_number < len(message_list):
        if message_list[test_number] == '':
            # the message is empty tring
            print(message_list[0].format(test_number))
        else:
            print(message_list[test_number])
    else:
        print(message_list[0].format(test_number))


######################
##### Tests Area #####

#1
tm(1)
all_tickers = pr.obtain_list_of_db_tickers()

#2
tm(2)
print(all_tickers[20:40])

#3
tm(3)
amzn_tckr = all_tickers[28][1]
s2019 = pr.datetime.datetime(2019,1,1)

some_data = pr.get_daily_historic_data_yahoo(amzn_tckr, start_date=s2019)
print(some_data.head())

