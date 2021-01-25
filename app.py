import streamlit as st
import numpy as np
import pandas as pd
import wordcloud

from PIL import Image
from string import punctuation
from matplotlib import pyplot as plt
from plotly import express as px

from modules import data_extraction as data_ext
from odules import message_analysis as analysis

def hist(x, x_label, y_label="Число сообщений", **kwargs):
    df = pd.DataFrame(x, columns=[x_label])
    h = px.histogram(df, x=x_label, **kwargs)
    h.layout.yaxis.title.text = y_label
    return h


def bar(x, y, x_label, y_label="Число сообщений", limit=999, **kwargs):
    df = pd.DataFrame(sorted(zip(y, x), reverse=True)[:limit], columns=[y_label, x_label])
    return px.bar(df, x=x_label, y=y_label)

def color_func():
    return f"hsl({random_state.randint(230, 270)}, {110}%, {60}%)"


@st.cache
def gen_wc(words):
    return wordcloud.WordCloud(background_color="white", max_font_size=80, random_state=0, width=800, height=480,
                               mask=np.array(Image.open("images/brain.jpg")), color_func=color_func,
                               font_path="images/RobotoCondensed-Regular.ttf") \
        .generate_from_frequencies({k: v for k, v in words.items() if v > 35})

def main():
    st.title("WhatsApp Chat Analysis")
    
    date_format = st.sidebar.selectbox('Выберите формат даты и времени:',
                                 ('mm.dd.yyyy', 'mm.dd.yy'), key='0')
    
    file = data_ext.read_file(open("example.txt"))    
    filename = st.file_uploader("Загрузить файл", type="txt")

    if filename:
        file = data_ext.read_file(filename)
        
    dts, authors, messages, author_counts, counts, names, lens, totals, words, worded = data_ext.compute(file)

    with st.beta_expander("Распределение сообщений"):
        st.subheader("По дням")
        st.plotly_chart(hist(dts, "День"))
        st.subheader("По часам")
        hours = [dt.hour for dt in dts]
        st.plotly_chart(hist(hours, "Час"))

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
