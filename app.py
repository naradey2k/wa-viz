import streamlit as st

def main():
	st.title('WhatsApp Chat Analysis')
	st.markdown('Приложение создано для анализа русского WhatsApp чата')

	st.sidebar.subheader('Как экспортировать чат?')	
	st.sidebar.text('1) Зайдите в чат-группу')
	st.sidebar.text('2) Настройки ⋮ -> Еще -> Экспорт чата')
	st.sidebar.text('3) Выберите "Без Файлов"')





	uploaded_file = st.file_uploader('Загрузите файл', type='txt')

if __name__ == '__main__':
	main()
