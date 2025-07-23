import streamlit as st

# Define the pages
index_page = st.Page("index_page.py", title="Vino", icon="🍷")
login_page = st.Page("login_page.py", title="로그인", icon="❄️")
signup_page = st.Page("signup_page.py", title="회원가입", icon="🎉")
chat_page = st.Page("chat_page.py", title="AI 채팅", icon="💬")

# Set up navigation
pg = st.navigation([index_page, login_page, signup_page, chat_page])

# Run the selected page
pg.run()