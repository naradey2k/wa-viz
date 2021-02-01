import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import wordcloud
import pymorphy2
import random
import nltk

nltk.download('stopwords')
nltk.download('punkt')

from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
from PIL import Image

@st.cache
def tokenize(text):
	return [word for word in word_tokenize(text, language='russian')]

@st.cache
def get_words(df):
	texts = df['Text'].values
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
def create_wc(df, form):
	forms = {'Heart': 'forms/heart.png',
			 'Brain': 'forms/brain.png',
			 'Stormtrooper': 'forms/stormtrooper.png'}

	df = df[df['Text'] != '<Без медиафайлов>']
	df = df[df['Text'] != 'Данное соощение удалено']
	df = df[df['Text'] != 'Вы удалили данное соощение']

	texts = df['Text'].values

	words = get_words(texts)

	return wordcloud.WordCloud(background_color="white", max_font_size=80, random_state=0, width=800, height=480,
                               mask=np.array(Image.open(forms[form])), color_func=color_func,
                               font_path="fonts/Oswald-Regular.ttf") \
        .generate_from_frequencies({key: val for key, val in words.items() if val >= 20})

def color_func(word=None, font_size=None,
               position=None, orientation=None,
               font_path=None, random_state=None):
	
	return f'hsl({random_state.randint(230, 270)}, {110}%, {60}%)'

def most_active_dt(df):
	fig, ax = plt.subplots()
	
    	ax = df['Date'].value_counts().head(10).plot.barh()
    	ax.set_title('10 самых активных дней')
    	ax.set_xlabel('Кол-во сообщений')
    	ax.set_ylabel('Дата')
	
    	plt.tight_layout()
	
    	return fig

def most_active_authors(df):
	fig, ax = matplotlib.pyplot.subplots()

	ax = df[df['Author'] != None].value_counts().plot.bar()
	ax.set_title('Частые пользователи')
	ax.set_xlabel('Пользователи')
	ax.set_ylabel('Кол-во сообщений')

	matplotlib.pyplot.tight_layout()

	return fig
