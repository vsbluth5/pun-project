import requests
import random
from similar_text import similar_text
from datamuse import datamuse
api = datamuse.Datamuse()

def make_pun (word):
    word_hom = api.words(rel_hom=word)
    hom_words = []
    for item in word_hom: 
        hom_words.append(item["word"])

    word_syn = api.words(rel_syn=word)
    syn_words = []
    for item in word_syn: 
        syn_words.append(item["word"])

    word_spell = api.words(sp=word)
    spell_words = []
    for item in word_spell: 
        spell_words.append(item["word"])

    return{"word": word, "synonyms": syn_words, "spellings": spell_words, "homonyms": hom_words}
word = input("What word would you like to pun off of?")

print(make_pun(word))