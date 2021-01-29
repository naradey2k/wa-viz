import streamlit as st 
import pandas as pd 
import re

from datetime import datetime

def starts_with_dt(message):
	pattern = '^([0-2][0-9]|(3)[0-1])(\.)(((0)[0-9])|((1)[0-2]))(\.)(\d{2}|\d{4})(,)? ([0-9])|([0-9]):([0-9][0-9])$'
    result = re.match(pattern, message)

    if result:
        return True

    return False


def get_data(message):
	splitted = message.split(' - ')

	dt = splitted[0]
	date = dt.split(', ')[0]

	author, text = splitted[1].split(': ')[0], splitted[1].split(': ')[1]

	return date, author, text

@st.cache
def read_file(file_name):
	with open(file_name, 'r', encoding='utf-8') as file:
		messages = file.readlines()

	return messages

@st.cache
def create_df(messages, date_format):
	date_formats = {'dd.mm.yyyy': '%d.%m.%Y',
					'dd.mm.yy': '%d.%m.%y'}

	data = []
	l_messages = []

	author, text = None, None

	for message in messages:
		if starts_with_dt(message):
			if len(l_messages) > 0:
				data.append([date, author, ' '.join(l_messages)])

		l_messages.clear()
		date, author, text = get_data(message)
		l_messages.append(text)

		else:
			l_messages.append(text)

	df = pd.DataFrame(data, columns=['Date', 'Author', 'Text'])	
	df['Date'] = pd.to_datetime(df['Date'], format=date_formats[date_format])

	return df
