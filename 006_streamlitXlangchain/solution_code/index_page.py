import streamlit as st

col1, col2, col3 = st.columns([1, 10, 1])
with col2:
    sub1, sub2, sub3 = st.columns([1, 1, 1])
    with sub2:
        st.image("static/logo.svg", width=150)
    st.markdown(
        "<h1 style='text-align:center;'>인공지능 기반 와인 추천 서비스</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h3 style='text-align:center;'>당신의 특별한 순간을 위한 와인을 찾아드립니다.</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; font-size:18px;'>"
        "와인을 처음 만나는 설렘도, 깊이 있는 여운도 여기에서 시작됩니다."
        "</p>",
        unsafe_allow_html=True,
    )