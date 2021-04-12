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
        print()
        if ( portWithFilter.iloc[i, 2] == medianbyZipCode.loc[j, 'zipcode'] ):
            portWithFilter.iloc[i, 8] = medianbyZipCode.loc[j,'price']
            if( portWithFilter.iloc[i, 1] > medianbyZipCode.loc[j, 'price'] ):
                portWithFilter.iloc[i, 9] = 'not buy'
            else:
                portWithFilter.iloc[i, 9]  = 'buy'
            continue


print(portWithFilter.head(4))





