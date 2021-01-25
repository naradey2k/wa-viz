import pandas as pd
import streamlit as st
import collections
import nltk
import re

nltk.download('stopwords')
nltk.download('punkt')

from catboost import Tokenizer
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords


@st.cache
def tokenize_texts(texts):
    simple_tokenizer = Tokenizer(lowercasing=True,
                                 separator_type='BySense',
                                 token_types=['Word', 'Number'])

    return [simple_tokenizer.tokenize(text) for text in texts]

@st.cache
def preprocess(texts):
    stop_words = stopwords.words('russian')    
    lemmatizer = MorphAnalyzer()
    texts_copy = []    

    for text in tokenize_texts(texts):
        text_copy = []

        for token in text:
            if token not in stop_words:
                token = lemmatizer.normal_forms(token)[0]
                text_copy.append(token)

        texts_copy.append(' '.join(text_copy))
            
    return texts_copy
    

@st.cache
def compute_stats(file):
    dts, authors, messages = map(list, zip(*file))

    author_counts = collections.Counter(authors)    
    counts, names = zip(*sorted(zip(author_counts.values(), author_counts.keys()), reverse=True))

    lens = [[len(msg) for msg, author in zip(messages, authors) if author == name] for name in names]
    totals = [sum(l) for l in lens]
    lens = [int(sum(l)/len(l)) for l in lens]

    words = collections.Counter(preprocess(messages))
    sorted_words = sorted(zip(words.values(), words.keys()), reverse=True)

    return dts, authors, messages, author_counts, counts, names, lens, totals, words, sorted_words


