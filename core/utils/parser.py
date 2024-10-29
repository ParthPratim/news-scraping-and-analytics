import json
import os
import datetime
import math

import requests
from bs4 import BeautifulSoup

"""
Article Scraping Format
-------------------
The scraper should scrap and store the following metadata for each sample 
scraped for each article
    1. Source               : The news website from which data was scraped
    2. Date_Of_Publish      : When was the news published
    3. DateTime_Of_Scrap    : When was this article scrapped
    4. Headline             : The headline of article
    5. Keywords             : Use core.utils.tagger.KeyWordIdentifier
    6. Depth                : No. of levels of Category/Subcategory which was 
                                scraped
    7. Categories           : Categories and Subcategories this sample is from
"""

class TimesNowScrapper :
    def __init__(self, start_time : datetime.datetime , end_time : datetime.datetime, items_per_page : int = 10):
        self.url_prefix = "https://timesofindia.indiatimes.com/archivelist/starttime-"
        self.url_suffix = ".cms"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Connection': 'keep-alive',
            'Priority': 'u=0, i',
        }
        self.ancient_time = 37062 # 20 June 2001
        self.start_time = (start_time - datetime.datetime(1900,1,1)).days + 2
        self.end_time = (end_time - datetime.datetime(1900,1,1,)).days+2
        self.items_per_page = items_per_page
        print(f"TimesNowParser starting with {self.start_time} to {self.end_time}")
        self.news_list = []

    def download_content(self):
        days = self.start_time
        json_content = []
        single_page = {
            "url" : "",
            "parse_time" : "",
            "publish_date" : "",
            "headline" : "",
        }
        base_url = "https://timesofindia.indiatimes.com"
        while days <= self.end_time:
            url = self.url_prefix + str(days)  + self.url_suffix
            response = requests.get(url , headers = self.headers)
            print(f"Got response as {response.status_code}")
            response.status_code = 201
            soup = BeautifulSoup(response.content, 'html.parser')
            if response.status_code != 200 :
                print("WARNING CAN'T CONNECT TO TIMEWSNOW\n Sending dummy info : Would be later implemented in project")
                with open('./core/utils/result.txt', 'r') as f :
                    soup = BeautifulSoup(f, 'html.parser')
            span_tags = soup.find_all('span', style="font-family:arial ;font-size:12;color: #006699")     
            for info in span_tags:
                links = [(a.get('href'), a.text) for a in info.find_all('a')]
                for url, text in links:
                    curr_page = single_page.copy()
                    url = url if url[:4] == "http" else base_url + url
                    curr_page["url"] = url
                    curr_page["headline"] = text
                    curr_page["parse_time"] = str(datetime.datetime.now(datetime.UTC))
                    publish_date = datetime.datetime(1900,1,1) + datetime.timedelta(days-2)
                    curr_page["publish_date"] = str(publish_date.strftime("%Y-%m-%d"))
                    json_content.append(curr_page)
            print(f"Finished parsing {days}")
            days = days + 1
        print(f"Parser done! with {self.start_time} and {self.end_time}")
        self.news_list = json_content.copy()
        return json_content




class RecursiveParser:

    def __init__(self, config, bs4Obj = None , useFallbackSchema = False, schema_file = None):
        self.config = config
        self.schema_file = schema_file
        self.bs4Obj = bs4Obj
        if useFallbackSchema:
            self.schema = self.config.DEFAULT_SCHEMA
        else:
            self.schema = None

    def GetSchemaFile(self):
        return os.path.join(self.config.SCHEMA_DIRECTORY, self.schema_file)

    def LoadSchema(self):
        with open(self.GetSchemaFile(), 'r') as jschema:
            return json.load(jschema)

    def DoParse(self):
        self.schema = self.LoadSchema()
        # Write logic for parsing the schema and use bs4 for parsing the website
        # using the schema

if __name__ == "__main__" :
    # TESTING
    today = datetime.datetime.now()
    tt = TimesNowScrapper(today,today)
    s = tt.download_content()
    print(s)
