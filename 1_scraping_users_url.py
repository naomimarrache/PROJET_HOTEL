# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

"""
1er ETAPE : Obtenir une base de user depuis une page de commentaire 
         d'un hotel quelconque
         
biais : On se basant sur cette méthode on risque d'avoir une base d'user 
        correspondant à une clientèle pas assez élargie
        
        --> Se baser sur plusieurs hotels (luxe et accessibles)
"""
    
# function to check if the button is presnent on the page, to avoid miss-click problem
def check_exists_by_css_selector(css_selector):
    try:
        driver.find_element_by_xpath(css_selector)
    except NoSuchElementException:
        return False
    return True


def scrap_url_user_by_hotel_page(driver,url_hotel_base,url_list_user,username_list):        
    driver.get(url_hotel_base)
    driver.execute_script('document.body.style.MozTransform = "scale(0.3)";')
    while True:
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        div_selector= soup.find_all('div',class_="_2wrUUKlw _3hFEdNs8")
        for div in div_selector:
            sufix_url = div.find("a",class_= "ui_header_link _1r_My98y")['href']
            url_list_user.append(prefix_url+sufix_url)
            username_list.append(sufix_url.replace('/Profile/',""))
        try:
            driver.find_element_by_css_selector('a.ui_button:nth-child(2)').click()
        except:
            print("erreur")
            break


def create_csv_with_lists(filename,column_name1,column_name2,url_list_user,username_list):
    df = pd.DataFrame({column_name1:url_list_user,column_name2:username_list})    
    df = df.drop_duplicates()
    df.to_csv(filename, index = False, header=True,encoding='utf-8-sig')

if __name__=="__main__":    
    try : 
        url_hotel_base1 = "https://www.tripadvisor.fr/Hotel_Review-g187184-d198204-Reviews-Hotel_Barriere_Le_Normandy_Deauville-Deauville_City_Calvados_Basse_Normandie_Normandy.html"
        driver = webdriver.Firefox()
        url_list_user, username_list = [], []
        prefix_url= "https://www.tripadvisor.fr"
        scrap_url_user_by_hotel_page(driver,url_hotel_base1,url_list_user,username_list)
        #on pourrait rajouter une page d'hotel plus bas de gamme pour avoir une clientèle élargie 
        #scrap_url_user_by_hotel_page(driver,url_hotel_base2,url_list_user)
        create_csv_with_lists("users_profile_url.csv","url_profile","username",url_list_user,username_list)
    except:
        print("Interruption manuelle ou autre problème rencontré..")
        create_csv_with_lists("users_profile_url.csv","url_profile","username",url_list_user,username_list)
    

  








