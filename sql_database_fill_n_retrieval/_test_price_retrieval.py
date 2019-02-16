# _test_price_retrieval.py
# should be in same directory as the file without _test_

import price_retrieval as pr

# A list of output messages
o_m = ['\n\tTest {} has no specific message.\n']

o_m.append('''\tTesiting obtain_list_of_db_tickers()
It will put all tickers from the db into a list, tupled with their db ID.\n
''')

def test_message(test_number):
    if test_number < len(o_m):
        print(o_m[test_number])
    else:
        print(o_m[0].format(test_number))

##### Tests Area #####

#1
test_message(10)
all_tickers = pr.obtain_list_of_db_tickers()

#2
print(all_tickers[20:40])

#3
