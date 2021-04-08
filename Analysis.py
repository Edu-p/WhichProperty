import pandas as pd


portifolio = pd.read_csv( 'dataset/kc_house_data.csv' )

# print(portifolio.dtypes)

# filtering data

portWithFilter = portifolio[['id','price','zipcode','date','condition','yr_built','yr_renovated','bedrooms']]

# print(portWithFilter.shape)

# removing outliers

portWithFilter = portWithFilter.loc[(portWithFilter['price']<2000000) & (portWithFilter['bedrooms']<5)]

# print(portWithFilter.shape)

# casting

portWithFilter['date'] = pd.to_datetime(portWithFilter['date'])

# sorting by date

portWithFilter = portWithFilter.sort_values('date')

# print(portWithFilter['date'].head)

# grouping by zipcode

portWithFilter[['price','zipcode']].groupby('zipcode').median()








