import streamlit as st
import app.db.db_interactions as interactions
import app.view.views as views

st.set_page_config(page_title='О приложении', layout='wide')
st.write('# Добро пожаловать!')
st.write('Это небольшое приложение для управления базой данных некоторого предприятия. Сделано '
         'в рамках курса ПБЗ (5 семестр). Лабораторная номер 2, вариант 19. Для навигации используйте меню слева')
interactions.check_issued_editions()
st.snow()