from pytickersymbols import PyTickerSymbols
import requests
import json

stock_data = PyTickerSymbols()
german_stocks = stock_data.get_stocks_by_index('DAX')
uk_stocks = stock_data.get_stocks_by_index('FTSE 100')


list_german_stocks = list(german_stocks)


for stock_index in range(1, len(list_german_stocks)):
    print(list(list_german_stocks)[stock_index])


