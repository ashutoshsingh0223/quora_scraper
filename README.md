# quora_scraper
Scrape quora questions with related questions and answers.


# Adding topics from quora  
Add topics of your choice(Eg. Bollywood) to the following files.Add exact topics from quora.  
```
questions_scraper.py
scrape_related_questions.py
scrape_answers.py
```


# Steps to run with docker
You can use docker to run the scraper  
Clone the repo  
[Install docker](https://docs.docker.com/install/)  
[Install docker-compose](https://docs.docker.com/compose/install/)
```
cd quora_scraper
docker-compose build
docker-compose up -d
```

#View logs(logs are currently here and there a little working on it)  
`docker-compose logs --tail=10` (--tail == number of lines)


#Log-in to the container  
`docker exec -it <container name> bash` 

# Running locally
If you want to run it on Mac to see how selenium works with the browser. You can use any one of `Chromedriver` or `Geckodriver(Mozilla)`.
Just comment the following lines in these two files. `questions_scraper.py` in function `run_scraper`.
`fetch_answer_and_related_questions.py` in functions `fetch_related_questions_and_links` and `run`

Comment out these lines.
```
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)
```

Add any one of the following lines depending upon what driver you have.
For `Chromediver` add  
`driver = webdriver.Chrome()`  
For `geckodriver(Mozilla)`  
`driver = webdriver.Firefox()`

Then run these commands sequentially
```
python3 questions_scraper.py
python3 scrape_related_questions.py
python3 scrape_answers.py
```

Don't forget to add the executables of these webdrivers to path.(using docker is much easier)

