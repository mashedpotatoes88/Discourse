#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type:text/html")
print()
import nltk
from nltk.corpus import wordnet


def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

word = "js"
synonyms = get_synonyms(word)
print("Synonyms of '{}': {}".format(word, synonyms))
