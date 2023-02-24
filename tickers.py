
import matplotlib.pyplot as plt
from config import IEX_API_Key
import boto3
import pandas as pd


pd.__version__
tickers = [
    'JPM',
    'MS',
    'WFC',
    'GS',
]

ticker_string =''

for ticker in tickers:
    ticker_string += ticker
    ticker_string += ','

ticker_string = ticker_string[:-1]

endpoints = 'chart'
years = '5'

HTTP_request = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={ticker_string}&types={endpoints}&range={years}y&token={IEX_API_Key}'

bank_data = pd.read_json(HTTP_request)

series_list = []

for ticker in tickers:
    series_list.append(pd.DataFrame(bank_data[ticker]['chart'])['close'])

series_list.append(pd.DataFrame(bank_data[ticker]['chart'])['date'])

column_names = tickers.copy()
column_names.append('Date')

bank_data = pd.concat(series_list, axis=1)

bank_data.columns = column_names
bank_data.set_index('Date', inplace = True)

fig, axs = plt.subplots(nrows=2, ncols=2, constrained_layout=False)

##################################################
plt.subplot(2,2,1)
plt.boxplot(bank_data)
plt.title('Boxplot of Bank Stock Prices (5y Lookback)')
plt.xlabel('Bank')
plt.ylabel('Stock Prices')

ticks = range(1, len(bank_data.columns) + 1)
labels = list(bank_data.columns)
plt.xticks(ticks, labels)

##################################################
plt.subplot(2,2,2)

dates = bank_data.index.to_series()
dates = [pd.to_datetime(d) for d in dates]
WFC_stock_prices = bank_data['WFC']

plt.scatter(dates, WFC_stock_prices)
plt.title("Wells Fargo (5Y Lookback)")
plt.ylabel("Stock Price")
plt.xlabel("Date")

##################################################
plt.subplot(2,2,3)

dates = bank_data.index.to_series()
dates = [pd.to_datetime(d) for d in dates]
GS_stock_prices = bank_data['GS']

plt.scatter(dates, WFC_stock_prices)
plt.title("Goldman Sachs (5Y Lookback)")
plt.ylabel("Stock Price")
plt.xlabel("Date")

##################################################
plt.subplot(2,2,4)

plt.hist(bank_data, bins = 30)
plt.legend(bank_data.columns,fontsize=10)
plt.title("Daily Closing Stock Prices (5Y Lookback)")
plt.ylabel("Observations")
plt.xlabel("Stock Prices")

plt.tight_layout()

plt.savefig('bank_data.png')
# Send file to AWS S3 bucket

s3 = boto3.resource('s3')
s3.meta.client.upload_file('bank_data.png', 'iex-vis', 'bank_data.png', ExtraArgs={'ACL':'public-read'})