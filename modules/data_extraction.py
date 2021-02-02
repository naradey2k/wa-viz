import streamlit as st 
import pandas as pd 

from datetime import datetime

def get_data(message):
	splitted = message.split(' - ')

	dt = splitted[0]
	date = dt.split(', ')[0]

	author, text = splitted[1].split(': ')[0], splitted[1].split(': ')[1]

	return date, author, text

@st.cache
def create_data(messages, date_format):	
	date_formats = {'dd.mm.yyyy': '%d.%m.%Y',
					'dd.mm.yy': '%d.%m.%y'}

	data = []
	author, text = None, None

	for message in messages:	
		date, author, text = get_data(message)		

        date = datetime.strptime(date, date_formats[date_format])

		data.append([date, author, text])

	return data

@st.cache
def read_data(file_name, date_format):
    with open(file_name, 'r', encoding='utf-8') as file:
        messages = file.readlines()

    return messages
