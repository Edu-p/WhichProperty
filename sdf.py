
# grouping by zipcode

medianbyZipCode = data[['price', 'zipcode']].groupby('zipcode').median().reset_index()

# comparing properties by median of zipcode


# print(portWithFilter.columns)


for i in range(len(data)):
    for j in range( len(medianbyZipCode) ):
        if ( data.iloc[i, 2] == medianbyZipCode.loc[j, 'zipcode']):
            data.iloc[i, 8] = medianbyZipCode.loc[j, 'price']
            if( data.iloc[i, 1] > medianbyZipCode.loc[j, 'price']):
                data.iloc[i, 9] = 'not buy'
            else:
                data.iloc[i, 9]  = 'buy'
            continue


# print(portWithFilter.head(15))

# when to buy the chosen properties, when to sell


data.loc[(data['date'].dt.month >= 3) & (data['date'].dt.month < 9), 'season'] = 'Summer'
data.loc[(data['date'].dt.month >= 9) | (data['date'].dt.month < 3), 'season'] = 'Winter'

medianbyZipCodeandSeason = data[['price', 'zipcode', 'season']].groupby(['zipcode', 'season']).median().reset_index()

for i in range (len(data)):
    if data.iloc[i, 9] == 'buy':
        for j in range( len(medianbyZipCodeandSeason) ):
            if(data.iloc[i, 2] == medianbyZipCodeandSeason.loc[j, 'zipcode']) & (medianbyZipCodeandSeason.loc[j, 'season'] == 'Summer'):
                if( data.iloc[i, 1] >= medianbyZipCodeandSeason.loc[j, 'price']):
                    data.iloc[i, 11]  = data.iloc[i, 1] * 1.1
                    break
                else:
                    data.iloc[i, 11] = data.iloc[i, 1] * 1.3
                    break

    data.iloc[i, 12] = data.iloc[i, 11] - data.iloc[i, 1]

print(data[['status', 'price', 'zipcode', 'season', 'sell_price', 'profit']].head(50))

print( 'Total Profit: {}'.format(data['profit'][data['profit'] > 0].sum()))