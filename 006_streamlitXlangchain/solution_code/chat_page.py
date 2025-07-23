import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

os.environ["OPENAI_API_KEY"] = ""

st.subheader("💬 AI Chatbot")

# 1) 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = ''

def route(info):
    # 유튜브 검색
    if "유튜브" in info["topic"]:
        return "유튜브 검색 기능은 향후 구현될 예정입니다"

    # 가격 검색
    elif "가격검색" in info["topic"]:
        return "가격 검색 기능은 향후 구현될 예정입니다"
    
    else : 
        general_chain = (
            PromptTemplate.from_template(
            """
                당신은 와인을 추천해주는 인공지능입니다. 과거 대화 맥락을 참고해 질문에 답변하시오.

                <question>
                {question}
                </question>

                <history>
                {history}
                </history>
            """
            )
            | ChatOpenAI(model="gpt-4o-mini")
            | StrOutputParser()
        )
        return general_chain

def generate_summary(summary, new_lines): 
    summary_chain = (
        PromptTemplate.from_template(
            """
            제공된 대화를 요약하고, 이전의 요약에 추가하여 새로운 요약을 반환합니다.
            <예시>
            현재 요약: 인간이 인공지능에 대해 무엇을 생각하는지 AI에게 물어봅니다. AI는 인공지능이 선한 힘이라고 생각합니다.
            새로운 대화 라인:
            인간: 왜 인공지능이 선한 힘이라고 생각하나요?
            AI: 인공지능은 인간이 그들의 잠재력을 완전히 발휘하도록 도울 것입니다.
            새 요약:\n인간이 인공지능에 대해 무엇을 생각하는지 AI에게 물어보고, AI는 인공지능이 인간의 잠재력을 완전히 발휘할 수 있도록 돕기 때문에 선한 힘이라고 생각합니다.
            </예시>
            현재 요약:
            {summary}
            새로운 대화 라인:
            {new_lines}
            새 요약:
            """
        )
        | ChatOpenAI(model="gpt-4o-mini", temperature=0)
        | StrOutputParser()
    )
    return summary_chain.invoke({'summary' : summary, 'new_lines' : new_lines})

def generate_response(query, history) :
    router_prompt = PromptTemplate.from_template(
        """
        주어진 사용자 질문을 `가격검색`, `유튜브` 또는 `기타` 중 하나로 분류하세요. 한 단어로만 응답하세요.

        가격검색: 와인 가격 및 구매 정보 질문
        유튜브: 동영상이나 유튜브 관련 질문
        기타: 추천 관련 질문 또는 위 범주에 해당하지 않는 질문

        <question>
        {question}
        </question>

        Classification:
        """
    )
    router_chain = router_prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0) | StrOutputParser()
    full_chain = (
        {
            'topic' : router_chain,
            "question" : lambda x : x["question"],
            "history" : lambda x : x["history"]
        }
        | RunnableLambda(route)
    )
    print('history : ', history)
    response = full_chain.invoke({"question" : query, "history" : history})
    print(response)
    new_lines = f'인간 : {query} \n AI : {response} '
    new_summary = generate_summary(st.session_state.history, new_lines)
    st.session_state.history = new_summary
    return response

# 2) 사용자 입력
prompt = st.chat_input("무엇을 도와드릴까요?")

# 3) 들어온 값 저장
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("AI가 응답을 생성하는 중입니다..."):
        response = generate_response(prompt, st.session_state.history)
    st.session_state.messages.append({"role": "ai", "content": response})

# 4) 출력
for message in st.session_state.messages :
    with st.chat_message(message["role"]):
        st.markdown(message["content"])