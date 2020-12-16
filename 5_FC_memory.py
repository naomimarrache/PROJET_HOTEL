# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 13:53:24 2020

@author: MAROUANE
"""


# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 16:51:36 2020

@author: MAROUANE
"""

from surprise import Dataset
from surprise import accuracy
import numpy as np
import os
import csv
import pandas as pd
from surprise.model_selection import train_test_split
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from surprise import Reader, Dataset, KNNBasic, KNNWithMeans, KNNBaseline, KNNWithZScore
from sklearn.metrics.pairwise import cosine_similarity
from surprise.model_selection import cross_validate
import ast 
import json



def selet_top(predictions, n):
    # First map the predictions to each user.
    top_r = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_r[uid].append((iid, est))
        err=abs(est - true_r)
        #print(err)

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_r.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_r[uid] = user_ratings[:n]

    return top_r


#Reading the dataset
UDF = pd.read_csv("users_profile_url.csv")
RDF = pd.read_csv('reviews.csv')
HDF = pd.read_csv('hotels.csv')
#allouer à chaque hotel/review un id hotel_id/review_id
UDF['user_id'] = UDF.index
HDF['hotel_id'] = HDF.index
#commencer à 1 et non 0
UDF['user_id']=UDF['user_id'].apply(lambda x : x+1)
HDF['hotel_id']=HDF['hotel_id'].apply(lambda x : x+1)
RHDF=pd.merge(RDF,HDF)
UHDF = pd.merge(RHDF,UDF)
rates = UHDF.rate
hotel_ids = UHDF.hotel_id
user_ids = UHDF.user_id
ratings = pd.DataFrame({'user_id':user_ids,'hotel_id':hotel_ids,'rating':rates})
reader = Reader()
Data1 = Dataset.load_from_df(ratings[['user_id','hotel_id','rating']],reader)

#Splitting the dataset
trainset, testset = train_test_split(Data1, test_size=0.3,random_state=10)
print('Number of users: ', trainset.n_users, '\n')
print('Number of items: ', trainset.n_items, '\n')
models=[KNNBasic, KNNWithMeans]
mesure=['cosine', 'pearson']
list_k=[10,20,30,40]
    # Creating an empty Dataframe with column names only
dfObj = pd.DataFrame(columns=['model', 'measure', 'k', 'resman', 'value'])
for i in range (0,2):
    print('models',models[i])
    for j in range(0,2):
        print('mesure',mesure[j])
        for k in list_k:
            print('la valeur de k :', k)
            #Use user_based true/false to switch between user-based or item-based collaborative filtering
            algo = models[i](k=k,sim_options={'name': mesure[j], 'user_based': False})
            #results = cross_validate(algo = algo, data = Data1, measures=['RMSE'], cv=5, return_train_measures=True)    
            #resmean=results['test_rmse'].mean()
            algo.fit(trainset)        
            # run the trained model against the testset
            test_pred = algo.test(testset)
            test_pred
            #evaluate model
            valeur=accuracy.rmse(test_pred, verbose=True)
            #print("valeur", valeur)
            top_r = selet_top(test_pred, n=5)
            
            dfObj = dfObj.append({'model': models[i], 'measure': mesure[j], 'k':k, 'resman':valeur, 'value': top_r}, ignore_index=True) #index 0, 1
     
dfObj.sort_values(by = 'resman', inplace = True)          

#meilleur algo avec parametres
ress1=dfObj.iloc[0]
#ress1
#recuperer les valeurs user, item, score du meilleur resultats
#ress=dfObj['value'].iloc[0]
#resu=df.iloc[0, df.columns.get_loc('value')] 
resu=dfObj.iloc[0, dfObj.columns.get_loc('value')] 
resue=dfObj.iloc[0]['value']
"""
#Print the recommended items for each user
for uid, user_ratings in resu.items():
    print(uid, [iid for (iid, _) in user_ratings])
   """
