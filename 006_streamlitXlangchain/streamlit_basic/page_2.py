# page_2.py
import streamlit as st

name = st.text_input("이름", key= "name")
st.title(name)