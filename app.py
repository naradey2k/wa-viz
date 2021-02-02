import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import re
import sys

from modules import data_extraction as extraction
from modules import data_analysis as analysis
from datetime import datetime
from io import StringIO

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

	data = []
	l_messages = []
	author, text = None, None

	for message in messages:
		if starts_with_date(message): 
			if len(l_messages) > 0:
				data.append((date, author, ' '.join(l_messages))) 
				
			l_messages.clear() 
			date, author, message = get_data(message) 
			l_messages.append(message)
		else:
			l_messages.append(message)
		
	return data

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

		data = create_data(raw_data, date_format)

		dates, authors, texts = map(list, *zip(data))

		with st.beta_expander('Распределение сообщений'):
			st.header('По дням')
			st.plotly_chart(analysis.plot_dates(dates))

			st.header('По автору')
			st.plotly_chart(analysis.most_active_authors(authors))

			st.header('Динамика сообщений')
			st.plotly_chart(analysis.plot_line_dates(dates))
			
		with st.beta_expander('Облако слов'):			
			word_cloud = analysis.create_wc(texts, form)

			fig, ax = plt.subplots()

			ax.imshow(word_cloud, interpolation='bilinear')
			ax.axis("off")

			st.pyplot(fig)

if __name__ == '__main__':
	main()
