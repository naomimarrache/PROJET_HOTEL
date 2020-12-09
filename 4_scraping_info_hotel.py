# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import requests
import pandas as pd

"""

on fai tle choix de pas scraper ni le prix (pas toujours la en fction des dates) 
ni type de chambre (pas toujours la)
localisation recupéres sous forme Europe > France > Normandie ... > Deauville
            --> possibilité de faire un tfidf 
penser à remplacer les none par la moyenne des notes dans cette categorie dans la ville, ou le pays

"""


def find_price_similar_hotel_by_url(url_similar):
    r=requests.get(url_similar)
    soup_ = BeautifulSoup(r.text, 'lxml')  
    try:
        prix = soup_.find_all('div',class_="price")[2].text.replace("€","")
    except:
        prix = None
    return prix
    


def list_to_str_with_sep(list_,sep):
    str_ = ""
    for elem in list_:
        str_ = str_ + sep + str(elem)
    str_ = str_[len(sep):]
    return str_ 

def position_str_to_ratio(position_str):
    tab = position_str.replace(" ","").split("sur")
    ratio = (int(tab[1])-int(tab[0]))/int(tab[1])
    return ratio

def contain_lang(str_):
    lang_list = ['Anglais', 'Russe', 'Arabe', 'Français', 'Espagnol']
    for lang in lang_list:
        if lang in str_:
            return True
    return False
        

def scrap_infos_hotel_by_url(driver,url, name_hotel_list,url_hotel_list, adress_hotel_list, price_hotel_list, position_by_city_hotel_list,  city_hotel_list,country_hotel_list, localisation_hotel_list, global_rate_hotel_list, category_hotel_list, style_hotel_list, equipments_hotel_list):
    driver.get(url)
    driver.execute_script('document.body.style.MozTransform = "scale(0.3)";')
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source,'lxml')
    try:
        name_hotel  = soup.find('h1',class_="_1mTlpMC3").text
    except:
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source,'lxml')
        name_hotel  = soup.find('h1',class_="_1mTlpMC3").text
    adress_hotel = soup.find('div',class_="vEwHDg4B _1WEIRhGY").text  
    
    price_hotel = "NotFound"
    try:
        price_hotel = soup.find('div',class_="ui_columns is-mobile is-multiline is-vcentered is-gapless-vertical _2mWM5u8t").text.replace("€","").replace("Voir l'offre","").strip()
    except:
        try:
            try:
                price_hotel = soup.find('div',class_="ui_columns is-gapless is-mobile").text.replace("€","").replace("Voir l'offre","").strip()
            except:
                price_hotel = soup.find('div',class_="_3kGtuPhC").text.replace("€","").replace("Voir l'offre","").strip()
        except:
            price_hotel = "NotFound"
            #price_hotel = soup.find('div',class_="_3U1VaTGs").text.replace("€","").strip()
    if len(price_hotel.strip())==0 or price_hotel=="NotFound":
        price_hotel = None
        
    if price_hotel==None:
        print("no price")
        try:
            url_similar_hotel = "https://www.tripadvisor.fr"+soup.find('a',class_="_3TKvRNea ui_button primary")['href']
            print(url_similar_hotel)
            #url_similar_hotel = soup.find('a',class_="_3TKvRNea ui_button primary")['href']
            price_hotel = find_price_similar_hotel_by_url(url_similar_hotel)
            print("\nSimlar hotel price : "+ price_hotel)
        except:
            price_hotel = None

        
    position_by_city_hotel = soup.find('div',class_="_1vpp5J_x").text.split("H")[0].strip().replace('Nº','')
    #ville_hotel = soup.find('div',class_="_1vpp5J_x").find('a').text
    localisation_hotel_selector = soup.find('ul',class_="breadcrumbs").find_all('li',class_="breadcrumb")[:-1]
    localisation_hotel = [ geo_level.text.replace(u'\xa0', u'').strip() for geo_level in localisation_hotel_selector ]
    localisation_hotel = list_to_str_with_sep(localisation_hotel,"||")
    city_hotel = localisation_hotel_selector[-1].text
    country_hotel = localisation_hotel_selector[1].text
    global_rate_hotel = soup.find('span',class_="_3cjYfwwQ").text.replace(",",".")
    try:
        category_hotel = soup.find('svg',class_="_2aZlo29m")['title'].split("sur")[0].strip().replace(',','.')
    except:
        category_hotel = None
        
    
    style_divs = soup.find_all('div',class_="_2dtF3ueh")[1:-1]
    if len(soup.find_all('div',class_="_2jJmIDsg"))==2:    
        style_divs = soup.find_all('div',class_="_2dtF3ueh")[1:]   
    style_hotel = [div.text for div in style_divs]
    style_hotel = list_to_str_with_sep(style_hotel,"||")
    if(contain_lang(style_hotel)):
        style_hotel = None
    #types_room_divs = soup.find_all("div",class_="_1nAmDotd")[2].find_all('div',class_="_2rdvbNSg")
    #types_room_hotel = [div.text for div in types_room_divs]
    try:
        driver.find_element_by_class_name("_80614yz7").click()
        soup = BeautifulSoup(driver.page_source,'lxml')
        equipments_hotel_div = soup.find_all('div',class_="_2rdvbNSg")
        equipments_hotel = [div.text for div in equipments_hotel_div]
        equipments_hotel = list_to_str_with_sep(equipments_hotel,"||")
    except:
        equipments_hotel_divs = soup.find_all("div",class_="_1nAmDotd")[0].find_all('div',class_="_2rdvbNSg")
        equipments_hotel = [div.text.replace(u'\xa0', u'').strip() for div in equipments_hotel_divs]
        equipments_hotel = list_to_str_with_sep(equipments_hotel,"||")


    
    name_hotel_list.append(name_hotel)
    url_hotel_list.append(url)
    adress_hotel_list.append(adress_hotel)
    price_hotel_list.append(price_hotel)
    position_by_city_hotel_list.append(position_by_city_hotel)
    city_hotel_list.append(city_hotel)
    country_hotel_list.append(country_hotel)
    localisation_hotel_list.append(localisation_hotel)
    global_rate_hotel_list.append(global_rate_hotel)
    category_hotel_list.append(category_hotel)
    style_hotel_list.append(style_hotel)
    equipments_hotel_list.append(equipments_hotel)
    
    
        

