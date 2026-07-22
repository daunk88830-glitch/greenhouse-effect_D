import streamlit as st

st.set_page_config(
    page_title="온실효과와 지구온난화",
    page_icon="🌍",
    layout="wide"
)

home = st.Page("pages/0_홈.py", title="홈", icon="🏠", default=True)

p1 = st.Page("pages/1_개념_이해.py", title="개념 이해", icon="📖")
p2 = st.Page("pages/2_시뮬레이션.py", title="시뮬레이션 체험", icon="🎛️")
p3 = st.Page("pages/3_데이터_비교.py", title="데이터 비교", icon="📊")

p4 = st.Page("pages/4_열수지_가상실험.py", title="열수지 가상실험", icon="🧪")
p5 = st.Page("pages/5_열수지_계산하기.py", title="열수지 계산하기", icon="🧮")
p6 = st.Page("pages/6_기사_조사_요약.py", title="기사 조사 요약", icon="📰")
p7 = st.Page("pages/7_탐구주제_구상.py", title="탐구주제 구상", icon="💡")

pg = st.navigation({
    "": [home],
    "1차시": [p1, p2, p3],
    "2차시": [p4, p5, p6, p7],
})

pg.run()
