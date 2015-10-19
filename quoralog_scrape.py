#Required..
#BeautifulSoup
#Selenium driver and chrome driver. 


import time
import urllib2
import feedparser
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

browser = webdriver.Chrome()

# url = "https://www.quora.com/Which-time-is-better-for-studying-night-or-day/log"
url = "https://www.quora.com/What-are-some-amazing-facts-about-Google-or-Microsoft/log"
browser.get(url)

time.sleep(1)

#div.pagedlist_item div class tag for visible and loaded logs items.
elem = browser.find_elements_by_css_selector("div.pagedlist_item")

#TODO Change for checking when page ends instead of static 20pagedowns.
no_of_pagedowns = 40 

while no_of_pagedowns:
    i = len(elem)
    print i
    
    elem[i-1].send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    no_of_pagedowns-=1

content = browser.page_source
soup = BeautifulSoup(content)

raw_data = str(soup.find_all('div', class_="feed_item_activity"))
soup = BeautifulSoup(raw_data);

second_last_div = None
last_div = None
for div in soup:
    second_last_div = last_div
    last_div = div

last_div = second_last_div
print last_div
print last_div.getText()
links = last_div.findAll('a')
link  = links[0]

userlink = "https://www.quora.com",link.attrs['href']

print userlink


