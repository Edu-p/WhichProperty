# 1.0 Imports

import pandas as pd
import numpy as np
import seaborn as sns
# from matplotlib import pyplot as plt
from IPython.display import Image
import Streamlit as st
import plotly.express as px

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

    #removing outliers

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

def creating_features( data ):
    ### 4.0.8.2 creating columns

    data['profit'] = 0
    data['status'] = 'NA'
    data['sell_price'] = 0

    data['zipcode_median_price'] = 0

    # grouping by zipcode
    medianbyZipCode = data[['price', 'zipcode']].groupby('zipcode').median().reset_index()
    # comparing properties by median of zipcode
    print(data.columns)
    for i in range(len(data)):  # this need to update to do more fast this att
        for j in range(len(medianbyZipCode)):
            if (data.iloc[i, 2] == medianbyZipCode.loc[j, 'zipcode']):
                print(i, j)
                data.iloc[i, 11] = medianbyZipCode.loc[j, 'price']
                continue

    data['season'] = 'StdSeason'
    data.loc[(data['date'].dt.month >= 3) & (data['date'].dt.month < 9), 'season'] = 'Summer'
    data.loc[(data['date'].dt.month >= 9) | (data['date'].dt.month < 3), 'season'] = 'Winter'
    print(data[['zipcode_median_price', 'season']])

    return data

def data_filtering( data ):

    data = data.loc[(data['price'] < 2000000) & (data['bedrooms'] < 5)]

    return data

portifolio = loading_data( 'dataset/kc_house_data.csv' )

portifolio = filtering_data( portifolio )

show_data_dimensions(portifolio)

portifolio = show_data_types( portifolio )

checkNa(portifolio)

portifolio = removing_outliers( portifolio )

portifolio = change_types( portifolio )

descriptive_statistical(portifolio)

portifolio = creating_features( portifolio )


# 5.0 Data Exp

# validating hypothesis


# 1 hypothesis

# Avarage Price per year

st.sidebar.title( 'Commercial Options' )
st.title( 'Commercial atributes' )

data['date'] = pd.to_datetime( data['date'] ).dt.strftime('%Y-%m-%d')

# Filters
min_year_built = int( data['yr_built'].min() )
max_year_built = int(data['yr_built'].max() )

st.sidebar.subheader( 'Select Max Year Built' )
f_year_built = st.sidebar.slider( 'Year Built', min_year_built,
                                 max_year_built,
                                 min_year_built)



st.header( 'Avarage Price per Year Built' )

df1 = data.loc[ data['yr_built'] < f_year_built ]

df1 =  df1[['yr_built','price']].groupby('yr_built').mean().reset_index()

fig = px.line( df1,x='yr_built',y='price' )

st.plotly_chart( fig,use_container_width=True )










# 6.0 Putting on Heroku




