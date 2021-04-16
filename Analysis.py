import pandas as pd


portifolio = pd.read_csv( 'dataset/kc_house_data.csv' )

# filtering data

portWithFilter = portifolio[['id','price','zipcode','date','condition','yr_built','yr_renovated','bedrooms']]


# removing outliers

portWithFilter = portWithFilter.loc[(portWithFilter['price']<2000000) & (portWithFilter['bedrooms']<5)]

# casting

portWithFilter['date'] = pd.to_datetime(portWithFilter['date'])

# sorting by date

portWithFilter = portWithFilter.sort_values('date')

# grouping by zipcode

medianbyZipCode = portWithFilter[['price','zipcode']].groupby('zipcode').median().reset_index()

# comparing properties by median of zipcode

portWithFilter['median_price'] = 0
portWithFilter['status'] = 'NA'

# print(portWithFilter.columns)


for i in range( len(portWithFilter) ):
    for j in range( len(medianbyZipCode) ):
        if ( portWithFilter.iloc[i, 2] == medianbyZipCode.loc[j, 'zipcode'] ):
            portWithFilter.iloc[i, 8] = medianbyZipCode.loc[j,'price']
            if( portWithFilter.iloc[i, 1] > medianbyZipCode.loc[j, 'price'] ):
                portWithFilter.iloc[i, 9] = 'not buy'
            else:
                portWithFilter.iloc[i, 9]  = 'buy'
            continue


# print(portWithFilter.head(15))

# when to buy the chosen properties, when to sell

portWithFilter['season'] = 'StdSeason'
portWithFilter['sell_price'] = 0
portWithFilter['profit'] = 0


portWithFilter.loc[ (portWithFilter['date'].dt.month >= 3) & (portWithFilter['date'].dt.month < 9), 'season'] = 'Summer'
portWithFilter.loc[ (portWithFilter['date'].dt.month >= 9) | (portWithFilter['date'].dt.month < 3), 'season'] = 'Winter'

medianbyZipCodeandSeason = portWithFilter[['price','zipcode','season']].groupby( ['zipcode','season'] ).median().reset_index()

for i in range ( len(portWithFilter) ):
    if portWithFilter.iloc[i, 9] == 'buy':
        for j in range( len(medianbyZipCodeandSeason) ):
            if(portWithFilter.iloc[i, 2] == medianbyZipCodeandSeason.loc[j, 'zipcode']) & ( medianbyZipCodeandSeason.loc[j, 'season'] == 'Summer' ):
                if( portWithFilter.iloc[i,1] >= medianbyZipCodeandSeason.loc[j,'price'] ):
                    portWithFilter.iloc[i, 11]  = portWithFilter.iloc[i,1]*1.1
                    break
                else:
                    portWithFilter.iloc[i, 11] = portWithFilter.iloc[i, 1] * 1.3
                    break

    portWithFilter.iloc[i,12] = portWithFilter.iloc[i,11] - portWithFilter.iloc[i,1]

print(portWithFilter[['status','price','zipcode','season','sell_price','profit']].head(50))

print( portWithFilter['profit'][portWithFilter['profit'] > 0].sum() )

