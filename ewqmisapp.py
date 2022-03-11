import numpy as np 
import pandas as pd
import requests
import streamlit as st
import math
from scipy import stats
from statistics import mean

st.write("""
# Equal Weight Quantitative Momentum Investment Strategy

The table below shows cryptocurrencies from the list of top 200 cryptocurrencies that have increased in price the most in the last 200 days. Further, you can enter your portfolio size and obtain an equal-weight investment strategy for top 20 of these high momentum cryptocurrencies.

### Top 200 Cryptocurrencies ordered by 200D Price Return
""")

api_url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=200&page=1&sparkline=false&price_change_percentage='24h%2C7d%2C14d%2C30d%2C200d%2C1y%2C'"
data = requests.get(api_url).json()

my_columns = ['Name', 'Ticker', 'Current Price', 'Market Capitalization', '200D Price Return']
final_dataframe = pd.DataFrame(columns = my_columns) 


for i in data:
    name = i['name']
    ticker = i['symbol'].upper()
    price = i['current_price']
    market_cap = i['market_cap']
    price_change_percentage_200d = i['price_change_percentage_200d_in_currency']
    final_dataframe = final_dataframe.append(
    pd.Series(
        [
            name,
            ticker,
            price,
            market_cap,
            price_change_percentage_200d,
        ],
            index = my_columns,
    ),
        ignore_index = True
)
final_dataframe.sort_values('200D Price Return', ascending = False, inplace = True)
final_dataframe.reset_index(inplace = True)
st.dataframe(final_dataframe, 1200, 900)

st.write("""
## Equal Weight Investment Strategy for Top 20 High Momentum Cryptocurrencies

Enter the value of your portfolio to obtain an equal-weight investment distribution for top 20 high momentum cryptocurrencies from the above list.

""")
portfolio_size = st.number_input('Enter the value of your portfolio', key=1)

position_size = portfolio_size / len(final_dataframe.index)

print(position_size)




my_columns = ['Name', 'Ticker', 'Current Price', 'Market Capitalization', '200D Price Return', 'Number of Tokens to Buy']
final_dataframe = pd.DataFrame(columns = my_columns) 
for i in data:
    name = i['name']
    ticker = i['symbol'].upper()
    price = i['current_price']
    market_cap = i['market_cap']
    price_change_percentage_200d = i['price_change_percentage_200d_in_currency']
    final_dataframe = final_dataframe.append(
    pd.Series(
        [
            name,
            ticker,
            price,
            market_cap,
            price_change_percentage_200d,
            'N/A'
        ],
            index = my_columns,
    ),
        ignore_index = True
)

final_dataframe.sort_values('200D Price Return', ascending = False, inplace = True)
final_dataframe = final_dataframe[:20]
final_dataframe.reset_index(inplace = True)

position_size = float(portfolio_size)/len(final_dataframe.index)
for i in range(0, len(final_dataframe)):
    final_dataframe.loc[i, 'Number of Tokens to Buy'] = math.floor(position_size/final_dataframe.loc[i, 'Current Price'])
st.dataframe(final_dataframe, 1200, 900)

@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(final_dataframe)

st.download_button(
    label="Download above data as CSV",
    data=csv,
    file_name='top20_momentum_strategy.csv',
    mime='text/csv',
)

st.write("""
## Composite Quantitative Momentum Investment Strategy

The table below lists Top 200 cryptocurrencies from the highest percentiles of - 24H price return, 7D price return, 14D price return, 30D price return, 200D price return and 1Y price return, ordered by "HQM Score", where HQM score is the arithmetic mean of 24H percentile return,
7D percentile return, 14D percentile return, 30D percentile return, 200D percentile return, and 1Y percentile return.

""")

hqm_columns = [
    'Name',
    'Ticker', 
    'Current Price',
    'HQM Score',
    'Market Capitalization', 
    '24H Price Return',
    '24H Return Percentile',
    '7D Price Return',
    '7D Return Percentile',
    '14D Price Return',
    '14D Return Percentile',
    '30D Price Return',
    '30D Return Percentile',
    '200D Price Return',
    '200D Return Percentile',
    '1Y Price Return',
    '1Y Return Percentile',
]
hqm_dataframe = pd.DataFrame(columns = hqm_columns)

for i in data:
    name = i['name']
    ticker = i['symbol'].upper()
    price = i['current_price']
    hqm_score = 'N/A'
    market_cap = i['market_cap']
    price_change_percentage_24h = i['price_change_24h']
    percentile_return_24h = 'N/A'
    price_change_percentage_7d = i['price_change_percentage_7d_in_currency']
    percentile_return_7d = 'N/A'
    price_change_percentage_14d = i['price_change_percentage_14d_in_currency']
    percentile_return_14d = 'N/A'
    price_change_percentage_30d = i['price_change_percentage_30d_in_currency']
    percentile_return_30d = 'N/A'
    price_change_percentage_200d = i['price_change_percentage_200d_in_currency']
    percentile_return_200d = 'N/A'
    price_change_percentage_1y = i['price_change_percentage_1y_in_currency']
    percentile_return_1y = 'N/A'

    hqm_dataframe = hqm_dataframe.append(
    pd.Series(
        [
            name,
            ticker,
            price,
            hqm_score,
            market_cap,
            price_change_percentage_24h,
            percentile_return_24h,
            price_change_percentage_7d,
            percentile_return_7d,
            price_change_percentage_14d,
            percentile_return_14d,
            price_change_percentage_30d,
            percentile_return_30d,
            price_change_percentage_200d,
            percentile_return_200d,
            price_change_percentage_1y,
            percentile_return_1y,
        ],
            index = hqm_columns,
    ),
        ignore_index = True
)

