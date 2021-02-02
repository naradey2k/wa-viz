import plotly.graph_objects as go
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import collections
import nltk
import re

nltk.download('stopwords')
nltk.download('punkt')

from plotly import express as px
from pymorphy2 import MorphAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


@st.cache
def tokenize(text):
	return [token for token in word_tokenize(text, language='russian')]

@st.cache
def get_words(texts):	
	words = []
	lemmatizer = MorphAnalyzer()
	stopwords = stopwords.words('russian')

	for text in texts:
		for token in tokenize(text):
			if token not in stopwords:
				token = lemmatizer.normal_forms(token)[0]
				words.append(token)

	return words

@st.cache
def create_wc(texts, form):
	forms = {'Heart': 'forms/heart.png',
			 'Brain': 'forms/brain.png',
			 'Stormtrooper': 'forms/stormtrooper.png'}

    words = get_words(texts)

    fdict = collections.Counter(words)
    
    return wordcloud.WordCloud(background_color="white", max_font_size=80, random_state=0, width=800, height=480,
                               mask=np.array(Image.open(forms[form])), color_func=color_func,
                               font_path="fonts/Oswald-Regular.ttf") \
        .generate_from_frequencies({key: value for key, value in fdict.items() if value >= 20})


@st.cache
def plot_line_dates(dates):
    fdist = collections.Counter(dates)

    plot = go.Figure(data=go.Scatter(x=fdist.keys(), y=fdist.values()))

    return plot

@st.cache
def plot_dates(dates):
	fdist = collections.Counter(dates)	

    df = pd.DataFrame(data=fdist.values(), columns=['Дата'], index=fdist.keys())

    plot = px.histogram(df, x='Дата')
    plot.layout.yaxis.label = 'Кол-во сообщений'

    return plot

@st.cache
def plot_authors(authors):
    df = pd.DataFrame(data=authors, columns=['Автор'])

    plot = px.histogram(df, x='Автор')
    plot.layout.yaxis.label = 'Кол-во сообщений'

    return plot 
