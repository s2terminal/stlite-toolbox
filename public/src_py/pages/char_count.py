import streamlit as st

input_text = st.text_area("テキストを入力してください")
char_count = len(input_text)
st.write(f"文字数: {char_count}")
