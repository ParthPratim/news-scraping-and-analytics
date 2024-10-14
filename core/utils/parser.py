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
