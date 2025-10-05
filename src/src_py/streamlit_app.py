import streamlit as st

st.title("streamlit_app.py!")

name = st.text_input('名前を入力してください')
st.write("Hello,", name or "world")
