

# 1.0 Imports

import pandas as pd
import numpy as np
import seaborn as sns
# from matplotlib import pyplot as plt

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
print( portifolio.dtypes )

## 4.0.3 Check NA

print(portifolio.isna().sum())

## 4.0.5 Removing Outliers

portifolio = portifolio.loc[(portifolio['price'] < 2000000) & (portifolio['bedrooms'] < 5)]


## 4.0.6 Change types

portifolio['date'] = pd.to_datetime(portifolio['date'])

## 4.0.7 Descriptive Statistical

pd.set_option('display.float_format', lambda x: '%.2f' % x)

### 4.0.7.1 Numerical Attributes

num_attributes = portifolio.select_dtypes( include=['int64', 'float64'] )
cat_attributes = portifolio.select_dtypes( exclude=['int64', 'float64', 'datetime64[ns]'] )

#### 4.0.7.1.1 Central Tendency -  mean, median
ct1 = pd.DataFrame( num_attributes.apply( np.mean ) ).T
ct2 = pd.DataFrame( num_attributes.apply( np.median ) ).T

#### 4.0.7.1.2 Dispersion - std, min, max, range, skev, kurtosis
d1 = pd.DataFrame( num_attributes.apply( np.std ) ).T
d2 = pd.DataFrame( num_attributes.apply( min ) ).T
d3 = pd.DataFrame( num_attributes.apply( max ) ).T
d4 = pd.DataFrame( num_attributes.apply( lambda x: x.max() - x.min() ) ).T
d5 = pd.DataFrame( num_attributes.apply( lambda x: x.skew() ) ).T
d6 = pd.DataFrame( num_attributes.apply( lambda x: x.kurtosis ) ).T

dfDesc = pd.concat( [ d2, d3, d4, ct1, ct2, d1, d5, d4 ] ).T.reset_index()

dfDesc.columns = ['attributes', 'min', 'max', 'range', 'mean', 'median', 'std', 'skew', 'kurtosis']

print(dfDesc)

## 4.0.8 Feature engeneering

portifolio['median_price'] = 0
portifolio['status'] = 'NA'
portifolio['season'] = 'StdSeason'
portifolio['sell_price'] = 0
portifolio['profit'] = 0

# 5.0 Data Exp

###########
# ver notas na area de trabalho
###########


# 6.0 Putting on Heroku


