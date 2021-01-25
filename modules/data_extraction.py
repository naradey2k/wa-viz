import streamlit as st 
import pandas as pd 
import re

from datetime import datetime

def starts_with_date(input):
    pattern = '^([0-2][0-9]|(3)[0-1])(\.)(((0)[0-9])|((1)[0-2]))(\.)(\d{2}|\d{4})(,)? ([0-9])|([0-9]):([0-9][0-9])$'
    result = re.match(pattern, input)

    if result:
        return True

    return False

@st.cache
def get_data(message):
	split_messsage = message.split(' - ')	

	dt = split_messsage[0]
  
	message = ' '.join(split_messsage[1:])
	
  split_message = message.split(': ') 
  
  author = splitMessage[0] 
  text = ' '.join(split_message[1:]) 

  return dt, author, text

@st.cache
def read_data(file_name, date_format):    
    date_formats = {'mm.dd.yyyy': '%m.%d.%Y', 'mm.dd.yy': '%m.%d.%y'}
    result = []
    
    with open(file_name, 'r', encoding='utf=8') as file:
        messages = file.readlines()
    
    for message in messages:
        dt, author, text = get_data(message)
        
        date = datetime.strptime(dt, date_formats[date_format])
        
        if text:
            result.append((date, author, text))
            
    return result

