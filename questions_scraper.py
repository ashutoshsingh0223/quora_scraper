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
from selenium.webdriver.common.keys import Keys
import sys
from bs4 import BeautifulSoup
import numpy as np
import json
import unittest, time, re
import xlsxwriter
import pandas as pd
import numpy as np
import sys
import os
import fetch_answer_and_related_questions

class Sel:
	def __init__(self):
		# self.driver = webdriver.Firefox()
		self.base_url = "https://www.quora.com"
		self.verificationErrors = []
		self.accept_next_alert = True

	def run_scraper(self):
		topics = ["Personal-Finance","Loans","Personal-Loans-1","Bank-Loans","Financial-Services-1",
			"Finance","Finance-in-India", "Finance-and-Investments", "Investing-in-the-Stock-Market-1",
			"Hedge-Funds", "Investing", "Mutual-Fund-Investment-Strategies", "The-Economics-of-Investing","Stock-Markets-2",
			"Investment-Advice","Mutual-Fund-Investment-Advice-1","Stocks-finance"]
		try:
			for topic in topics:
				# driver = webdriver.Firefox()
				chrome_options = webdriver.ChromeOptions()
				chrome_options.add_argument('--no-sandbox')
				chrome_options.add_argument('--headless')
				chrome_options.add_argument('--disable-gpu')
				driver = webdriver.Chrome(chrome_options=chrome_options)
				print("_+_+_+_+_+++++topic+++++_+_+_+_+_")
				print(topic)
				data_path = "data"
				topic_dir = os.path.join(os.getcwd(),"data",str(topic))
				if os.path.isdir(topic_dir) is False:
					os.mkdir(topic_dir)
				row_count = 0
				delay = 3
				driver.get(self.base_url + "/topic/"+str(topic)+"/all_questions")
				c = 1
				dictionary_of_question_link = {}
				count_no_increment = 0
				links_of_questions = []
				question_dictionary_list =[]
				index_of_last_link = 0
				for_index_of_last_link = False
				old_len = 0
				new_len = 0
				list_of_questions = []
				while True:
					old_len = len(dictionary_of_question_link)
					wait_time = np.random.uniform(1.00,3.00,size = None)
					count_equal = 0
					time.sleep(wait_time)
					if for_index_of_last_link is True:
						index_of_last_link = len(links_of_questions) - 1
					for i in range(1,10		):
						driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
						element = driver.find_element_by_tag_name("body").send_keys(Keys.END)
						driver.find_elements_by_class_name("question_link")
						wait_time_2 = np.random.uniform(.50,1.0,size = None)
						time.sleep(wait_time_2)
						html_source = driver.page_source
						data = html_source
						soup = BeautifulSoup(data)
						# questions = soup.find_all("span",class_="question_text")
						links_of_questions = soup.find_all("a",class_="question_link")
					print("questions so far: "+ str(len(links_of_questions)))
					for question_index in range(index_of_last_link,len(links_of_questions)):
						try:
							question = links_of_questions[question_index].text
							list_of_questions.append(question)
							link = str(links_of_questions[question_index]['href'])
							dictionary_of_question_link.update({question:link})
						except Exception as e:
							print(e)
							continue

					print("\n")          
					new_len = len(dictionary_of_question_link)
					print("old_length: " +str(old_len))
					print("new_length: " +str(new_len))


					if old_len == new_len:
						count_no_increment = count_no_increment + 1
						old_len = new_len
					else:
						count_no_increment = 1
					if count_no_increment >=4:
						list_of_total_questions = list(dictionary_of_question_link.keys())
						list_of_total_question_links = list(dictionary_of_question_link.values())
						array_for_both_questions_and_links = []
						array_for_both_questions_and_links.append(list_of_total_questions)
						array_for_both_questions_and_links.append(list_of_total_question_links)
						df_questions_with_corresponding_links = pd.DataFrame(array_for_both_questions_and_links)
						df_questions_with_corresponding_links = df_questions_with_corresponding_links.transpose()
						df_questions_with_corresponding_links.to_csv(str(topic_dir)+"/"+str(topic)+"_links.csv",index=False)
						print("________________________changing topic________________________________")
						wait_time = np.random.uniform(4.00,5.00,size = None)
						break
				driver.close()
		except Exception as e:
			print(str(e)+" -- "+'Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

if __name__ == "__main__":
	s = Sel()
	s.run_scraper()
