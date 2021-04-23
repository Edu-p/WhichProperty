

# 1.0 Imports

import pandas as pd
import numpy as np
import seaborn as sns
# from matplotlib import pyplot as plt
from IPython.display import Image

# 2.0 Helper functions

def loading_data( path ):

    data = pd.read_csv(path)

    return data

def filtering_data( data ):

    data = data[['id', 'price', 'zipcode', 'date', 'condition', 'yr_built', 'yr_renovated', 'bedrooms']]

    return data

def show_data_dimensions( data ):

    print('number of Rows: {}'.format(portifolio.shape[0]))
    print('number of Rows: {}'.format(portifolio.shape[1]))
    print('----------------------------\n')

    return None

def show_data_types( data ):

    data['date'] = pd.to_datetime(data['date'])
    print(portifolio.dtypes)

    return data

def checkNa( data ):
    print(portifolio.isna().sum())
    print('----------------------------\n')
    return None

def removing_outliers( data ):

    data = data.loc[(data['price'] < 2000000) & (data['bedrooms'] < 5)]

    return data

def change_types( data ):

    data['date'] = pd.to_datetime(data['date'])

    return data

def descriptive_statistical( data ):

    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    ### 4.0.7.1 Numerical Attributes

    num_attributes = portifolio.select_dtypes(include=['int64', 'float64'])
    cat_attributes = portifolio.select_dtypes(exclude=['int64', 'float64', 'datetime64[ns]'])

    #### 4.0.7.1.1 Central Tendency -  mean, median
    ct1 = pd.DataFrame(num_attributes.apply(np.mean)).T
    ct2 = pd.DataFrame(num_attributes.apply(np.median)).T

    #### 4.0.7.1.2 Dispersion - std, min, max, range, skev, kurtosis
    d1 = pd.DataFrame(num_attributes.apply(np.std)).T
    d2 = pd.DataFrame(num_attributes.apply(min)).T
    d3 = pd.DataFrame(num_attributes.apply(max)).T
    d4 = pd.DataFrame(num_attributes.apply(lambda x: x.max() - x.min())).T
    d5 = pd.DataFrame(num_attributes.apply(lambda x: x.skew())).T
    d6 = pd.DataFrame(num_attributes.apply(lambda x: x.kurtosis)).T

    dfDesc = pd.concat([d2, d3, d4, ct1, ct2, d1, d5, d4]).T.reset_index()

    dfDesc.columns = ['attributes', 'min', 'max', 'range', 'mean', 'median', 'std', 'skew', 'kurtosis']

    print(dfDesc)
    print('----------------------------\n')

    return None


# 3.0 Loading data(*)

portifolio = loading_data( 'dataset/kc_house_data.csv' )

### 3.0.1 filtering data

portifolio = filtering_data( portifolio )


# 4.0 Data Description

## 4.0.1 Data Dimensions

show_data_dimensions(portifolio)

## 4.0.2 Data Types

portifolio = show_data_types( portifolio )

## 4.0.3 Check NA

checkNa(portifolio)

## 4.0.5 Removing Outliers

portifolio = removing_outliers( portifolio )


## 4.0.6 Change types

portifolio = change_types( portifolio )

## 4.0.7 Descriptive Statistical

descriptive_statistical(portifolio)

## 4.0.8 Feature engeneering

### 4.0.8.1 hypothesis to validate
    # 1. does the season that you sell influence profit?
    # 2. the valuation of the zipcode influences the price of the property?
    # 3. if the condition of the property is bad, is it devalued?
    # 4. are older properties cheaper?
    # 5. are non-renovated properties cheaper?

### 4.0.8.2 creating columns

portifolio['profit'] = 0
portifolio['status'] = 'NA'
portifolio['sell_price'] = 0

portifolio['zipcode_median_price'] = 0

# grouping by zipcode

medianbyZipCode = portifolio[['price', 'zipcode']].groupby('zipcode').median().reset_index()

# comparing properties by median of zipcode

# print(portWithFilter.columns)
print('ate aq')
print(portifolio.columns)

for i in range(len(portifolio)):
    for j in range( len(medianbyZipCode) ):
        if ( portifolio.iloc[i, 2] == medianbyZipCode.loc[j, 'zipcode']):
            print(i,j)
            portifolio.iloc[i, 11] = medianbyZipCode.loc[j, 'price']
            continue




portifolio['season'] = 'StdSeason'
portifolio.loc[(portifolio['date'].dt.month >= 3) & (portifolio['date'].dt.month < 9), 'season'] = 'Summer'
portifolio.loc[(portifolio['date'].dt.month >= 9) | (portifolio['date'].dt.month < 3), 'season'] = 'Winter'

print(portifolio[['zipcode_median_price', 'season']])



# 5.0 Data Exp

###########
# ver notas na area de trabalho
###########


# 6.0 Putting on Heroku


