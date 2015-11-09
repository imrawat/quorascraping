#Required..
#BeautifulSoup
#Selenium driver and chrome driver. 

import socks
import socket
import time
import urllib2
import feedparser
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

browser = webdriver.Chrome()

url = "https://www.quora.com/"
browser.get(url)

time.sleep(1)

#div.pagedlist_item div class tag for visible and loaded logs items.
elem = browser.find_elements_by_css_selector("div.pagedlist_item")

#TODO Change for checking when page ends instead of static 20pagedowns.
no_of_pagedowns = 5
count = 0
while no_of_pagedowns:
    i = len(elem)
    count = count+1
    print count
    
    elem[i-1].send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    no_of_pagedowns-=1

content = browser.page_source
soup = BeautifulSoup(content)

# raw_data = str(soup.find_all('div', class_="pagedlist_item"))
# soup = BeautifulSoup(raw_data);
quesTag = soup.find_all('div', class_="pagedlist_item")

fieldnames = ['first_name', 'last_name']

with open('feedques.csv', 'w') as csvfile:
	fieldnames = ['QuestionText', 'QuestionLink', 'Asker', 'Edits', 'QuestionsAsked', 'Answers', 'Facebook', 'Sex', 'Location', 'Banned', 'Followers', 'Following']
	writer = csv.DictWriter(csvfile,	)
	writer.writeheader()

for divTag1 in quesTag:
	quesTextTag = divTag1.find_all('div', class_="QuestionText")
	for divTag2 in quesTextTag:
		questionLink = divTag2.a.attrs['href']
		questionLink = "https://www.quora.com"+questionLink
		questionText = divTag2.text
		# print questionLink
		with open('feedques.csv', 'a') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			# print questionLink
			writer.writerow({fieldnames[0]: questionText.encode('utf-8'), fieldnames[1]: questionLink.encode('utf-8')})





