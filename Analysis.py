

# 1.0 Imports

import pandas as pd

# 2.0 Helper functions

# 3.0 Loading data(*)

portifolio = pd.read_csv( 'dataset/kc_house_data.csv' )
### 3.0.1 filtering data
portifolio = portifolio[['id', 'price', 'zipcode', 'date', 'condition', 'yr_built', 'yr_renovated', 'bedrooms']]


# 4.0 Data Description

## 4.0.1 Data Dimensions

print( 'number of Rows: {}'.format( portifolio.shape[0] ) )
print( 'number of Rows: {}'.format( portifolio.shape[1] ) )

## 4.0.2 Data Types

portifolio['date'] = pd.to_datetime(portifolio['date'])
portifolio.dtypes

## 4.0.3 Check NA

portifolio.isna().sum()

## 4.0.4 Fillout NA

## 4.0.5 Removing Outliers

portifolio = portifolio.loc[(portifolio['price'] < 2000000) & (portifolio['bedrooms'] < 5)]


## 4.0.6 Change types

portifolio['date'] = pd.to_datetime(portifolio['date'])

## 4.0.7 Descriptive Statistical





# 5.0 Data Exp



# 6.0 Putting on Heroku




# grouping by zipcode

medianbyZipCode = portifolio[['price', 'zipcode']].groupby('zipcode').median().reset_index()

# comparing properties by median of zipcode

portifolio['median_price'] = 0
portifolio['status'] = 'NA'

# print(portWithFilter.columns)


for i in range(len(portifolio)):
    for j in range( len(medianbyZipCode) ):
        if ( portifolio.iloc[i, 2] == medianbyZipCode.loc[j, 'zipcode']):
            portifolio.iloc[i, 8] = medianbyZipCode.loc[j, 'price']
            if( portifolio.iloc[i, 1] > medianbyZipCode.loc[j, 'price']):
                portifolio.iloc[i, 9] = 'not buy'
            else:
                portifolio.iloc[i, 9]  = 'buy'
            continue


# print(portWithFilter.head(15))

# when to buy the chosen properties, when to sell

portifolio['season'] = 'StdSeason'
portifolio['sell_price'] = 0
portifolio['profit'] = 0


portifolio.loc[(portifolio['date'].dt.month >= 3) & (portifolio['date'].dt.month < 9), 'season'] = 'Summer'
portifolio.loc[(portifolio['date'].dt.month >= 9) | (portifolio['date'].dt.month < 3), 'season'] = 'Winter'

medianbyZipCodeandSeason = portifolio[['price', 'zipcode', 'season']].groupby(['zipcode', 'season']).median().reset_index()

for i in range (len(portifolio)):
    if portifolio.iloc[i, 9] == 'buy':
        for j in range( len(medianbyZipCodeandSeason) ):
            if(portifolio.iloc[i, 2] == medianbyZipCodeandSeason.loc[j, 'zipcode']) & (medianbyZipCodeandSeason.loc[j, 'season'] == 'Summer'):
                if( portifolio.iloc[i, 1] >= medianbyZipCodeandSeason.loc[j, 'price']):
                    portifolio.iloc[i, 11]  = portifolio.iloc[i, 1] * 1.1
                    break
                else:
                    portifolio.iloc[i, 11] = portifolio.iloc[i, 1] * 1.3
                    break

    portifolio.iloc[i, 12] = portifolio.iloc[i, 11] - portifolio.iloc[i, 1]

print(portifolio[['status', 'price', 'zipcode', 'season', 'sell_price', 'profit']].head(50))

print( 'Total Profit: {}'.format(portifolio['profit'][portifolio['profit'] > 0].sum()))