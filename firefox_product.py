# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 09:24:13 2020
@author: User
"""

import pandas as pd
from selenium import webdriver
#from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait as W
#from selenium.webdriver.support import expected_conditions as E
import csv
from urllib import parse
import re
import time


df = pd.read_excel (r'C:\Users\User\Desktop\Asin.xlsx')
links = []
def get_url():
    asin = []
    asin = list(df['Asin'])
    
    for i in range(len(asin)):
        links.append('https://www.amazon.com/dp/' + asin[i])
    
        

get_url()
records = []
seller_records = []

def extract_record(links):
    
    #creating instance of webdriver
    chromedriver = "C:\Chromedriver\chromedriver"
    driver = webdriver.Chrome(chromedriver)
    driver.maximize_window()
    driver.get('https://www.amazon.com/dp/B012IOVJJG')
    driver.implicitly_wait(3)
    
    anchor_loc = driver.find_element_by_xpath('/html/body/div[2]/header/div/div[4]/div[1]/div/span/a').click()
    driver.implicitly_wait(3)
    input_loc = driver.find_element_by_id('GLUXZipUpdateInput').send_keys('90001')
    driver.implicitly_wait(3)
    input_loc = driver.find_element_by_id('GLUXZipUpdateInput').send_keys(Keys.ENTER)
    driver.get('https://www.amazon.com/dp/B012IOVJJG')
    
    url = 'https://keepa.com/#!'
    time.sleep(2)
    driver.get(url)
    time.sleep(5)
    driver.implicitly_wait(3)
    
    div = driver.execute_script("document.getElementById('loginOverlay').style.display = 'block';")
    
    username = driver.find_element_by_id('username').send_keys('hozyali')
    
    password = driver.find_element_by_id('password').send_keys('eSP@$_502')
    
    submit = driver.find_element_by_id('submitLogin').send_keys(Keys.ENTER)
    
    count = 0
    for i in range(len(links)):
    #extract and record data item from a single record
        
        driver.implicitly_wait(5)
        driver.get(links[i])
        item = links[i]
        

        try:    
             # find price xpath
             price = ''
             price = driver.find_element_by_class_name('priceBlockBuyingPriceString').text.strip()
        except AttributeError:
              # is not found
             price = ''
        except Exception:
            print('Price tag doesn`t exists')
        
        
        try:
            # Getting asin and dimensions
            product_detail = ''
            product_lists = ''
            product_detail = driver.find_element_by_class_name('detail-bullet-list')
            product_lists = product_detail.find_elements_by_class_name('a-list-item')
            
            for items in range(len(product_lists)):
                 if("ASIN" in product_lists[items].text.strip()):
                     vlaue=product_lists[items].text.strip()
                     vlaue=vlaue.split(":")
                     asin = vlaue[1].strip()
                 if("Dimensions" in product_lists[items].text.strip()):
                     vlaue=product_lists[items].text.strip()
                     vlaue=vlaue.split(":")
                     dimen = vlaue[1].strip()
                 
        except AttributeError:
            product_detail = ''
            product_lists = ''
        except Exception:
            print('Asin tag and Dimension tag doesn`t exists')
        
        
        try:

            ranking_detail = driver.find_element_by_id('detailBulletsWrapper_feature_div').find_elements_by_tag_name('ul')[1]
            ranking = ranking_detail.find_element_by_class_name('a-list-item').text.strip()
            ranking = ranking.split(":")
            ranking = ranking[1].strip()
            ranking = ranking.replace(',','')
            rank = re.findall('[0-9]+',ranking)
            
        except AttributeError:
            ranking = ''
        except Exception:
            print('Ranking tag doesn`t exists')
            
        
        try:    
             # find rating xpath
             rating = ''
             rate = driver.find_element_by_id('detailBullets_averageCustomerReviews')
             rating = rate.find_element_by_class_name('reviewCountTextLinkedHistogram').get_attribute('title')

        except AttributeError:
              # is not found
             rating = ''
        except Exception:
            print('Rating tag doesn`t exists')
            
        try:    
             # find competitors href
              competitors = ''
              competitors = driver.find_element_by_id('olp_feature_div').find_element_by_tag_name('a').get_attribute('href')
              
        except AttributeError:
              # is not found
              competitors = ''
        except Exception:
            print('Competitors link tag doesn`t exists')
                    
        
        try:    
             # find buybox price
              buybox_price = ''
              buybox_price = driver.find_elements_by_id('price_inside_buybox')[0].text.strip()
              
        except AttributeError:
              # is not found
              buybox_price = ''
        except Exception:
            print('BuyBox price tag doesn`t exists')
        
        
        try:
            #find buybox items
            buy_box_con = driver.find_element_by_class_name('buybox-tabular-container')
            box_elem = buy_box_con.find_elements_by_class_name('buybox-tabular-column')
        except AttributeError:
              # is not found
              buy_box_con = ''
              box_elem = ''
        except Exception:
               print('BuyBox FBA Column tags doesn`t exists')
            
        try:
            buy_box = []
            #adding buybox elements
            for elems in range(len(box_elem)):
                buy_box.append(box_elem[elems].text)
        except AttributeError:
               buy_box = []
        except Exception:
               print('BuyBox ship from and sold by tag doesn`t exists')
        
        
        try:
            #adding links if not sold by amazon
            atag = ''
            atag += driver.find_element_by_xpath('//*[@id="sellerProfileTriggerId"]').get_attribute('href')
            params = dict(parse.parse_qsl(parse.urlsplit(atag).query))
            seller = params['seller']
        except AttributeError:
            atag = ''
        except Exception:
            print('BuyBox Seller tag doesn`t exists')
        
         
        try:
            # Getting title
            title = driver.find_element_by_id('productTitle').text.strip()
        except AttributeError:
            title = ''
        except Exception:
            print('Product Title tag doesn`t exists')
        
        try:
            # Getting parent/Niche
            parent = driver.find_element_by_xpath('//*[@id="wayfinding-breadcrumbs_feature_div"]/ul/li[1]/span/a').text.strip()
        except AttributeError:
            parent = ''
        except Exception:
            print('Parent/Niche tag doesn`t exists')

        try:
            comp_link = 'https://www.amazon.com/gp/offer-listing/'+asin+'/ref=olp_f_new?f_primeEligible=true&f_new=true'
            driver.get(comp_link)
            comp_price = []
            comp_cond = []
            comp_atag_text = []
            comp_atag = []
            fba = []
            comp_btag_text = []
            seller_array = []
            driver.get(comp_link)
            div_list_column = driver.find_element_by_id('olpOfferListColumn')
            div = driver.find_elements_by_class_name('olpOffer')

            
            def comp_data(div):
                for i in range(len(div)):
                    
                    row = driver.find_elements_by_class_name('olpOffer')[i]
                    comp_price.append(row.find_element_by_class_name('olpPriceColumn').find_element_by_class_name('olpOfferPrice').text.strip())
                    driver.implicitly_wait(2)
                    comp_cond.append(row.find_element_by_class_name('olpConditionColumn').find_element_by_class_name('olpCondition').text.strip())
                    
                    
                    fba_div = row.find_element_by_class_name('olpDeliveryColumn').find_element_by_class_name('olpBadgeContainer').find_element_by_class_name('olpBadge')
                    
                    fba.append(fba_div.find_element_by_tag_name('a').text.strip())
                    
                    comp_btag_text.append(row.find_element_by_class_name('olpSellerColumn').find_element_by_tag_name('b').text.strip())    
                    
                    comp_div = row.find_element_by_class_name('olpSellerColumn').find_elements_by_tag_name('a')
                    
                    
                    comp_div = row.find_element_by_class_name('olpSellerColumn').find_elements_by_tag_name('a')[0].get_attribute('href')
                    
                    
                    comp_adiv = row.find_element_by_class_name('olpSellerColumn').find_elements_by_tag_name('a')[0].text.strip()
        
                    comp_atag.append(comp_div)
        
                    comp_atag_text.append(comp_adiv)
        
                    seller_params = dict(parse.parse_qsl(parse.urlsplit(comp_div).query))
                    seller_array.append(seller_params['seller'])
                       
                    
            comp_data(div)
            
            condition = True
            while condition:
                try:
                    pagination = div_list_column.find_element_by_class_name('a-pagination')
                    next_page = pagination.find_elements_by_tag_name('a')[-1].click()
                    comp_data(div)
                except AttributeError:
                    next_page = ''
                except:
                    condition = False
            
            
        except AttributeError:
            comp_link = ''
        except Exception:
            print('Competitors Link doesn`t exists')
        
            
        try:    
            market_id = []
            me_id = []
            seller_product_asin = []
            seller_url = []
            
            
            def seller_info(comp_atag):
                
                for i in comp_atag:
                    
                    driver.get(i)
                    product_link = driver.find_element_by_id('products-link').find_element_by_tag_name('a').click()
                    current_url = driver.current_url
                    seller_url.append(current_url)
                    url = dict(parse.parse_qsl(parse.urlsplit(current_url).query))
                    market_id.append(url['marketplaceID'])
                    me_id.append(url['me'])
                    
                    product_list = driver.find_element_by_class_name('s-main-slot').find_elements_by_class_name('s-result-item')
                    for value in product_list:
                        asin_array = ''
                        asin_array = value.get_attribute('data-asin')
                        if (asin_array == ''):
                            continue
                        else:
                            
                            seller_product_asin.append(asin_array)
                        
                    condition = True
                    while condition:
                        try:
                            pagination = driver.find_element_by_class_name('a-pagination')
                            next_page = pagination.find_element_by_class_name('a-last').find_element_by_tag_name('a').click()
                            product_list = driver.find_element_by_class_name('s-main-slot').find_elements_by_class_name('s-result-item')
                            for value in product_list:
                                seller_product_asin.append(value.get_attribute('data-asin'))
                        except:
                            condition = False
                            
                print(len(seller_product_asin))
        except Exception:
            print('Seller info doesn`t exists')
        

        seller_info(comp_atag)                    
       
        try:
            driver.get('https://keepa.com/#!product/1-'+asin)
            
            time.sleep(5)
            
            content_div = driver.execute_script("document.getElementById('statisticsContent').style.display = 'block';")
            
            average = driver.find_element_by_id('statsTable').find_elements_by_class_name('statsRow5')[3].text.strip()
            
            average = average.split('\n')
            
            avg = average[0]
            
            avg = avg.replace(',','')
            
            keepa = re.findall('[0-9]+',avg)
        except AttributeError:
            keepa = ''
        except Exception:
            print('Keepa Link doesn`t exists')
        
        
                 
        def seller_data(seller_product_asin):
            seller_links = []
            for i in seller_product_asin:
                
                seller_links.append('https://www.amazon.com/dp/' + i)
                for j in seller_links:
                    driver.get(j)
                    
                    try:    
                         # find price xpath
                         seller_price = ''
                         seller_price = driver.find_element_by_class_name('priceBlockBuyingPriceString').text.strip()
                    except AttributeError:
                          # is not found
                         seller_price = ''
                    except Exception:
                        print('Price tag doesn`t exists')
                    
                    
                    try:
                        # Getting asin and dimensions
                        product_detail = ''
                        product_lists = ''
                        product_detail = driver.find_element_by_class_name('detail-bullet-list')
                        product_lists = product_detail.find_elements_by_class_name('a-list-item')
                        
                        for items in range(len(product_lists)):
                             if("ASIN" in product_lists[items].text.strip()):
                                 vlaue=product_lists[items].text.strip()
                                 vlaue=vlaue.split(":")
                                 seller_asin = vlaue[1].strip()
                             if("Dimensions" in product_lists[items].text.strip()):
                                 vlaue=product_lists[items].text.strip()
                                 vlaue=vlaue.split(":")
                                 seller_dimen = vlaue[1].strip()
                             
                    except AttributeError:
                        product_detail = ''
                        product_lists = ''
                    except Exception:
                        print('Asin tag and Dimension tag doesn`t exists')
                    
                    
                    try:
            
                        ranking_detail = driver.find_element_by_id('detailBulletsWrapper_feature_div').find_elements_by_tag_name('ul')[1]
                        ranking = ranking_detail.find_element_by_class_name('a-list-item').text.strip()
                        ranking = ranking.split(":")
                        ranking = ranking[1].strip()
                        seller_ranking = ranking.replace(',','')
                        seller_rank = re.findall('[0-9]+',ranking)
                        
                    except AttributeError:
                        seller_ranking = ''
                    except Exception:
                        print('Ranking tag doesn`t exists')
                        
                    
                    try:    
                         # find rating xpath
                         rating = ''
                         rate = driver.find_element_by_id('detailBullets_averageCustomerReviews')
                         seller_rating = rate.find_element_by_class_name('reviewCountTextLinkedHistogram').get_attribute('title')
            
                    except AttributeError:
                          # is not found
                         seller_rating = ''
                    except Exception:
                        print('Rating tag doesn`t exists')
                        
                    try:    
                         # find competitors href
                          seller_competitors = ''
                          seller_competitors = driver.find_element_by_id('olp_feature_div').find_element_by_tag_name('a').get_attribute('href')
                          
                    except AttributeError:
                          # is not found
                          seller_competitors = ''
                    except Exception:
                        print('Competitors link tag doesn`t exists')
                                
                    
                    try:    
                         # find buybox price
                          seller_buybox_price = ''
                          seller_buybox_price = driver.find_elements_by_id('price_inside_buybox')[0].text.strip()
                          
                    except AttributeError:
                          # is not found
                          seller_buybox_price = ''
                    except Exception:
                        print('BuyBox price tag doesn`t exists')
                    
                    
                    try:
                        #find buybox items
                        buy_box_con = driver.find_element_by_class_name('buybox-tabular-container')
                        box_elem = buy_box_con.find_elements_by_class_name('buybox-tabular-column')
                    except AttributeError:
                          # is not found
                          buy_box_con = ''
                          box_elem = ''
                    except Exception:
                           print('BuyBox FBA Column tags doesn`t exists')
                        
                    try:
                        seller_buy_box = []
                        #adding buybox elements
                        for elems in range(len(box_elem)):
                            seller_buy_box.append(box_elem[elems].text)
                    except AttributeError:
                           seller_buy_box = []
                    except Exception:
                           print('BuyBox ship from and sold by tag doesn`t exists')
                    
                    
                    try:
                        #adding links if not sold by amazon
                        seller_atag = ''
                        seller_atag += driver.find_element_by_xpath('//*[@id="sellerProfileTriggerId"]').get_attribute('href')
                        params = dict(parse.parse_qsl(parse.urlsplit(seller_atag).query))
                        seller_seller = params['seller']
                    except AttributeError:
                        seller_atag = ''
                    except Exception:
                        print('BuyBox Seller tag doesn`t exists')
                    
                     
                    try:
                        # Getting title
                        seller_title = driver.find_element_by_id('productTitle').text.strip()
                    except AttributeError:
                        seller_title = ''
                    except Exception:
                        print('Product Title tag doesn`t exists')
                    
                    try:
                        # Getting parent/Niche
                        seller_parent = driver.find_element_by_xpath('//*[@id="wayfinding-breadcrumbs_feature_div"]/ul/li[1]/span/a').text.strip()
                    except AttributeError:
                        seller_parent = ''
                    except Exception:
                        print('Parent/Niche tag doesn`t exists')
                    seller_result = (seller_title,seller_price,seller_dimen,seller_ranking,seller_rank,seller_competitors,seller_parent,seller_buy_box,seller_buybox_price,seller_atag,seller_rating)        
                    seller_records.append(seller_result)
        seller_data(seller_product_asin)                
        
        
        seller_result = (seller_product_asin,market_id,me_id,seller_url)
        result = (title,price,dimen,asin,keepa,ranking,rank,competitors,parent,buy_box,buybox_price,atag,rating,item,comp_link,seller,seller_array,comp_price,comp_cond,fba,comp_btag_text,comp_atag_text,comp_atag)
        count += 1        
        records.append(result)
        seller_records.append(seller_result)
        print(count)
extract_record(links)        


# exporting records into csv  
with open ('result.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Description',
                     'Price',
                     'product Dimension',
                     'Asin',
                     'Keepa',
                     'Best Sellers Rank',
                     'Best seller numeric values',
                     'Competetors Link',
                     'Parent/Niche',
                     'buybox',
                     'Buybox price',
                     'href',
                     'Rating',
                     'Asin links',
                     'Altered Competitors link',
                     'Current Seller ID',
                     'Array of seller IDs',
                     'Competitors Price',
                     'Seller Product Condition',
                     'Fullfillment By',
                     'Seller Product Rating',
                     'Seller Name',
                     'Seller links',                     
                     ])
    writer.writerows(records)


with open ('seller_result.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
                     'Description',
                     'Price',
                     'product Dimension',
                     'Asin',
                     'Keepa',
                     'Best Sellers Rank',
                     'Best seller numeric values',
                     'Competetors Link',
                     'Parent/Niche',
                     'buybox',
                     'Buybox price',
                     'href',
                     'Rating',
                     'List of seller asin',
                     'Market_id',
                     'Me_id',
                     'Seller_url',
                     ])
    writer.writerows(seller_records)
    
