import json
import os

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
        self.url_suffx = ".cms"
        pass


class RecursiveParser:

    def __init__(self, config, bs4Obj = None , schema_file = None):
        self.config = config
        self.schema_file = schema_file
        self.bs4Obj = bs4Obj
        self.schema = self.config.DEFAULT_SCHEMA

    def GetSchemaFile(self):
        return os.path.join(self.config.SCHEMA_DIRECTORY, self.schema_file)

    def LoadSchema(self):
        with open(self.GetSchemaFile(), 'r') as jschema:
            return json.load(jschema)

    def DoParse(self):
        self.schema = self.LoadSchema()
        # Write logic for parsing the schema and use bs4 for parsing the website
        # using the schema
