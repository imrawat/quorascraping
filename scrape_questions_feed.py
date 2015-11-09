#Required..
#BeautifulSoup
#Selenium driver and chrome driver. 

import socks
import socket
import time
import urllib2
import feedparser
import re
import shutil
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from tempfile import NamedTemporaryFile

APPEND_TO_OLD_FEED_QUES = True

file = open('questionsHTML.txt','r')

content = file.read()

soup = BeautifulSoup(content)

quesTag = soup.find_all('div', class_="pagedlist_item")

fieldnames = ['first_name', 'last_name']

tempfile = NamedTemporaryFile(delete=False)

if APPEND_TO_OLD_FEED_QUES:
	with open('feedques.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter = ',')
		tempwriter = csv.writer(tempfile, delimiter=',')

		for row in reader:
			print row
			tempwriter.writerow(row)

		for divTag1 in quesTag:
			quesTextTag = divTag1.find_all('div', class_="QuestionText")
			for divTag2 in quesTextTag:
				questionLink = divTag2.a.attrs['href']
				questionLink = "https://www.quora.com"+questionLink
				questionText = divTag2.text

				rowValues = [questionText.encode('utf-8'), questionLink.encode('utf-8'), ' ', ' ', ' ', ' ', ' ',' ' , ' ' , ' ',' ', ' ']
				
				tempwriter.writerow(rowValues)

	shutil.move(tempfile.name, "feedques.csv")

else:


	with open('feedques.csv', 'w') as csvfile:
		fieldnames = ['QuestionText', 'QuestionLink', 'Asker', 'Edits', 'QuestionsAsked', 'Answers', 'Facebook', 'Sex', 'Location', 'Banned', 'Followers', 'Following']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
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



