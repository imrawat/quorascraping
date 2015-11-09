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


file = open('questionsHTML.txt','r')

content = file.read()

soup = BeautifulSoup(content)

quesTag = soup.find_all('div', class_="pagedlist_item")

fieldnames = ['first_name', 'last_name']

with open('why_women_questions.csv', 'w') as csvfile:
	fieldnames = ['QuestionText', 'QuestionLink', 'Asker', 'Edits', 'QuestionsAsked', 'Answers', 'Facebook', 'Sex', 'Location', 'Banned', 'Followers', 'Following']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

for divTag1 in quesTag:
	quesTextTag1 = divTag1.find_all('div', class_="row board_item_description")

	for divTag2 in quesTextTag1:

		quesTextTag2 = divTag2.find_all('div', class_='inline_editor_content')
		for divTag3 in quesTextTag2:
			questionLink =  divTag3.a.attrs['href']
			questionText = divTag3.a.text
			# print questionText
			# break;
			

			# questionLink = divTag2.a.attrs['href']
			# questionLink = "https://www.quora.com"+questionLink
			with open('why_women_questions.csv', 'a') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				# print questionLink
				writer.writerow({fieldnames[0]: questionText.encode('utf-8'), fieldnames[1]: questionLink.encode('utf-8')})

	# break



