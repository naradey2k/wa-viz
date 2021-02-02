import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import sys

from modules import data_extraction as extraction
from modules import data_analysis as analysis

@st.cache
def read_data(file_name):
	with open(file_name, 'r', encoding='utf-8') as file:	
		messages = file.readlines()

	return messages

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
		raw_data = read_data(uploaded_file)

		data = extraction.create_data(raw_data, date_format)

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