def create_csv_hotels(filename,name_hotel_list,url_hotel_list, adress_hotel_list, price_hotel_list, position_by_city_hotel_list,  city_hotel_list,country_hotel_list, localisation_hotel_list, global_rate_hotel_list, category_hotel_list, style_hotel_list, equipments_hotel_list):
    dataf = pd.DataFrame({"name_hotel":name_hotel_list,"url_hotel":url_hotel_list,"adress_hotel":adress_hotel_list,"price_hotel":price_hotel_list,"position_by_city_hotel":position_by_city_hotel_list,"city_hotel":city_hotel_list,"country_hotel":country_hotel_list,"localisation_hotel":localisation_hotel_list,"global_rate_hotel":global_rate_hotel_list,"category_hotel":category_hotel_list,"style_hotel":style_hotel_list,"equipments_hotel":equipments_hotel_list})    
    dataf = dataf.drop_duplicates()
    dataf.to_csv(filename, index = False, header=True,encoding='utf-8-sig')
    return dataf


if __name__ == '__main__':
    df = pd.read_csv('reviews.csv')
    driver = webdriver.Firefox()
    list_url_hotel = pd.Series(df.url_hotel.unique())
    name_hotel_list, url_hotel_list, adress_hotel_list, price_hotel_list, position_by_city_hotel_list , country_hotel_list= [], [], [], [], [], []
    city_hotel_list, localisation_hotel_list, global_rate_hotel_list, category_hotel_list, style_hotel_list, equipments_hotel_list = [], [], [], [], [], []
    try: 
        for no,url in enumerate(list_url_hotel):
            print(str(no)+ "  "+url)
            #scrap_infos_hotel_by_url(driver,url)
            try:
                scrap_infos_hotel_by_url(driver,url, name_hotel_list, url_hotel_list, adress_hotel_list, price_hotel_list, position_by_city_hotel_list,  city_hotel_list,country_hotel_list, localisation_hotel_list, global_rate_hotel_list, category_hotel_list, style_hotel_list, equipments_hotel_list)
            except KeyboardInterrupt:
                driver.close()
                print("\n\nInterruption manuelle ou autre problème rencontré..")
                print("HOTEL URL en cours de traitement :  ", url)
                df_hotels = create_csv_hotels("hotels2.csv",name_hotel_list, url_hotel_list,adress_hotel_list, price_hotel_list, position_by_city_hotel_list,  city_hotel_list, country_hotel_list, localisation_hotel_list, global_rate_hotel_list, category_hotel_list, style_hotel_list, equipments_hotel_list)
                break            
            except Exception as e:
                print("\nERROR : erreur scraping, tant pis pour cet hotel ! \n")
        
        
        df_hotels = create_csv_hotels("hotels2.csv",name_hotel_list, url_hotel_list,adress_hotel_list, price_hotel_list, position_by_city_hotel_list,  city_hotel_list ,country_hotel_list, localisation_hotel_list, global_rate_hotel_list, category_hotel_list, style_hotel_list, equipments_hotel_list)
        print("HOTELS.CSV WELL CREATED ! 1")
    except:
        driver.close()
        print("\n\nInterruption manuelle ou autre problème rencontré..")
        print("HOTEL URL en cours de traitement :  ", url)
        df_hotels = create_csv_hotels("hotels2.csv",name_hotel_list, url_hotel_list,adress_hotel_list, price_hotel_list, position_by_city_hotel_list,  city_hotel_list, country_hotel_list, localisation_hotel_list, global_rate_hotel_list, category_hotel_list, style_hotel_list, equipments_hotel_list)
        print("HOTELS.CSV WELL CREATED ! 2")       
        



