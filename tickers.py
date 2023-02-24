import pandas as pd
from config import IEX_API_Key


tickers = [
    'JPM',
    'BAC',
    'C',
    'WFC',
    'GS',
]

ticker_string =''

for ticker in tickers:
    ticker_string += ticker
    ticker_string += ','

ticker_string = ticker_string[:-1]

endpoints = 'chart'
years = '10'

HTTP_request = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={ticker_string}&types={endpoints}&range={years}y&token={IEX_API_Key}'

bank_data = pd.read_json(HTTP_request)






