
import sys
import os
import pandas as pd
import numpy as np
import time
import psycopg2

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

#브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True) 

path = "chromedriver.exe"
driver = webdriver.Chrome(path, options=chrome_options)

conn = psycopg2.connect(host='localhost',dbname='Hotel',user='postgres',password='1234',port='5432')
cur = conn.cursor()


keywords = ['서울', '제주', '부산', '인천', '강릉', '속초', '여수', '경주', '대구', '대전', '울산', '평창', '전주', '군산', '양양']
id = 1
# 데이터 수집할 키워드 입력
for keyword in keywords:

    #네이버 호텔 웹사이트 열기
    driver.get('https://hotels.naver.com/')
    driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div[2]/button[2]').click()
    driver.find_element(By.CLASS_NAME, 'SearchBox_btn_location__49Pk3').click()
    
    element = driver.find_element(By.CLASS_NAME,"Autocomplete_txt__nb6wT")
    element.send_keys(keyword)  # keyword는 위에서 입력한 키워드
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR,"a.SearchResults_anchor__luLYP").click()
    time.sleep(1)

    driver.find_element(By.CLASS_NAME,"SearchBox_search__tLThj").click()

    # hotel_name_raw = driver.find_elements(By.CLASS_NAME,"Detail_title__40_dz")
    # for hotel_name in hotel_name_raw:
    #     i = hotel_name.text
    #     name_list.append(i)
    # print(name_list)

    address = []
    names = []
    prices = []
    rates = []
   
    for i in range(0,5):
        time.sleep(2)
        items = driver.find_elements(By.CLASS_NAME,"SearchList_HotelItem__aj2GM")

        for item in items:
            address.append(keyword)
            names.append(item.find_element(By.CLASS_NAME,"Detail_title__40_dz").text)
            prices.append(item.find_element(By.CLASS_NAME,"Price_show_price__iQpms").text)
            rates.append(item.find_element(By.CLASS_NAME,"Detail_score__UxnqZ").text)
            # name = item.find_element(By.CLASS_NAME,"Detail_title__40_dz").text
            # price = item.find_element(By.CLASS_NAME,"Price_show_price__iQpms").text
            # rate = item.find_element(By.CLASS_NAME,"Detail_score__UxnqZ").text
        driver.find_element(By.CLASS_NAME,"Pagination_next__OzkO7").click()

    

    for i in range(0,len(names)):
        print(names[i], prices[i], rates[i], address[i])

    for i in range(0,len(names)):
        cur.execute("INSERT INTO accomodation(accomodation_id,accomodation_name,accomodation_lowprice,accomodation_rate,accomodation_address) VALUES (%s, %s, %s, %s, %s);",(id,names[i],prices[i],rates[i],address[i]))
        conn.commit()
        id = id + 1

   
    # driver.close()
    # time.sleep(1)

driver.close()

# 호텔목록 SearchList_HotelItem__aj2GM
# 호텔이름 Detail_title__40_dz 
# 호텔평점 Detail_score__UxnqZ
# 호텔최저가 Price_show_price__iQpms
