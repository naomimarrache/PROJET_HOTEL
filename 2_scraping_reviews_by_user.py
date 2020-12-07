# -*- coding: utf-8 -*-
"""
2e ETAPE: Recupérer quelques comentaires d'hotel pour chaque utilisateur


TEMPS EXECUTION : POUR 1000 USER == 33 MINUTES

"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import requests



def is_hotel(div):
    review_type = div.find('div',class_="_2X5tM2jP _2RdXRsdL _1gafur1D").find("a")['href'][:13]
    if review_type == '/Hotel_Review':
        return True
    return False


def display_more(driver):
    #afficher tous les commentaires en cliqaunt sur PLUS pour avoir tous les reviews by user
    try:
        driver.find_element_by_css_selector("button._1JOGv2rJ").click()
        print("click PLUS")
    except:
        print("Bouton PLUS pas trouvé")



def create_csv_url_review(filename,username_list,url_reviews_to_scrap):
    df = pd.DataFrame({"username":username_list,"url_review":url_reviews_to_scrap})    
    df = df.drop_duplicates()
    df.to_csv(filename, index = False, header=True,encoding='utf-8-sig')



if __name__ == "__main__":
    
    df_user = pd.read_csv('users_profile_url.csv')
    #df_user = df_user[400:]
    driver = webdriver.Firefox()
    rate_list, review_list, title_list, url_hotel_list,  user_list = [], [], [], [], []
    url_prefix = "https://www.tripadvisor.fr"
    url_reviews_to_scrap = []
    username_list = []

    try:
        for user_no, url_profile in enumerate(df_user.url_profile):
            print(user_no)
            username = url_profile.replace('https://www.tripadvisor.fr/Profile/','')
            driver.get(url_profile)
            driver.execute_script('document.body.style.MozTransform = "scale(0.3)";')
            #afficher tous les commentaires en cliqaunt sur PLUS pour avoir tous les reviews by user
            #display_more(driver)
            time.sleep(0.5)
            try:
                soup = BeautifulSoup(driver.page_source,'lxml')
            #url_reviews_to_scrap = []
            
                div_selector = soup.find_all('div',class_ = "f14S8Wzw")
                for div in div_selector:
                    if(is_hotel(div)):
                        url_review = div.find('div',class_ = "_1kKLd-3D").find("a",class_="")['href']
                        url_reviews_to_scrap.append(url_prefix+ url_review)
                        username_list.append(username)
            except:
                print("ERREUR, possible : Trop de données à charger, tant pis pour cet user !")
        create_csv_url_review("reviews_url2.csv",username_list,url_reviews_to_scrap)
        #scraping_reviews_by_reviews_list(url_reviews_to_scrap,username,user_list,rate_list,review_list,title_list)
    #create_csv_review("reviews.csv",user_list,rate_list,title_list,review_list)
    except:
        print("Interruption manuelle ou autre problème rencontré..")
        print("PROFILE USER en cours de traitement :  ", url_profile)
        create_csv_url_review("reviews_url2.csv",username_list,url_reviews_to_scrap)
        
     #   print("Interruption manuelle ou autre problème rencontré..")
        #create_csv_review("reviews.csv",user_list,rate_list,title_list,review_list)

    
        






