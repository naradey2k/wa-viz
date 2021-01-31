import streamlit as st
import pandas as pd
import sys

from modules import data_extraction as extraction
from modules import data_analysis as analysis

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
# 		try:
		@st.cache(persist=True, allow_output_mutation=True)
		def read_file(file_name, date_format):	
			with open(file_name, 'r', encoding='utf-8') as file:			
				messages = file.readlines()		

			return extraction.create_df(messages, date_format)
		
		try:
			file = uploaded_file.read()
		
			df = read_file(file, date_format)
		
			with st.beta_expander('Самые активные дни'):
				st.pyplot(analysis.most_active_df(df))

			with st.beta_expander(''):
				st.pyplot(analysis.most_active_authors(df))

				authors = pd.DataFrame(df[df['Author'] != None].value_counts().sort_values(by='columns', ascending=False), columns=['Имя', 'Место'])
				authors.index += 1
				authors.index.name = 'Место'	

				st.table(authors)

			with beta_expander('Облако слов'):
				st.pyplot(analysis.create_wc(df, form))
			
		except OSError as exc:
			if exc.errno == 36:
				df = extraction.create_df(file, date_format)

				with st.beta_expander('Самые активные дни'):
					st.pyplot(analysis.most_active_df(df))

				with st.beta_expander(''):
					st.pyplot(analysis.most_active_authors(df))

					authors = pd.DataFrame(df[df['Author'] != None].value_counts().sort_values(by='columns', ascending=False), columns=['Имя', 'Место'])
					authors.index += 1
					authors.index.name = 'Место'	

					st.table(authors)

				with beta_expander('Облако слов'):
					st.pyplot(analysis.create_wc(df, form))

# 		except:
# 			error = sys.exc_info()[0]
# 			st.error('Что-то пошло не так! Выберите другой тип даты! Тип ошибки - '.format(error.__name__))


if __name__ == '__main__':
	main()
