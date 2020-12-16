# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
    
def agregate_hotels_with_cleaning(filename,files_to_agregate):
    Dataframes = []
    for file in files_to_agregate:
        Dataframes.append(pd.read_csv(file))  
    df_concat = pd.concat(Dataframes)
    df = df_concat.drop_duplicates(subset='url_hotel', keep="last")
    df.reset_index(inplace=True)
    prices_hotel = [ str(price).replace(' ','').replace(u'\xa0', u'').strip() for price in df.price_hotel]
    df['price_hotel'] = prices_hotel 
    for i in range(len(df.price_hotel)):
        try:
            if df.price_hotel[i] == 'nan':
                df.price_hotel[i] = 0
            else:
                df.price_hotel[i] = int(df.price_hotel[i])
        except ValueError:
            print('ValueError')          
    for i in range(len(df.price_hotel)):
        if df.price_hotel[i] == 0:
            df['price_hotel'][i] = mean_by_country_city_category(i,df)
            if df.price_hotel[i] == 0:
                df['price_hotel'][i] = df.price_hotel.mean()
        if df.category_hotel[i] == None:
            print(df.category_hotel[i])
    df['price_hotel'] = df.price_hotel.apply(lambda x: int(x))
    df['category_hotel'].fillna(0, inplace = True)
    df['style_hotel'].fillna('', inplace = True)
    df['position_by_city_hotel'].fillna('', inplace = True)
    df.to_csv(filename, index = False, header=True,encoding='utf-8-sig')
    return df

def mean_by_country_city_category(i,df):
    city = df['city_hotel'][i]
    country = df['country_hotel'][i]
    category = df['category_hotel'][i]
    df_test = df.copy()
    df_test = df_test.drop(i)
    df_test1 = df_test.loc[df_test['country_hotel']==country]
    df_test2 = df_test1.loc[df_test1['city_hotel']==city]
    df_test3 = df_test2.loc[df_test2['category_hotel']==category]
    if df_test1.shape[0]>0:
        df_test = df_test1
        #print(df_test.shape)
        if df_test2.shape[0]>0:
            df_test = df_test2
            #print(df_test.shape)
            if df_test3.shape[0]>0:
                df_test = df_test3
                #print(df_test.shape)
    return df_test.price_hotel.mean()


if __name__ == "__main__":
    files_to_agregate = ['hotels/hotels0_1000.csv','hotels/hotels1000_1850.csv','hotels/hotels1800_2190.csv','hotels/hotels2170_3000.csv']
    df_agregate = agregate_hotels_with_cleaning("hotels_agreg.csv",files_to_agregate)
    