import spacy

NER = spacy.load("en_core_web_sm")

def get_keywords(headline):
    keywords = [word.text  for word in NER(headline).ents]
    return keywords

"""
Confirm if we can use spacy or can we only use probabilistic models
"""
