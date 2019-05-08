# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from bs4 import BeautifulSoup
import urllib2
import time
import numpy as np
import re
import csv
import pandas as pd
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import xlsxwriter


f = False
def fetch(driver,dictionary,count,file_name):
	import json
	global f

	answer_link_list = dictionary["answer_link_list"]
	answer_upvote_list = []
	workbook = xlsxwriter.Workbook("./"+str(file_name)+"/"+str(file_name)+"till_"+str(count)+"_answers.xlsx")
	worksheet = workbook.add_worksheet()
	row = 0
	col = 0
	worksheet.write(row,col,dictionary["ques"])
	print("number of answers for question number "+str(count)+":"+str(len(answer_link_list)))
	count_a = 0
	if len(answer_link_list) > 0:
		for answer in answer_link_list:
			url = base_url+answer
			wait_time = np.random.uniform(0.00,1.00,size = None)
			time.sleep(wait_time)
			# response = opener.open(url)
			driver.get(url)
			response = driver.page_source
			soup_3= BeautifulSoup(response)
			real_answers_list = soup_3.find_all("div",class_="ui_qtext_expanded")
			if len(real_answers_list) == 0:
				real_answers_list = soup_3.find_all("div",class_="ExpandedAnswer ExpandedQText")
			# print(str("return--> ")+str(len(real_answers_list)))
			answer_text = "no answer"
			try:
				for a in real_answers_list:
					answer_text = str(a.find_all("span",class_="ui_qtext_rendered_qtext")[0].text)
				print(answer_text)
			except Exception as e:
				print(e)

			if answer_text == "no answer":
				pass
				# answer_upvote_list.append({"answer":answer_text,"upvote":float(10)})
			else:
				answer_upvote_list.append({"answer":answer_text})
			count_a = count_a + 1
			print("answer number "+str(count_a))
			# SORT LIST OF ALL THE ANSWERS FOR EACH QUESTION ACCORDING TO THEIR UPVOTES
		if len(answer_upvote_list) > 0:
			sorted_list = list(reversed(answer_upvote_list))
			# most_upvoted_answer = sorted_list[0]["answer"]
		else:
			sorted_list = [{"answer":"no_answer"}]
		col  = 0
		# row_to_write = [dictionary["ques"]]
		worksheet.write(row,col,dictionary["ques"])
		for dict_ in sorted_list:
			col = col + 1
			# row_to_write.append(dict_["answer"])
			worksheet.write(row,col,dict_["answer"])
		# writer.writerow(row_to_write)
	else:
		worksheet.write(row,1,"no answer")
	workbook.close()



# "./cardiology/Cardiology",

# list_ = ["./cardiology/Cardiologists","./cardiology/Cardiovascular-Fitness","./cardiology/Cardiovascular-Diseases"]
list_ = ["Mutual-Funds"]
for file_name in list_:
	df = pd.read_excel(str(file_name)+"_links.xlsx",sheet_name="Sheet1")
	questions = df.loc[:,0].values.tolist()[10]
	links = df.loc[:,1].values.tolist()[10]
	question_link ={}
	driver =  webdriver.Firefox()


	base_url = "https://www.quora.com"
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	question_with_anwer_links_and_views = []
	count = 10
	driver.get(base_url)
	time.sleep()
	for key,link in zip(questions,links):
		print("\n\n\n\n\n\n\n\n\n\n\n")
		print(":::::::::::::::::::::::::::::::::::::::::::::::::::"+str(count))
		link = link
		if "unanswered" in link:
			continue
		driver.get(base_url+"/"+link)
		html_source = driver.page_source
		data = html_source.encode('utf-8')
		soup = BeautifulSoup(data)


		related_questions_tag = soup.find("div",class_="question_related list side_bar")
		related_questions_links = related_questions_tag.find_all("a",class_='question_link')
		related_questions_links = list(map(lambda x: x["href"],related_questions_links))
		related_questions = related_questions_tag.find_all("span",class_='ui_qtext_rendered_qtext')
		related_questions = list(map(lambda x: x.text,related_questions))

		arr = [related_questions,related_questions_links]
		df = pd.DataFrame(arr)
		df = df.transpose()
		df.to_excel("mf/"+str(key.replace("/"," "))+".xlsx")
		count += 1


	


