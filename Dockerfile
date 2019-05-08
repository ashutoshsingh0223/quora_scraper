FROM python:3.6-slim

WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app



RUN apt-get update && apt-get install -yq

RUN apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

RUN  apt-get update -y && \
     apt-get upgrade -y && \
     apt-get dist-upgrade -y && \
     apt-get -y autoremove && \
     apt-get clean
RUN apt-get install -y p7zip \
    zip \
    unzip \
    gnupg2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

#RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz" -O /tmp 
#geckodriver.tgz && tar zxf /tmp/geckodriver.tgz -C /usr/bin/ && rm /tmp/geckodriver.tgz

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# create symlinks to chromedriver and geckodriver (to the PATH)
#RUN ln -s /usr/bin/geckodriver /usr/bin/chromium-browser && chmod 777 /usr/bin/geckodriver && chmod 777 /usr/bin/
#chromium-browser

RUN ln -s /usr/bin/chromium-browser && chmod 777 /usr/bin/chromium-browser


# Make port 80 available to the world outside this container
EXPOSE 3000
EXPOSE 4444

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "questions_scraper.py"]
CMD ["python", "scrape_related_questions.py"]
CMD ["python", "scrape_answers.py"]
