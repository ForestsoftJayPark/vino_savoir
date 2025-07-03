import streamlit as st


st.subheader("💬 AI Chatbot")

# 1) 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = ''

def generate_response():
    pass

# 2) 사용자 입력
prompt = st.chat_input("무엇을 도와드릴까요?")

# 3) 들어온 값 저장
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = generate_response(prompt, st.session_state.history)
    st.session_state.messages.append({"role": "ai", "content": response})

# 4) 출력
for message in st.session_state.messages :
    with st.chat_message(message["role"]):
        st.markdown(message["content"])