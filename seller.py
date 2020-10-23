# -*- coding: utf-8 -*-
# *** Spyder Python Console History Log ***

#import pandas as pd
from selenium import webdriver
#from bs4 import BeautifulSoup
#from selenium.webdriver.chrome.options import Options 
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import time
from urllib import parse
import csv


url = 'https://www.amazon.com/dp/' + 'B012IOVJJG'
chromedriver = "C:\Chromedriver\chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.maximize_window()
driver.get(url)
driver.implicitly_wait(3)
     
anchor_loc = driver.find_element_by_xpath('//*[@id="nav-global-location-slot"]/span/a').click()
driver.implicitly_wait(2)
input_loc = driver.find_element_by_id('GLUXZipUpdateInput').send_keys('90001')
driver.implicitly_wait(2)
input_loc = driver.find_element_by_id('GLUXZipUpdateInput').send_keys(Keys.ENTER)
driver.get(url)
driver.get('https://www.amazon.com/gp/offer-listing/' + 'B012IOVJJG' + '/ref=olp_f_new?f_primeEligible=true&f_new=true')

comp_price = []
comp_cond = []
comp_atag_text = []
comp_atag = []
fba = []
comp_btag_text = []
seller_array = []

div_list_column = driver.find_element_by_id('olpOfferListColumn')
div = driver.find_elements_by_class_name('olpOffer')
competitors_record = []

def comp_data(div):
    
    for i in range(len(div)):
        row = driver.find_elements_by_class_name('olpOffer')[i]
        #comp_price.append(row.find_element_by_class_name('olpPriceColumn').find_element_by_class_name('olpOfferPrice').text.strip())
        #comp_cond.append(row.find_element_by_class_name('olpConditionColumn').find_element_by_class_name('olpCondition').text.strip())
        #fba_div = row.find_element_by_class_name('olpDeliveryColumn').find_element_by_class_name('olpBadgeContainer').find_element_by_class_name('olpBadge')
        #fba.append(fba_div.find_element_by_tag_name('a').text.strip())
        #comp_btag_text.append(row.find_element_by_class_name('olpSellerColumn').find_element_by_tag_name('b').text.strip())    
        comp_div = row.find_element_by_class_name('olpSellerColumn').find_elements_by_tag_name('a')[0].get_attribute('href')
        
        #comp_adiv = row.find_element_by_class_name('olpSellerColumn').find_elements_by_tag_name('a')[0].text.strip()
        #comp_atag.append(comp_div)
        #comp_atag_text.append(comp_adiv)
        #seller_params = dict(parse.parse_qsl(parse.urlsplit(comp_div).query))
        #seller_array.append(seller_params['seller'])
        competitors_record.append(comp_div)

    #competitors_info = (comp_price,comp_cond,fba,comp_btag_text,comp_atag_text,comp_atag,seller_array)
    #competitors_record.append(competitors_info)
    
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
        
        
seller_records = []        
def seller_info(competitors_record):
    seller_product_asin =[]
    market_id = []
    me_id = []
    count = 0
    for links in competitors_record:
        driver.get(links)
        product_link = driver.find_element_by_id('products-link').find_element_by_tag_name('a').click()
        current_url = driver.current_url
        url = dict(parse.parse_qsl(parse.urlsplit(current_url).query))
        market_id.append(url['marketplaceID'])
        me_id.append(url['me'])
        product_list = driver.find_element_by_class_name('s-main-slot').find_elements_by_class_name('s-result-item')
        
        for value in product_list:
            
            seller_product_asin.append(value.get_attribute('data-asin'))
        
        seller_result = (current_url,market_id,me_id,seller_product_asin)
        count += 1
        seller_records.append(seller_result)
        print(count)
seller_info(competitors_record)

condition = True
while condition:
    try:
        pagination = driver.find_element_by_class_name('a-pagination')
        next_page = pagination.find_elements_by_tag_name('a')[-1].click()
        seller_info(competitors_record)
    except AttributeError:
        next_page = ''
    except:
        condition = False
        
        
with open ('seller_result.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Current URL',
                     'Market_id',
                     'Seller_me_id',
                     'Seller_product_asin',
                     ])
    writer.writerows(seller_records)
