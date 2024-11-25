class StorageModel:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def save_to_mongo(self, mongo_collection):
        # Convert to dictionary for MongoDB
        data = {k: v for k, v in self.__dict__.items() if k != 'self'}
        mongo_collection.insert_one(data)       

class ScrappedNews(StorageModel):
    
    def __init__(self,
                 url = None,
                 parse_time = None, 
                 published_date = None,
                 headline = None,
                 scrapped_source = None
                 ):
        StorageModel.__init__(**locals())
