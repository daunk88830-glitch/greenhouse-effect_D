import streamlit as st

st.title("💡 2차시 - ④ 탐구주제 구상하기")
st.caption("학기 말 주제탐구 발표를 위한 아이디어를 자유롭게 구상해보세요.")

st.markdown("""
### 안내
꼭 오늘 다룬 CO2·기온 데이터가 아니어도 괜찮습니다. 평소 관심 있던 사회, 경제, 문화,
스포츠 등 **어떤 분야든 데이터로 탐구해볼 수 있는 주제**라면 좋습니다.
""")

interest_area = st.multiselect(
    "관심 있는 분야를 골라보세요 (여러 개 선택 가능)",
    ["기후·환경", "사회·인구", "경제", "건강·의료", "스포츠", "문화·미디어", "기술·IT", "기타"]
)

idea = st.text_area(
    "탐구하고 싶은 주제와 이유를 자유롭게 적어보세요.",
    placeholder="예: 우리 동네 미세먼지 농도와 호흡기 질환 발생률의 관계가 궁금하다. 왜냐하면...",
    height=150
)

data_plan = st.radio(
    "이 주제를 탐구하려면 어떤 데이터가 필요할까요?",
    ["오늘 사용한 CO2·기온 데이터를 더 깊이 분석하고 싶다",
     "완전히 새로운 데이터를 찾아야 한다",
     "아직 잘 모르겠다"]
)

if st.button("제출하기"):
    st.success("탐구주제 아이디어가 제출되었습니다! 선생님과 상담하며 구체화해봐요.")
    st.write("**선택한 관심 분야:**", ", ".join(interest_area) if interest_area else "없음")
    st.write("**작성한 아이디어:**", idea if idea else "없음")
    st.write("**데이터 계획:**", data_plan)
