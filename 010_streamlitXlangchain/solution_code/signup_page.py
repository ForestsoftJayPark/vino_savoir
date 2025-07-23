import streamlit as st

st.subheader("📝 회원가입")
new_user = st.text_input("ID", key="signup_user")
new_pass = st.text_input("Password", type="password", key="signup_password")

st.button("회원가입", key="signup_button")