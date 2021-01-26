import streamlit as st
import pandas as pd
import re

def starts_with_dt(line):
    pattern = '^([0-2][0-9]|(3)[0-1])(\.)(((0)[0-9])|((1)[0-2]))(\.)(\d{2}|\d{4})(,)? ([0-9])|([0-9]):([0-9][0-9])$'
    result = re.match(pattern, line)

    if result:
        return True

    return False

def get_data(line):
    split_line = line.split(' - ') 
    
    dt = split_line[0]
    date, time = dt.split(', ')  

    message = ' '.join(split_line[1:]) 
    
    split_message = message.split(': ') 
    author = split_message[0] 
    text = ' '.join(split_message[1:]) 
    
    return date, time, author, text

@st.cache
def load_data(file_name, date_format):
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()    

    return create_df(lines, date_format)

@st.cache
def create_df(data, date_format):
    date_formats = {'dd.mm.yyyy': '%d.%m.%Y, %H:%M',
                    'dd.mm.yy': '%d.%m.%y, %H:%M'}

    data = []
    messages = []

    date, time, author = None, None

    for line in data:
        line = line.strip() 
        if starts_with_dt(line): 
            if len(messages) > 0:
                data.append([date, time, author, ' '.join(messages)]) 

            messages.clear() 
            date, time, author, text = get_data(line) 
            messages.append(text)

        else:
            messages.append(line) 
    
    df = pd.DataFrame(data, columns=['Date', 'Time', 'Author', 'Text'])
    df["Date"] = pd.to_datetime(df["Date"], format=date_formats[date_format])    
    
    return df
