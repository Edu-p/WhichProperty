
# 1.0 Imports

import pandas as pd
import numpy as np
import seaborn as sns
# from matplotlib import pyplot as plt
from IPython.display import Image
import streamlit as st
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
    # for i in range(len(data)):  # this need to update to do more fast this att
    #     for j in range(len(medianbyZipCode)):
    #         if (data.iloc[i, 2] == medianbyZipCode.loc[j, 'zipcode']):
    #             print(i, j)
    #             data.iloc[i, 11] = medianbyZipCode.loc[j, 'price']
    #             continue

    data['season'] = 'StdSeason'
    data.loc[(data['date'].dt.month >= 3) & (data['date'].dt.month < 9), 'season'] = 'Summer'
    data.loc[(data['date'].dt.month >= 9) | (data['date'].dt.month < 3), 'season'] = 'Winter'
    print(data[['zipcode_median_price', 'season']])

    return data

def validating_first_hypo( data ):
    st.title('Validating hypothesis')

    st.header('Does the season that you sell influence price?')

    df = data[['season', 'price']].groupby('season').median().reset_index()

    fig = px.bar(df, x='price', y='season')

    st.plotly_chart(fig, use_container_width=True)

    return None

def validating_second_hypo( data ):
    st.header('The valuation of the zipcode influences the price of the property?')

    st.write('\n')

    data = data[['zipcode', 'price']].groupby('zipcode').median().reset_index()

    cols_new = ['zipcode', 'median_price']

    data.columns = cols_new

    data['zipcode'] = data['zipcode'].astype(object)

    st.write(data)

    fig = px.bar(data, x='zipcode', y='median_price')

    st.plotly_chart(fig, use_container_width=True)

    return None

def validating_third_hypo( data ):

    st.header('If the condition of the property is bad, is it more than 30% devalued, on average?')
    st.subheader('(if you compare with properties that were in good condition)')
    st.write('\n')

    median_good = int(data[ (data['condition'] == 4) | (data['condition'] == 3) | (data['condition'] == 5) ]['price'].median() )
    median_bad = int(data[ (data['condition'] == 1) | (data['condition'] == 2) ]['price'].median() )

    data1 = { 'type' : ['median_bad','median_good'], 'price_of_median' : [median_bad, median_good] }

    df = pd.DataFrame( data1 ).reset_index()

    st.write( df )

    fig = px.bar(df, x='type' , y='price_of_median')

    st.plotly_chart(fig, use_container_width=True)

    return None


def validating_fourth_hypo( data ):
    st.header('Are older properties cheaper?')
    st.subheader('(older properties is year_built < 1950)')
    st.write('\n')

    old_properties = data[ data['yr_built'] <= 1950 ]['price'].median()
    new_properties = data[ data['yr_built'] > 1950 ]['price'].median()

    data1 = {'type': ['old_properties', 'new_properties'], 'price_of_median': [old_properties, new_properties]}

    df = pd.DataFrame(data1).reset_index()

    st.write(df)

    fig = px.bar(df, x='type', y='price_of_median')

    st.plotly_chart(fig, use_container_width=True)


    return None

def validating_fifth_hypo( data ):
    st.header('Are non-renovated properties 20% cheaper?')
    st.write('\n')

    non_renovated_properties = data[ data['yr_renovated'] == 0 ]['price'].median()
    renovated_properties = data[ data['yr_renovated'] !=0 ]['price'].median()

    data1 = {'renovation': ['non_renovated', 'renovated'], 'price_of_median': [non_renovated_properties, renovated_properties]}

    df = pd.DataFrame(data1).reset_index()

    st.write(df)

    fig = px.bar(df, x='renovation', y='price_of_median')

    st.plotly_chart(fig, use_container_width=True)


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
portifolio = creating_features( portifolio )

# 5.0 Data Exp

## 5.0.1 validating first hypothesis
validating_first_hypo( portifolio )

## 5.0.2 validating second hypothesis
validating_second_hypo( portifolio )

## 5.0.3 validating third hypothesis
validating_third_hypo( portifolio )

## 5.0.4 validating fourth hypothesis


## 5.0.5 validating fifth hypothesis


st.write( portifolio.head(40) )

# 6.0 Conclusions


# 7.0 Putting on Heroku


