import pandas as pd

data = pd.read_csv('currencies_updated/AUD-USD_Change_updated.csv')
print(data)

#data2 = data.drop_duplicates()
#print(data2)


#data = data.dropna()
data.drop('Adj Close', axis=1, inplace=True)
#data.to_csv('./currencies_lists_updated/AUD-USD_Adj Close_updated.csv', index=False)

data.to_csv('./currencies_lists_updated/AUD-USD_Change_updated.csv', index=False)
#print(data.isnull().sum())
#print('----------------------------------------------------------------------')

#data2 = pd.read_csv('./currencies_lists_updated/EUR-CAD_Adj Close_updated.csv')
#print(data2)

