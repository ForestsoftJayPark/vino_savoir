import os
import asyncio
import streamlit as st
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

os.environ["OPENAI_API_KEY"] = ""

st.subheader("💬 AI Chatbot")

# 1) 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = ''
if "agent" not in st.session_state:
    client = MultiServerMCPClient(
        {
            "online_class" :{
                "command" : "python",
                "args" : ["./mcp_server/online_class_server.py"],
                "transport" : "stdio"
            },
            "wine_price_search" :{
                "command" : "python",
                "args" : ["./mcp_server/wine_price_server.py"],
                "transport" : "stdio"
            },
            "rag-mcp": {
                "command": "uvx",
                "args": [
                    "mcp-hybrid-search",
                    "./mcp_server"
                ],
                "env": {
                    "OPENAI_API_KEY": ""
                },
                "transport" : "stdio"
            },
            "youtube_search" :{
                "command" : "python",
                "args" : ["./mcp_server/youtube_server.py"],
                "transport" : "stdio"
            }
        }
    )
    tools = asyncio.run(client.get_tools())
    print(tools)

    st.session_state.agent = create_react_agent(ChatOpenAI(model="gpt-4.1"), tools)


def generate_response(prompt: str) -> str:
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(
            st.session_state.agent.ainvoke({"messages": prompt})
        )
        print(response['messages'])
        return response['messages'][-1].content
    finally:
        loop.close()


# 2) 사용자 입력
prompt = st.chat_input("무엇을 도와드릴까요?")

# 3) 들어온 값 저장
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = generate_response(prompt)
    st.session_state.messages.append({"role": "ai", "content": response})

# 4) 출력
for message in st.session_state.messages :
    with st.chat_message(message["role"]):
        st.markdown(message["content"])