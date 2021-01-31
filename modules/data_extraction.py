import streamlit as st 
import pandas as pd 
import re

from datetime import datetime

def get_data(message):
	splitted = message.split(' - ')

	dt = splitted[0]
	date = dt.split(', ')[0]

	author, text = splitted[1].split(': ')[0], splitted[1].split(': ')[1]

	return date, author, text

@st.cache(persist=True, allow_output_mutation=True)
def create_df(messages, date_format):	
	date_formats = {'dd.mm.yyyy': '%d.%m.%Y',
					'dd.mm.yy': '%d.%m.%y'}

	data = []
	author, text = None, None

	for message in messages:	
		date, author, text = get_data(message)		
		data.append([date, author, text])

	df = pd.DataFrame(data, columns=['Date', 'Author', 'Text'])	
	df['Date'] = pd.to_datetime(df['Date'], format=date_formats[date_format])

	return df

@st.cache(persist=True, allow_output_mutation=True)
def read_file(file_name, date_format):	
	with open(file_name, 'r', encoding='utf-8') as file:			
		messages = file.readlines()		

	return create_df(messages, date_format)
