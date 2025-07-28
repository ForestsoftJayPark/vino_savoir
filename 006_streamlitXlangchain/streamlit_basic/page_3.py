# page_3.py
import streamlit as st

# 1) 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2) 사용자 입력
prompt = st.chat_input("무엇을 도와드릴까요?")

# 3) 데이터 저장
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "ai", "content":"저는 AI 입니다."})

# 4) 세션에 저장된 메시지 출력
for message in st.session_state.messages :
    with st.chat_message(message["role"]):
        st.markdown(message["content"])