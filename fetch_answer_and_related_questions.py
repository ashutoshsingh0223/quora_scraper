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
import time
import numpy as np
import re
import csv
import json
import pandas as pd
import numpy as np
import sys
import xlsxwriter


class fetch_answer_and_related_questions:
	def __init__(self,topic_dir,topic):
		self.f = False
		self.direct_related_marker = False
		self.topic_dir = topic_dir
		self.topic = topic
		self.base_url = "https://www.quora.com"


	def fetch(self,driver,dictionary_list,count):
		f = self.f
		file_name = "quora_answers"
		if self.direct_related_marker is True:
			workbook = xlsxwriter.Workbook(str(file_name+"till_"+str(count)+"_answers_related.xlsx"))
		else:
			workbook = xlsxwriter.Workbook(str(file_name+"till_"+str(count)+"_answers.xlsx"))
		worksheet = workbook.add_worksheet()
		row = 0
		for dictionary in dictionary_list:
			col = 0
			answer_link_list = dictionary["answer_link_list"]
			answer_upvote_list = []
			worksheet.write(row,col,dictionary["ques"])
			print("number of answers for question number for topic "+str(self.topic)+" "+str(count)+":"+str(len(answer_link_list)))
			count_a = 0
			if len(answer_link_list) > 0:
				for answer in answer_link_list:
					url = self.base_url+answer
					wait_time = np.random.uniform(0.00,1.00,size = None)
					time.sleep(wait_time)
					driver.get(url)
					response = driver.page_source
					soup_3= BeautifulSoup(response)
					real_answers_list = soup_3.find_all("div",class_="ui_qtext_expanded")
					if len(real_answers_list) == 0:
						real_answers_list = soup_3.find_all("div",class_="ExpandedAnswer ExpandedQText")
					answer_text = "no answer"
					try:
						for a in real_answers_list:
							answer_text = str(a.find_all("span",class_="ui_qtext_rendered_qtext")[0].text)
						# print(answer_text)
					except Exception as e:
						print(e)

					if answer_text == "no answer":
						pass
					else:
						answer_upvote_list.append({"answer":answer_text})
					count_a = count_a + 1
					#print("answer number "+str(count_a))
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
			row += 1
		workbook.close()

	def fetch_related_questions_and_links(self):
		augment_related_questions = []
		augment_related_links = []
		df = pd.read_excel(str(self.topic_dir)+"/"+str(self.topic)+"_links.xlsx",sheet_name="Sheet1")
		questions = df.loc[:,0].values.tolist()
		links = df.loc[:,1].values.tolist()
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-gpu')
		driver = webdriver.Chrome(chrome_options=chrome_options)

		print("topic: "+str(self.topic))
		print("number_of_questions: "+str(len(questions)))
		i = 0
		for key,link in zip(questions,links):
			if str(link).startswith("/"):
				driver.get(self.base_url+""+link)
			else:
				driver.get(self.base_url+"/"+link)
			html_source = driver.page_source
			data = html_source
			soup = BeautifulSoup(data)
			try:
				related_questions_tag = soup.find("div",class_="question_related list side_bar")
				related_questions_links = related_questions_tag.find_all("a",class_='question_link')
				related_questions_links = list(map(lambda x: x["href"],related_questions_links))
				related_questions = related_questions_tag.find_all("span",class_='ui_qtext_rendered_qtext')
				related_questions = list(map(lambda x: x.text,related_questions))
				augment_related_questions.extend(related_questions)
				augment_related_links.extend(related_questions_links)
			except Exception as e:
				print("EXCEPTION E+++ start")
				print(self.topic)
				print(i)
				print(key)
				print(link)
				print(str(e)+" -- "+'Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
				print("EXCEPTION E+++ end")
			i +=1
		print("number of related questions: "+str(len(augment_related_questions)))
		array_for_both_questions_and_links = []
		array_for_both_questions_and_links.append(augment_related_questions)
		array_for_both_questions_and_links.append(augment_related_links)
		df_questions_with_corresponding_links = pd.DataFrame(array_for_both_questions_and_links)
		df_questions_with_corresponding_links = df_questions_with_corresponding_links.transpose()
		df_questions_with_corresponding_links.to_csv(str(self.topic_dir)+"/"+str(self.topic)+"_links_related.csv",index=False)
		driver.close()
		return 

	def run(self):
		df = pd.read_csv("quora_unanswered.csv")
		questions = df["question"].values.tolist()
		links = df["link"].values.tolist()

		# df_related = pd.read_csv(str(self.topic_dir)+"/"+str(self.topic)+"_links_related.csv")
		# augment_related_questions = df_related.loc[:,0].values.tolist()
		# augment_related_links = df_related.loc[:,1].values.tolist()

		# question_link is dictionary you can get from q_mf or other files
		question_link ={}
		
		
		len_for_differentiating_between_direct_and_related = len(questions)+10
		# questions.extend(augment_related_questions)
		# links.extend(augment_related_links)

		questions_with_answer_links_and_views = []
		count = 0
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-gpu')
		driver = webdriver.Chrome(chrome_options=chrome_options)
# 		driver = webdriver.Firefox()
		for key,link in zip(questions,links):
			if link == "no answer":
				continue
			if link.startswith("/unanswered"):
				link = link.split("/unanswered")[1]
			count+=1
			print("\n\n\n\n\n\n\n\n\n\n\n")
			print(":::::::::::::::::::::::::::::::::::::::::::::::::::"+str(count))
			if self.direct_related_marker is False:
				if count > len_for_differentiating_between_direct_and_related:
					if len(questions_with_answer_links_and_views) > 0:
								self.fetch(driver,questions_with_answer_links_and_views,count)
								questions_with_answer_links_and_views = []
								self.direct_related_marker = True
			try:
				print(self.base_url+""+link)
				if str(link).startswith("/"):
					driver.get(self.base_url+""+link)
				else:
					driver.get(self.base_url+"/"+link)
				html_source = driver.page_source
				data = html_source
				soup = BeautifulSoup(data)

				any_answer = True
				try:
					answer_count = int(re.findall(r"\d+",str(soup.find("div",class_="answer_count")))[0])
					print("answer count: "+str(answer_count))
				except IndexError:
					answer_count = 0
					total_views = 0.0
					most_upvoted_answer = "no answer"
					any_answer = False
				if any_answer == True:
					answer_list = []
					view_list = []
					upvote_list = []
					count_answer_fetch_complete = 0
					while len(answer_list) < answer_count:
						try:
							old_len = len(answer_list)
							driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
							wait_time_4 = np.random.uniform(1.00,3.00,size = None)
							time.sleep(wait_time_4)
							html_source_scroll = driver.page_source
							data_scroll = html_source_scroll
							soup_scroll = BeautifulSoup(data_scroll)
							answer_list = soup_scroll.find_all("a",class_='answer_permalink')
							answer_list = list(map(lambda x: x["href"],answer_list))
							view_list = soup_scroll.find_all("span",class_="meta_num")
							new_len = len(answer_list)
							if old_len == new_len:
								count_answer_fetch_complete = count_answer_fetch_complete + 1
							if count_answer_fetch_complete > 3:
								break
						except Exception as e:
							print(e)
							continue
					total_views = 0.0
					for view in view_list:
						# print(view.text)
						try:
							if "k" in (view.text).lower():
								no_of_views = float(re.findall(r'(\d+.?\d*)',view.text)[0]) * 1000
							elif "m" in (view.text).lower():
								no_of_views = float(re.findall(r'(\d+.?\d*)',view.text)[0]) * 1000000
							elif "b" in (view.text).lower():
								no_of_views = float(re.findall(r'(\d+.?\d*)',view.text)[0]) * 1000000000
							else:
								no_of_views = float(view.text)
						except Exception as e:
							print(e)
							continue
						total_views = total_views + no_of_views
					try:
						questions_with_answer_links_and_views.append({"ques":key,"answer_link_list":answer_list})
						if len(questions_with_answer_links_and_views) > 10:
							self.fetch(driver,questions_with_answer_links_and_views,count)
							questions_with_answer_links_and_views = []
					except Exception as e:
						print(e)
						if len(questions_with_answer_links_and_views) > 0:
							self.fetch(driver,questions_with_answer_links_and_views,count)
							questions_with_answer_links_and_views = []

				
				else:
					questions_with_answer_links_and_views.append({"ques":key,"answer_link_list":[]})
					if len(questions_with_answer_links_and_views) > 10:
							self.fetch(driver,questions_with_answer_links_and_views,count)
							questions_with_answer_links_and_views = []
				print("questions done so far: "+str(count))	
			except Exception as e:
				print(str(e)+ " failed at question number count: "+str(count))
				print(str(e)+" -- "+'Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
				continue
		driver.close()



	# f = open("diabetes_answers1.csv","a")
	