for column in ['30D Price Return', '200D Price Return','1Y Price Return']:
    hqm_dataframe[column].fillna(hqm_dataframe[column].mean(), inplace = True)

time_periods = [
                '24H',
                '7D',
                '14D',
                '30D',
                '200D',
                '1Y',
                ]

for row in hqm_dataframe.index:
    for time_period in time_periods:
        hqm_dataframe.loc[row, f'{time_period} Return Percentile'] = stats.percentileofscore(hqm_dataframe[f'{time_period} Price Return'], hqm_dataframe.loc[row, f'{time_period} Price Return'])/100



for row in hqm_dataframe.index:
    momentum_percentiles = []
    for time_period in time_periods:
        momentum_percentiles.append(hqm_dataframe.loc[row, f'{time_period} Return Percentile'])
    hqm_dataframe.loc[row, 'HQM Score'] = mean(momentum_percentiles)
    
hqm_dataframe.sort_values(by = 'HQM Score', ascending = False, inplace = True)
hqm_dataframe.reset_index(inplace = True)    
st.dataframe(hqm_dataframe, 1200, 900)


st.write("""
## Equal Weight Composite Quantitative Momentum Investment Strategy

Enter the value of your portfolio to obtain an equal-weight investment distribution for top 20 high momentum cryptocurrencies from the above list.

""")

portfolio_size = st.number_input('Enter the value of your portfolio', key=2)

position_size = portfolio_size / len(final_dataframe.index)

print(position_size)

hqm_columns = [
    'Name',
    'Ticker', 
    'Current Price',
    'HQM Score',
    'Market Capitalization', 
    '24H Price Return',
    '24H Return Percentile',
    '7D Price Return',
    '7D Return Percentile',
    '14D Price Return',
    '14D Return Percentile',
    '30D Price Return',
    '30D Return Percentile',
    '200D Price Return',
    '200D Return Percentile',
    '1Y Price Return',
    '1Y Return Percentile',
]
hqm_dataframe = pd.DataFrame(columns = hqm_columns)

for i in data:
    name = i['name']
    ticker = i['symbol'].upper()
    price = i['current_price']
    hqm_score = 'N/A'
    market_cap = i['market_cap']
    price_change_percentage_24h = i['price_change_24h']
    percentile_return_24h = 'N/A'
    price_change_percentage_7d = i['price_change_percentage_7d_in_currency']
    percentile_return_7d = 'N/A'
    price_change_percentage_14d = i['price_change_percentage_14d_in_currency']
    percentile_return_14d = 'N/A'
    price_change_percentage_30d = i['price_change_percentage_30d_in_currency']
    percentile_return_30d = 'N/A'
    price_change_percentage_200d = i['price_change_percentage_200d_in_currency']
    percentile_return_200d = 'N/A'
    price_change_percentage_1y = i['price_change_percentage_1y_in_currency']
    percentile_return_1y = 'N/A'

    hqm_dataframe = hqm_dataframe.append(
    pd.Series(
        [
            name,
            ticker,
            price,
            hqm_score,
            market_cap,
            price_change_percentage_24h,
            percentile_return_24h,
            price_change_percentage_7d,
            percentile_return_7d,
            price_change_percentage_14d,
            percentile_return_14d,
            price_change_percentage_30d,
            percentile_return_30d,
            price_change_percentage_200d,
            percentile_return_200d,
            price_change_percentage_1y,
            percentile_return_1y,
        ],
            index = hqm_columns,
    ),
        ignore_index = True
)

for column in ['30D Price Return', '200D Price Return','1Y Price Return']:
    hqm_dataframe[column].fillna(hqm_dataframe[column].mean(), inplace = True)

time_periods = [
                '24H',
                '7D',
                '14D',
                '30D',
                '200D',
                '1Y',
                ]

for row in hqm_dataframe.index:
    for time_period in time_periods:
        hqm_dataframe.loc[row, f'{time_period} Return Percentile'] = stats.percentileofscore(hqm_dataframe[f'{time_period} Price Return'], hqm_dataframe.loc[row, f'{time_period} Price Return'])/100



for row in hqm_dataframe.index:
    momentum_percentiles = []
    for time_period in time_periods:
        momentum_percentiles.append(hqm_dataframe.loc[row, f'{time_period} Return Percentile'])
    hqm_dataframe.loc[row, 'HQM Score'] = mean(momentum_percentiles)
    
hqm_dataframe.sort_values(by = 'HQM Score', ascending = False, inplace = True)
hqm_dataframe = hqm_dataframe[:20]
hqm_dataframe.reset_index(inplace = True)   

for i in range(0, len(hqm_dataframe['Ticker'])):
    hqm_dataframe.loc[i, 'Number of Tokens to Buy'] = math.floor(position_size / hqm_dataframe['Current Price'][i])
st.dataframe(hqm_dataframe, 1200, 900)

@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(hqm_dataframe)

st.download_button(
    label="Download above data as CSV",
    data=csv,
    file_name='top20_composite_momentum_strategy.csv',
    mime='text/csv',
)