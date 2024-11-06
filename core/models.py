class StorageModel:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class ScrappedNews(StorageModel):
    
    def __init__(self,
                 url = None,
                 parse_time = None, 
                 published_date = None,
                 headline = None,
                 scrapped_source = None
                 ):
        
        
        StorageModel.__init__(**locals())
