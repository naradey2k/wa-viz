import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
import collections
import nltk
import re

from pymorphy2 import MorphAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime
from io import StringIO

nltk.download('stopwords')
nltk.download('punkt')

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
def plot_line_df(data, x_label, y_label, **kwargs):
# 	fdist = collections.Counter(dates)
	
	df = pd.DataFrame(data=data, columns=x_label)
	
	plot = px.line(df, layers={'x':x_label, 'y':y_label}, **kwargs)

	return plot

@st.cache
def plot_df(data, x_label, y_label, **kwargs):
	# 	fdist = collections.Counter(dates)	
	
	df = pd.DataFrame(data=data, columns=x_label)

	plot = px.histogram(df, layers={'x':x_label, 'y':y_label}, **kwargs)

	return plot

def starts_with_date(message):
    pattern = '^([0-2][0-9]|(3)[0-1])(\.)(((0)[0-9])|((1)[0-2]))(\.)(\d{2}|\d{4})(,)$'
    result = re.match(pattern, message)
	
    if result:
        return True

    return False

def get_data(message):
	splitted = message.split(' - ') 
    	
	dt = splitted[0]	
	date = dt.split(', ')[0]  
	
	message = ' '.join(splitted[1:]) 
	splitted_message = message.split(': ')
	
	author = splitted_message[0] 
	
	text = ' '.join(splitted_message[1:])
        
	return date, author, text

@st.cache
def read_data(file_name):
	with open(file_name, 'r') as file:	
		messages = file.readlines()

	return messages

@st.cache
def create_data(messages, date_format):	
	date_formats = {'dd.mm.yyyy': '%d.%m.%Y',
					'dd.mm.yy': '%d.%m.%y'}

	dates = []
	texts = []
	authors = []
	
	for message in messages:
		if starts_with_date(message):				
			date, author, text = get_data(message) 
			
			date = datetime.strptime(date, date_formats[date_format])
			
			dates.append(date)
			texts.append(text)
			authors.append(author)
			
		else:
			_, _, text = get_data(message)
			
			texts.append(text)
		
	return dates, authors, texts

def main():
	st.title('WhatsApp Chat Analysis')
	st.markdown('Приложение создано для анализа русского WhatsApp чата')

	st.sidebar.subheader('Как экспортировать чат?')	
	st.sidebar.text('1) Зайдите в чат-группу')
	st.sidebar.text('2) Настройки ⋮ -> Еще -> Экспорт чата')
	st.sidebar.text('3) Выберите "Без Файлов"')

	st.sidebar.subheader('Выберите формат даты:')
	date_format = st.sidebar.selectbox(label='', options=('dd.mm.yyyy', 'dd.mm.yy'), key=0)

	st.sidebar.subheader('Выберите форму облака слов:')
	form = st.sidebar.selectbox(label='', options=('Сердце', 'Мозг', 'Штурмовик'), key=0)

	uploaded_file = st.file_uploader(label='', type='txt')
	
	if uploaded_file is not None:    
		bytes_data = uploaded_file.read()
		
		stringio = StringIO(bytes_data.decode('utf-8'))
		
		raw_data = stringio.read()		
		
# 		raw_data = read_data(string_data)

		dates, authors, texts = create_data(raw_data, date_format)

		with st.beta_expander('Распределение сообщений'):
			st.header('По дням')
			st.plotly_chart(plot_df(dates, 'Дата', 'Кол-во сообщений'))

			st.header('По автору')
			st.plotly_chart(plot_df(authors, 'Автор', 'Кол-во сообщений'))

			st.header('Динамика сообщений')
			st.plotly_chart(plot_line_df(dates, 'Дата', 'Кол-во сообщений'))
			
		with st.beta_expander('Облако слов'):			
			word_cloud = create_wc(texts, form)

			fig, ax = plt.subplots()

			ax.imshow(word_cloud, interpolation='bilinear')
			ax.axis("off")

			st.pyplot(fig)

if __name__ == '__main__':
	main()
