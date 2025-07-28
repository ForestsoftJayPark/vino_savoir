#page_1.py
import streamlit as st

btn = st.button("안녕!")
if btn:
    st.write("안녕 못해!")
else:
    st.write("안녕!")
