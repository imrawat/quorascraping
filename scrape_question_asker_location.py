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

startRow = 1437 #Start row no -1. NOTE: rows with Header starts at 1 in csv.
noOfMetaDataRowsToAdd = 170
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
				rightColdTag = soup.find_all('div', class_="EditableList ProfileAboutList")
				
				for div in rightColdTag:
					
					questionText = row[0]
					questionLink = row[1]
					noOfEdits = row[3]
					noOfQues = row[4]
					noOfAnswers = row[5]
					noOfFollowers = row[10]
					noOfFollowing = row[11]
					
					facebookLink = row[6]
					linkedInLink = row[12]
					twitterLink = row[13]

					topicTag = soup.find_all('div', class_="TopicPreviewItemSentence");
					location =  ' '
					# print "check"
					for div2 in topicTag:
						# print '200 OK'
						print div2.text
						location = div2.text
						break

					rowValues = [questionText, questionLink, userlink, noOfEdits, noOfQues, noOfAnswers, facebookLink,' ' , location.encode('utf-8') , ' ',noOfFollowers, noOfFollowing, twitterLink, linkedInLink]

					tempwriter.writerow(rowValues)
			else:
				tempwriter.writerow(row)

		else:
			tempwriter.writerow(row)

shutil.move(tempfile.name, "womenquestions.csv")


				

