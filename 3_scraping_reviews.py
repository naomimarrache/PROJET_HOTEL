# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import requests
import re

"""
15sec 10review
1500sec 1000rev
6000sec 4000rev  == 1h36
"""


def scraping_review_by_review_url(url_review,username,user_list,rate_list,review_list,title_list,url_hotel_list):
    #<div class="rev_wrap ui_columns is-multiline"><div class="ui_column is-2-desktop is-12-tablet is-12-mobile"><div class="prw_rup prw_reviews_member_info_resp_sur" data-prwidget-name="reviews_member_info_resp_sur" data-prwidget-init="handlers"><div class="member_info"><div id="UID_0D0AA75FE7C7AB210F0EEE01CDC54A04-SRC_778367197" class="memberOverlayLink" onmouseover="widgetEvCall('handlers.initMemberOverlay', event, this);" data-anchorwidth="90"><div class="avatar profile_0D0AA75FE7C7AB210F0EEE01CDC54A04"><div class="avatarWrapper"><a><div class="prw_rup prw_common_basic_image avatarImage" data-prwidget-name="common_basic_image" data-prwidget-init=""><div class="ui_avatar resp"> <img src="https://media-cdn.tripadvisor.com/media/photo-l/1a/f6/e7/99/default-avatar-2020-57.jpg" class="basicImg" data-mediaid="452388761"></div></div></a></div></div><div class="info_text" onclick="widgetEvCall('handlers.usernameClick', event, this);"><div>Flo o</div><div class="userLoc"><strong>Paris</strong></div></div></div><div id="UID_0D0AA75FE7C7AB210F0EEE01CDC54A04-SRC_778367197" class="memberOverlayLink" onmouseover="widgetEvCall('handlers.initMemberOverlay', event, this);" data-anchorwidth="90"><div class="memberBadgingNoText is-shown-at-desktop"><span class="ui_icon pencil-paper"></span><span class="badgetext">46</span><span class="ui_icon thumbs-up"></span><span class="badgetext">50</span></div></div></div></div></div><div class="ui_column is-10-desktop is-12-tablet is-12-mobile"><div class="quote isNew"><h1 id="HEADING" class="title">Hôtel très confortable et parfaitement situé, mais service pas à la hauteur</h1></div><div class="altHeadInline" onclick="(ta.prwidgets.getjs(this,'handlers')).clickHeadingHrLink('/Hotel_Review-g187184-d198204-Reviews-Hotel_Barriere_Le_Normandy_Deauville-Deauville_City_Calvados_Basse_Normandie_Normandy.html')">Avis sur <a href="/Hotel_Review-g187184-d198204-Reviews-Hotel_Barriere_Le_Normandy_Deauville-Deauville_City_Calvados_Basse_Normandie_Normandy.html">Hôtel Barrière Le Normandy Deauville</a></div><span class="ui_bubble_rating bubble_30"></span><span class="ratingDate" title="3 décembre 2020">Avis publié : Il y a 3&nbsp;jours </span><div class="prw_rup prw_reviews_resp_sur_review_text" data-prwidget-name="reviews_resp_sur_review_text" data-prwidget-init="handlers"><div class="entry"><p class="partial_entry"><span class="summaryText">Nous avons ressenti l'impression d'un hôtel usine. Dès le check-in l'accueil fut plus que moyen et expéditif. On ne nous précise pas les horaires du petit déjeuner (la base), les conditions d'accès au parking. Lorsqu’ensuite on accède au parking à pied pour récupérer quelque chose à notre voiture, et que la porte pour en ressortir est fermée, on appelle la réception qui nous rétorque d’une façon obséquieuse «&nbsp;il fallait demander l’ouverture avant de descendre&nbsp;!&nbsp;» ah oui… tellement évident quand on ne nous a rien dit avant, alors qu’on peut y rentrer sans problème. Limite on se fait engueuler… Genre que faites vous dans le parking&nbsp;? La porte était ouverte on avait besoin de récupérer quelque chose à notre voiture, et on ne savait pas les modalités pour en ressortir. Et par 2 ou 3 fois on nous a répondu de la sorte, tout avait l’air tellement évident sans qu’on ne nous ai rien expliqué.
    #<h1 id="HEADING" class="title">Hôtel très confortable et parfaitement situé, mais service pas à la hauteur</h1>
    #print(url_review)
    review_div_class = "rev_wrap ui_columns is-multiline" 
    title_class = "title"
    review_text_class = "entry"
    url_hotel_div_class = "altHeadInline"
    url_prefix = "https://www.tripadvisor.fr"
    
    r=requests.get(url_review)
    soup_ = BeautifulSoup(r.text, 'lxml')
    review_div= soup_.find('div',class_=review_div_class)
    title = review_div.find('h1',class_=title_class).text
    review_text = review_div.find('div',class_=review_text_class).text
    review_text = review_text.replace('\t', ' ').replace('\n', ' ')
    rate = int(review_div.find('span',class_="ui_bubble_rating")['class'][1].split('bubble_')[1])/10
    url_hotel = review_div.find('div',class_=url_hotel_div_class).find('a')['href']
    title_list.append(title)
    review_list.append(review_text)
    rate_list.append(rate)
    user_list.append(username)
    url_hotel_list.append(url_prefix+url_hotel)        
        
        

def create_csv_review(filename,user_list,url_hotel_list,rate_list,title_list,review_list):
    df = pd.DataFrame({"username":user_list,"rate":rate_list,"title":title_list,"review":review_list,"url_hotel":url_hotel_list})    
    df = df.drop_duplicates()
    df.to_csv(filename, index = False, header=True,encoding='utf-8-sig')




if __name__ == '__main__':
    df_url_reviews = pd.read_csv('reviews_url.csv')
    rate_list, review_list, title_list, url_hotel_list,  user_list = [], [], [], [], []
    try:
        for i in range(df_url_reviews.shape[0]):
            username = df_url_reviews.username[i]
            url_review_to_scrap = df_url_reviews.url_review[i]
            print(str(i)+ " "+ url_review_to_scrap)
            try:
                scraping_review_by_review_url(url_review_to_scrap,username,user_list,rate_list,review_list,title_list,url_hotel_list)
            except:
                print("ERREUR durant le scraping de "+ url_review_to_scrap +"  DE  "+ username )
        create_csv_review("reviews2.csv",user_list,url_hotel_list,rate_list,title_list,review_list)
    except:
        print("\n\nInterruption manuelle ou autre problème rencontré..")
        print("REVIEW URL en cours de traitement :  ", url_review_to_scrap)
        create_csv_review("reviews2.csv",user_list,url_hotel_list,rate_list,title_list,review_list)
        
            


