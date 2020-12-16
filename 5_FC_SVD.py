# -*- coding: utf-8 -*-

import pandas as pd

from surprise import SVD, NMF, Reader, Dataset, accuracy
from surprise.model_selection.split import train_test_split

"""
Pour le filtrage collaboratif, nous faisons le choix d'
utilisé un filttrage collaboratif base modele et nonn memoire
car nous sommes dans le cas d'une matrice creuse

plus precisement nous utiliseros la factprisation matricielle
avec SVD( ou NMF) de surprise


http://dspace.univ-tlemcen.dz/bitstream/112/11348/1/Utilisation-de-factorisation-matricielle.pdf


NOTE : faire un grid search svd ou nmf
cf:
    https://towardsdatascience.com/svd-where-model-tuning-goes-wrong-61c269402919
"""


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

#construire les données d'entrainement
#trainset, testset = train_test_split(data,test_size = 0.20)

#on peut aussi entrainer autrement
trainset = data.build_full_trainset()
testset = trainset.build_anti_testset()

mod_SVD = SVD()
mod_NMF = NMF()

#entrainement du modèle
mod_SVD.fit(trainset)
mod_NMF.fit(trainset)

#test du modèle
pred_SVD = mod_SVD.test(testset)
pred_NMF = mod_NMF.test(testset)

#l'accuracy version rmse
print("la meilleure est la valeur de rmse la plus petite")
print("rmse pour SVD")
acc_rmse = accuracy.rmse(pred_SVD,verbose=True)
print("rmse pour NMF")
acc_rmse = accuracy.rmse(pred_NMF,verbose=True)

#on transforme en df et on récupère que l'user id 1
df_pred_svd = pd.DataFrame(pred_SVD)
user_1_pred = df_pred_svd[df_pred_svd['uid']==1]

#on prend les 4 meilleurs films
user_1_best_rating_pred = user_1_pred.sort_values(by='est',ascending = False)[:4]



"""
#on renomme le nom de la colonne pour pouvoir faire le merge
user_1_best_rating_pred = user_1_best_rating_pred.rename(columns={"iid": "movieId"})

#on fait le merge
pred_4_meilleurs_films_user_1 = user_1_best_rating_pred.merge(UHDF, on='movieId')

pred_4_meilleurs_films_user_1 = pred_4_meilleurs_films_user_1.drop(columns=['uid', 'r_ui','details','genres'])
"""


def generate_auto_id(list_id):
    id = list_id[len(list_id)-1]
    while True:
        if id in list_id:
            id = id  + 1
        else:
            break
    return id





from surprise import SVD,NormalPredictor
from surprise.model_selection import GridSearchCV


param_grid = {'n_factors':[50,100,150],'n_epochs':[10,20,30],  'lr_all':[0.005,0.01],'reg_all':[0.02,0.1]}
gs = GridSearchCV(SVD,param_grid, measures=['rmse'], cv=5)
gs.fit(data)
params = gs.best_params['rmse']




#1.1099016014705771


