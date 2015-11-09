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
import itertools
import shutil
from tempfile import NamedTemporaryFile

startRow = 1238 #Start row no -1. NOTE: rows with Header starts at 1 in csv.
noOfMetaDataRowsToAdd = 376
from bs4 import BeautifulSoup

def find_between(str, start, end):
	return re.search('%s(.*)%s' % (start, end), str).group(1)

count = 0

fieldnames = ['QuestionText', 'QuestionLink', 'Asker', 'Edits', 'QuestionsAsked', 'Answers', 'Facebook', 'Sex', 'Location', 'Banned', 'Followers', 'Following','Twitter','LinkedIn']
tempfile = NamedTemporaryFile(delete=False)
with open('womenquestions.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter = ',')
	tempwriter = csv.writer(tempfile, delimiter=',')

	for row in reader:
		print reader.line_num
		if(startRow < reader.line_num and count<noOfMetaDataRowsToAdd):
			
 			questionAsker = row[2]
 			
 			# print questionAsker
 			count = count+1
			if(questionAsker!='Anonymous' and questionAsker!='NEED TO SCROLL MORE'):
				
				print questionAsker
				
				try:
					userlink = questionAsker.encode('utf-8')
					html_doc = urllib2.urlopen(userlink)
					soup = BeautifulSoup(html_doc.read())
				
				except Exception, e:
					print "Error occured 3"
					shutil.move(tempfile.name, "womenquestions.csv")
					raise e

				#Check Social media links
				leftColTag = soup.find_all('div', class_="Profile ActionBar")
				
				for div in leftColTag:
					
					questionText = row[0]
					questionLink = row[1]
					noOfEdits = row[3]
					noOfQues = row[4]
					noOfAnswers = row[5]
					noOfFollowers = row[10]
					noOfFollowing = row[11]

					hasFacebook = False
					hasTwitter = False
					hasLinkedIn = False
					facebookLink = ' '
					linkedInLink = ' '
					twitterLink = ' '

					if('Facebook' in div.text):
						hasFacebook = True
					if('LinkedIn' in div.text):
						hasLinkedIn = True
					if('Twitter' in div.text):
						hasTwitter = True

					actionTag = div.find_all('div', class_='action_item')
					for div2 in actionTag:
						# print div2.text
						if(div2.text == 'Facebook'):
							facebookLink = div2.a.attrs['href']
							print 'Link '+facebookLink
						if(div2.text == 'LinkedIn'):
							linkedInLink = div2.a.attrs['href']
							print 'Link '+linkedInLink
						if(div2.text == 'Twitter'):
							twitterLink = div2.a.attrs['href']
							print 'Link '+twitterLink
						if(div2.text == 'Anonymous'):
							continue

					rowValues = [questionText, questionLink, userlink, noOfEdits, noOfQues, noOfAnswers, facebookLink,' ' , ' ' , ' ',noOfFollowers, noOfFollowing, twitterLink, linkedInLink]

					tempwriter.writerow(rowValues)
			else:
				tempwriter.writerow(row)

		else:
			tempwriter.writerow(row)

shutil.move(tempfile.name, "womenquestions.csv")


				

