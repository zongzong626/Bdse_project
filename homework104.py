#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep
from bs4 import BeautifulSoup
import requests
import bs4
import json
import os

options =webdriver.ChromeOptions()
#options.add_argument("--headLess")
options.add_argument("--start-maximized")
options.add_argument("--incognito")               
options.add_argument("--disable-popup-blocking ")
driver = webdriver.Chrome(options = options)
listData=[]

def visit():
    driver.get('https://www.104.com.tw/jobs/main/')

     
def search():
    box=driver.find_element(By.CSS_SELECTOR, "input#ikeyword")
    box.send_keys("統計")
    sleep(1)
    area=driver.find_element(By.CSS_SELECTOR, "span#icity")
    area.click()
    sleep(1)
    driver.find_element(By.CSS_SELECTOR, "input[value='6001001000']").click()
    sleep(1)
    driver.find_element(By.CSS_SELECTOR, "input[value='6001002000']").click()
    sleep(1)
    driver.find_element(By.CSS_SELECTOR,  "button.category-picker-btn-primary").click()
    sleep(1)
    btnInput = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.js-formCheck")
    btnInput.click()
    sleep(5)
    fullTimeJob=driver.find_element(By.CSS_SELECTOR, "ul.b-nav-tabs.job-type li[data-value='1']")
    fullTimeJob.click()
    sleep(5)

def scroll():
    innerHeightOfWindow = 0
    totalOffset = 0

    while totalOffset <= innerHeightOfWindow:
        # 每次移動高度
        totalOffset += 90
        
        # 捲動的 js code 加上smooth讓他滾動的比較平順
        js_scroll = '''(
            function (){{
                window.scrollTo({{
                    top:{}, 
                    behavior: 'smooth' 
                }});
            }})();'''.format(totalOffset)
        
        # 執行 js code
        driver.execute_script(js_scroll)
        
        #sleep(1)
        
        innerHeightOfWindow = driver.execute_script('return window.document.documentElement.scrollHeight;')
        
        #sleep(1)
        
        #print("innerHeightOfWindow: {}, totalOffset: {}".format(innerHeightOfWindow, totalOffset))
        
        #手動取得下一頁
        if innerHeightOfWindow - totalOffset < 200:
            sleep(5)
            buttons = driver.find_elements(By.CSS_SELECTOR, "button.b-btn--link.js-more-page")
            try:
                buttons[-1].click()
            except:
                continue
         
        if innerHeightOfWindow - totalOffset <= 100:
            sleep(5)
        
    
def parse():
       
        htmlFile=driver.page_source
        ObjSoup=BeautifulSoup(htmlFile,'lxml')
        jobs = ObjSoup.find_all('article',class_='js-job-item') 
        
        
        for job in jobs:
            
            #職缺名稱
            job_title = job.find('a',class_="js-job-link").text
            jobLink = job.find('a').get('href')
           
            #公司名稱 
            company_title =job.get('data-cust-name')
            companyLink = job.select('ul>li>a')[0].get('href')

            
            #工作地點與學經歷
            area = job.find('ul', class_='job-list-intro').find('li').text
            
                    
            listData.append({
            "職缺名稱": job_title,
            "職缺連結": jobLink,
            "公司名稱": company_title,
            "公司連結": companyLink,
            "工作地點": area
             }) 
            
            print(listData)
            
            
        
        
def saveJson():   
    fp = open("job.json","w",encoding="utf-8") #中間的w代表寫入
    fp.write( json.dumps(listData, ensure_ascii=False)) #ensure_ascii是避免中文字亂碼
    fp.close()
    
def close():
    driver.quit()        
        
        
    
if __name__ == '__main__':
    visit()
    search() 
    scroll()
    parse()
    saveJson()
    close()
    





