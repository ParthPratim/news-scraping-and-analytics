
class NounTaggerModel:

    PRETRAINED_PROBABILISTIC_MOEDEL = "hmm-pos-tagger-model-9-10-24.pkl"

    def __init__(self , model = None):
        if not model:
            self.model = NounTaggerModel.PRETRAINED_PROBABILISTIC_MOEDEL
        else:
            # TODO : Validation checks for model being actually present            
            self.model = model
    
    def predict(self, target):
        # TODO : Use pretrained weights to predict the keywords
        return []

class KeyWordIdentifier:
    
    def __init__(self, target):
        self.target = target
        # TODO : Modify this use custom model initializer
        self.model = NounTaggerModel()
    
    def getKeywords(self):
        # TODO : Use self.model to get tagged keywords
        return []
