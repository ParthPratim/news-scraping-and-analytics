import json
import os

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
    def __init__(self, start_time : int, end_time : int):
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
    def download_content(self):
        url = self.url_prefix + '40000' + self.url_suffix
        response = requests.get(url , headers = self.headers)
        return response.content

    def response_parse(self):
        with open("result.txt", 'r') as f: 
            soup = BeautifulSoup(f, 'html.parser')
            span_tags = soup.find_all('span', style="font-family:arial ;font-size:12;color: #006699")     
            single_page = {
                "url" : "",
                "parse-time" : "",
                "headline" : "",
            }
            for info in span_tags[0]:
                for x in info : 
                    print(x)


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
    tt = TimesNowScrapper(0,0)
    tt.response_parse()
