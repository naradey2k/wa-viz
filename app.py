import streamlit as st
import numpy as np
import pandas as pd
import wordcloud
import collections
import nltk
import re

nltk.download('stopwords')
nltk.download('punkt')

from PIL import Image
from string import punctuation
from matplotlib import pyplot as plt
from plotly import express as px
from catboost.text_processing import Tokenizer
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
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
    author = split_message[0] 
    text = ' '.join(split_message[1:]) 
	
    return dt, author, text

@st.cache
def read_file(file_name, date_format):    
#     date_formats = {'dd.mm.yyyy': '%d.%m.%Y, %H:%M', 'dd.mm.yy': '%d.%m.%y, %H:%M'}
#     result = []
#     message_data = [] 
#     dt, author = None, None 

#     with open(file_name, 'r', encoding='utf=8') as file:
#         messages = file.readlines()

#     for line in messages:
#         line = line.strip()
# 		if 'Данное сообщение удалено' in line or '<Без медиафайлов>' in message:
# 			messages.remove(message)
			
#         if starts_with_date(line): 
#             if len(message_data) > 0: 
#                 result.append([dt, author, ' '.join(message_data)]) 

#         message_data.clear() 
#         dt, author, message = get_data(line) 
#         message_data.append(message) 

#     else:
#         message_data.append(line)
        
#     return result
	date_formats = {'dd.mm.yyyy': '%d.%m.%Y, %H:%M', 'dd.mm.yy': '%d.%m.%y, %H:%M'}
	result = []
	message_data = [] 
	dt, author = None, None 
	with open(file_name, 'r', encoding='utf=8') as file:
		messages = file.readlines()

    for line in messages:
    	line = line.strip()
        if 'Данное сообщение удалено' in line or '<Без медиафайлов>' in message:
            messages.remove(message)
	
        if starts_with_date(line): 
            if len(message_data) > 0: 
                result.append([dt, author, ' '.join(message_data)]) 
        
           	message_data.clear() 
            dt, author, message = get_data(line) 
            message_data.append(message) 

        else:
            message_data.append(line)
    
	return result

@st.cache
def tokenize_texts(texts):
    simple_tokenizer = Tokenizer(lowercasing=True,
                                 separator_type='BySense',
                                 token_types=['Word', 'Number'])

    return [simple_tokenizer.tokenize(text) for text in texts]

@st.cache
def preprocess(texts):
    stop_words = stopwords.words('russian')    
    lemmatizer = MorphAnalyzer()
    texts_copy = []    

    for text in tokenize_texts(texts):
        text_copy = []

        for token in text:
            if token not in stop_words:
                token = lemmatizer.normal_forms(token)[0]
                text_copy.append(token)

        texts_copy.append(' '.join(text_copy))
            
    return texts_copy
    

@st.cache
def compute(file):
    dts, authors, messages = map(list, zip(*file))

    author_counts = collections.Counter(authors)    
    counts, names = zip(*sorted(zip(author_counts.values(), author_counts.keys()), reverse=True))

    lens = [[len(msg) for msg, author in zip(messages, authors) if author == name] for name in names]
    totals = [sum(l) for l in lens]
    lens = [int(sum(l)/len(l)) for l in lens]

    words = collections.Counter(preprocess(messages))
    sorted_words = sorted(zip(words.values(), words.keys()), reverse=True)

    return dts, authors, messages, author_counts, counts, names, lens, totals, words, sorted_words

def hist(x, x_label, y_label="Число сообщений", **kwargs):
    df = pd.DataFrame(x, columns=[x_label])
    h = px.histogram(df, x=x_label, **kwargs)
    h.layout.yaxis.title.text = y_label
    return h

@st.cache
def word_cloud(words):
	return wordcloud.WordCloud(background_color="white", max_font_size=80, random_state=0, width=800, height=480,
                               mask=np.array(Image.open("images/brain.jpg")), color_func=color_func,
                               font_path="images/RobotoCondensed-Regular.ttf") \
        .generate_from_frequencies({k: v for k, v in words.items() if v > 35})


def bar(x, y, x_label, y_label="Число сообщений", limit=999, **kwargs):
    df = pd.DataFrame(sorted(zip(y, x), reverse=True)[:limit], columns=[y_label, x_label])
    return px.bar(df, x=x_label, y=y_label)

def color_func(word=None, font_size=None,
               position=None, orientation=None,
               font_path=None, random_state=None):
    return f"hsl({random_state.randint(230, 270)}, {110}%, {60}%)"


@st.cache
def gen_wc(words):
    return wordcloud.WordCloud(background_color="white", max_font_size=80, random_state=0, width=800, height=480,
                               mask=np.array(Image.open("images/brain.jpg")), color_func=color_func,
                               font_path="images/RobotoCondensed-Regular.ttf") \
        .generate_from_frequencies({k: v for k, v in words.items() if v > 35})

def main():
    st.title("WhatsApp Chat Analysis")
    
    date_format = st.sidebar.selectbox('Выберите формат даты и времени:', ('dd.mm.yyyy', 'dd.mm.yy'), key='0')
    
    file = read_file("example.txt", 'dd.mm.yyyy')    
    filename = st.file_uploader("Загрузить файл", type="txt")

    if filename:
        file = read_file(filename, date_format)
        
    dts, authors, messages, author_counts, counts, names, lens, totals, words, worded = compute(file)

    with st.beta_expander("Распределение сообщений"):
        st.subheader("По дням")
        st.plotly_chart(hist(dts, "День"))
	
        st.subheader("По длине")
        st.plotly_chart(hist(lens, "Длина"))
        st.subheader("По автору")
        st.plotly_chart(hist([names.index(author) for author in authors], "Авторы (пока анонимно)"))

    with st.beta_expander("Популярные слова"):
        st.subheader("Распределение")
        st.plotly_chart(bar(words.keys(), words.values(), "Слово", limit=250))

        st.subheader("Wordcloud")
        wc = gen_wc(words)
        fig, ax = plt.subplots()
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        st.subheader("Таблица")
        rows, cols = 25, 3
        columns = []
        for i in range(cols):
            columns.append(pd.DataFrame(worded[i:rows*cols:cols], columns=[f"Частота", f"Слово"]))
        table = pd.concat(columns, axis=1)
        st.table(table.assign(hack='').set_index('hack'))

    st.header("Лидерборды")

    def leaderboard(counts, name):
        with st.beta_expander(name):
            st.plotly_chart(bar(names, counts, "Автор", name, limit=35))
            leaderboard = pd.DataFrame(sorted(zip(counts, names), reverse=True),
                                       columns=[name, "Автор"])
            leaderboard.index += 1
            leaderboard.index.name = "Место"
            st.table(leaderboard.head(100))

    leaderboard(counts, "Число сообщений")
    leaderboard(lens, "Средняя длина")
    leaderboard(totals, "Число символов")


if __name__ == '__main__':
    main()
