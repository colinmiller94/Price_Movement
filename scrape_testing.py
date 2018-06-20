
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import math
import datetime
import sqlite3




security = 'BAC'
url = 'https://www.nasdaq.com/symbol/'+ security + '/historical'
#url = 'https://finance.yahoo.com/quote/' + security + '/history'
print(url)
#
# source = urllib.request.urlopen(url).read()
# soup = BeautifulSoup(source,'lxml')
#
# tables = soup.find('table')
# table_rows = tables.find_all('tr')
#
# dates = []
# closes = []


dfs = pd.read_html(url)
df = dfs[2]


column_string = df.columns.values[4]

new_df = df[column_string]
new_df = df['Date']

dates = df['Date'].tolist()[1:]
print(len(dates))
closes = df[column_string].tolist()[1:]
print(len(closes))



# new_df2 = df[['Date',column_string]]
# new_df2.rename(index = str, columns = {column_string : 'Close'})


print(dates)
print(closes)