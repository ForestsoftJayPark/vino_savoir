# app.py
import streamlit as st

# # Text 실습
# st.write("Hello world")

# st.title("Streamlit x LangChain")

# st.header("기초 문법")

# st.subheader("Text element")

# import numpy as np
# import pandas as pd

# st.write("write를 활용한 데이터 출력")

# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['a', 'b', 'c']
# )
# st.write(chart_data)
# st.line_chart(chart_data) # st.write(chart_data) 대신 line_chart 사용

"""
----------------------------------------------------------------------
"""

# # Layout 실습
# col1, col2, col3 = st.columns([1,1,1], vertical_alignment="bottom")

# with col1:
# 	st.header("A cat")
# 	st.image("https://static.streamlit.io/examples/cat.jpg")
# with col2:
# 	st.header("A dog")
# 	st.image("https://static.streamlit.io/examples/dog.jpg")
# with col3:
# 	st.header("An owl")
# 	st.image("https://static.streamlit.io/examples/owl.jpg")

"""
----------------------------------------------------------------------
"""

# 페이지 생성
main_page = st.Page("page_1.py", title="Page 1", icon="🎈")
page_2 = st.Page("page_2.py", title="Page 2", icon="❄")
page_3 = st.Page("page_3.py", title="Page 3", icon="🎉")

# 네비게이션 생성
pg = st.navigation([main_page, page_2, page_3])

# Run
pg.run()