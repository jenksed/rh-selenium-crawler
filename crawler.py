# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import requests
import re
import pandas
import time
from config import *

city="DETROIT"
state="MI"
country="US"
results=1
num_pages=1
base=BASE_URL

url=base+city.lower()+"-"+state.lower()+"/"

#num_pages=results//21

def main():
    getTrucks()

def getTrucks():

    trucks = []
    for page in range(0,num_pages+1,1):
        total_pages=num_pages+1
        print("Processing "+str(page)+" of "+str(total_pages)+" pages.")

        driver = generateBrowser()
        driver.implicitly_wait(30)
        driver.get(url+str(page))
        scroll(driver, 5)

        # Once scroll returns bs4 parsers the page_source
        soup_a = BeautifulSoup(driver.page_source, features="html.parser")

        # Them we close the driver as soup_a is storing the page source
        driver.close()

        l=[]
        all = soup_a.find_all("div",{"class":"_53x7N"})
        for item in all:
            d={}
            d["Truck Name"]=item.find("h4").text
            d["Link to Page"]=constant_base+item.find('a')['href']

            div_style = item.find('div')['s
            #style = cssutils.parseStyle(div_style)
            #imgUrl = style['background-image']
            #imgUrl = imgUrl.replace('url(', '').replace(')', '')
            d["Image URL"]=div_style

            l.append(d)
        time.sleep(1)

        print(l)

def generateBrowser():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")
    return webdriver.Chrome(options=chrome_options)

def extractUrl(rawData):
    raw_data = str(rawData)
    regex = r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'
    x_url = re.search(regex,rawData)
    if x_url is not None:
        return str(x_url.group())
    else:
        return str(x_url)

def processImage(file_url):
    firstpos=file_url.rfind("/")
    lastpos=len(file_url)
    filename=file_url[firstpos+1:lastpos]

    img_file = requests.get(file_url, allow_redirects=True)
    open('images/'+city+filename, 'wb').write(img_file.content)
    return filename

def scroll(driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height

main()
