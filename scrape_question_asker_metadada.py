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

startRow = 6 #Start row no -1. NOTE: rows with Header starts at 1 in csv.
no_of_downs = 40
no_of_pagedowns = no_of_downs
noOfMetaDataRowsToAdd = 100 # No of rows to add meta data to after startrow

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


browser = webdriver.Chrome() #opens chrome browser to run selenium

def find_between(str, start, end):
	return re.search('%s(.*)%s' % (start, end), str).group(1)

count = 0

fieldnames = ['QuestionText', 'QuestionLink', 'Asker', 'Edits', 'QuestionsAsked', 'Answers', 'Facebook', 'Sex', 'Location', 'Banned', 'Followers', 'Following']
tempfile = NamedTemporaryFile(delete=False)
with open('why_women_questions.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter = ',')
	tempwriter = csv.writer(tempfile, delimiter=',')
	# tempwriter.writerow(fieldnames)

	for row in reader:
		if(startRow < reader.line_num and count<noOfMetaDataRowsToAdd):
 			questionLink = row[1]
 			questionText = row[0]
			count = count+1
			questionLog = row[1]+'/log'
			# questionLog = "https://www.quora.com/How-exactly-should-I-proceed-with-my-startup-idea/log"
			print '-----------BEGIN NEW-----------'
			print reader.line_num
			print questionLog

			# ----------------------------------------
			# Goto Questionlog page for scraping question asker
			print '----------------------------------------'
			print 'Goto Questionlog page for scraping question asker'
			browser.get(questionLog)

			time.sleep(1)

			elem = browser.find_elements_by_css_selector("div.pagedlist_item")

			pagedowncount = 0
			no_of_pagedowns = no_of_downs
			try:
				while no_of_pagedowns:
					i = len(elem)
					pagedowncount = pagedowncount + 1
					print pagedowncount
					elem[i-1].send_keys(Keys.PAGE_DOWN)
					time.sleep(1)
					no_of_pagedowns-=1
			except Exception, e:
				print "error occured 1"
				shutil.move(tempfile.name, "why_women_questions.csv")
				raise e
			

			# while no_of_pageups:
			# 	elem[i-1].send_keys(Keys.PAGE_UP)
			# 	time.sleep(0.25)
			# 	no_of_pageups-=1

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
			print last_div.getText()
			print last_div
			if(last_div.getText() != "Question added by Anonymous." and last_div.getText()!="Question added by Quora User." and last_div.getText()[:17]=="Question added by"):
				links = last_div.findAll('a')
				print last_div

				try:
					link  = links[0]
				except Exception, e:
					print "error occured 2"
					shutil.move(tempfile.name, "why_women_questions.csv")
					raise e

				userlink = "https://www.quora.com"+link.attrs['href']
				print userlink

				# ----------------------------------------
				#Goto user page for getting user metadata
				print '----------------------------------------'
				print 'Goto user page for getting user metadata'


				try:
					userlink = userlink.encode('utf-8')
					html_doc = urllib2.urlopen(userlink)
					soup = BeautifulSoup(html_doc.read())
				
				except Exception, e:
					print "Error occured 3"
					shutil.move(tempfile.name, "why_women_questions.csv")
					raise e
				# print html_doc.read()
				print "###############################################################################"
				# print soup

				leftColTag = soup.find_all('div', class_="layout_3col_left")
				
				for div in leftColTag:
					# "FeedsAll ActivityQuestions14Answers14Posts0Followers 169Following 131Edits267"
					noOfQues = find_between(div.text, "Questions", "Answers")
					noOfAnswers = find_between(div.text, "Answers", "Posts")
					noOfPosts = find_between(div.text, "Posts", "Followers")
					noOfFollowers = find_between(div.text, "Followers ", "Following")
					noOfFollowing = find_between(div.text, "Following ", "Edits")
					noOfEdits = find_between(div.text, "Edits", "")
					print noOfQues
					print noOfAnswers
					print noOfPosts
					print noOfFollowing
					print noOfFollowers
					print noOfEdits

					# with open('womenquestions.csv', 'a') as csvfile:
# fieldnames = ['QuestionText', 'QuestionLink', 'Asker', 'Edits', 'QuestionsAsked', 'Answers', 'Facebook', 'Sex', 'Location', 'Banned', 'Followers', 'Following']
					# 	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

					rowValues = [questionText, questionLink, userlink, noOfEdits, noOfQues, noOfAnswers, " ",' ' , ' ' , ' ',noOfFollowers, noOfFollowing]
					tempwriter.writerow(rowValues)
					# tempwriter.writerow({fieldnames[0]: questionText, fieldnames[1]: questionLink})
					# tempwriter.writerow({fieldnames[2]: userlink})
					# tempwriter.writerow({fieldnames[3]: noOfEdits})
					# tempwriter.writerow({fieldnames[4]: noOfQues})
					# tempwriter.writerow({fieldnames[5]: noOfAnswers})
					# tempwriter.writerow({fieldnames[10]: noOfFollowers})
					# tempwriter.writerow({fieldnames[11]: noOfFollowing})
			elif(last_div.getText() != "Question added by Anonymous." and last_div.getText()!="Question added by Quora User." and last_div.getText()[:17]!="Question added by"):
				print "Need to scroll more than 40"
				rowValues = [questionText, questionLink, 'NEED TO SCROLL MORE', '0', '0', '0', '0','0' , '0' , '0','0', "0"]
				tempwriter.writerow(rowValues)
			else: 
				print "Anonymous or Quora User"
				rowValues = [questionText, questionLink, 'Anonymous', '0', '0', '0', '0','0' , '0' , '0','0', "0"]
				tempwriter.writerow(rowValues)

		else:
			tempwriter.writerow(row)

shutil.move(tempfile.name, "why_women_questions.csv")
				

