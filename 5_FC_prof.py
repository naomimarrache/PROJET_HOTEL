# -*- coding: utf-8 -*-

import pandas as pd
from collections import defaultdict


from surprise import SVD, NMF , Reader, Dataset, accuracy
from surprise.model_selection.split import train_test_split
from surprise.model_selection import GridSearchCV


UDF = pd.read_csv("users_profile_url.csv")
RDF = pd.read_csv('reviews.csv')
HDF = pd.read_csv('hotels_agreg.csv')


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
data = Dataset.load_from_df(ratings[['user_id','hotel_id','rating']],reader)


algo=SVD()

#algo1=NMF()
#results = cross_validate(algo, data, measures=['RMSE'], cv=3, verbose=True)

trainset = data.build_full_trainset()   #Build on entire data set
algo.fit(trainset)
#algo1.fit(trainset)
testset = trainset.build_anti_testset()


param_grid = {'n_factors':[25,50,100,150],'n_epochs': [10,20,30,40,50], 'lr_all': [0.002, 0.005,0.01],'reg_all': [0.02,0.1,0.4, 0.6]}
gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=5)
gs.fit(data)
# best RMSE score
print(gs.best_score['rmse'])
# combination of parameters that gave the best RMSE score
print(gs.best_params['rmse'])


"""
param_grid2 = {'n_factors':[25,50,100,150],'n_epochs': [10,20,30,40,50]}
gs2 = GridSearchCV(NMF, param_grid2, measures=['rmse', 'mae'], cv=5)
gs2.fit(data)
# best RMSE score
print(gs2.best_score['rmse'])
# combination of parameters that gave the best RMSE score
print(gs2.best_params['rmse'])

"""





#Predicting the ratings for testset
predictions = algo.test(testset)
#predictions1=algo1.test(testset)
erreur=accuracy.rmse(predictions)
#erreur1=accuracy.rmse(predictions1)

def get_all_predictions(prediction,n):
 
    # First map the predictions to each user.
    similar_n = defaultdict(list)    
    for uid, iid, true_r, est, _ in prediction:
        similar_n[uid].append((iid, est))

    # sort the predictions for each user
    for uid, user_ratings in similar_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        similar_n[uid]=user_ratings[:n]
    return similar_n
n=4
pred_user  =get_all_predictions(predictions,n)

#pred_user1= get_all_predictions(predictions1,n)

tmp = pd.DataFrame.from_dict(pred_user)
tmp_transpose = tmp.transpose()

#recommandation pour user 16
user_id= 1
results_pred = tmp_transpose.loc[user_id]

#format de results_pred (moviedid, rating), mais on va extraire movieID
recommended_movie_ids=[]
for x in range(0, n):
    recommended_movie_ids.append(results_pred[x][0])
  
recommended_movies = HDF[HDF['hotel_id'].isin(recommended_movie_ids)]
