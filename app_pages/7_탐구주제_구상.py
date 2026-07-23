import streamlit as st

st.title("💡 2차시 - ④ 탐구주제 구상하기")
st.caption("학기 말 주제탐구 발표를 위한 아이디어를, 공공데이터포털의 실제 자료를 살펴보며 구상해봅시다.")

st.markdown("""
### 안내
꼭 오늘 다룬 CO2·기온 데이터가 아니어도 괜찮습니다. 평소 관심 있던 사회, 경제, 문화,
스포츠 등 **어떤 분야든 데이터로 탐구해볼 수 있는 주제**라면 좋습니다. 이번에는 정부와
공공기관이 만든 데이터를 무료로 볼 수 있는 **공공데이터포털**에서 직접 자료를 둘러보고,
그중 하나를 골라 탐구 주제를 구상해볼 거예요.
""")

interest_area = st.multiselect(
    "관심 있는 분야를 골라보세요 (여러 개 선택 가능)",
    ["기후·환경", "사회·인구", "경제", "건강·의료", "스포츠", "문화·미디어", "기술·IT", "기타"]
)

with st.expander("📍 공공데이터포털에서 자료 찾아보기 (자세한 안내)", expanded=True):
    st.markdown("""
**공공데이터포털**(`data.go.kr`)은 정부와 공공기관이 가진 다양한 데이터를 누구나 무료로
내려받을 수 있게 공개한 사이트예요. 로그인 없이도 데이터 목록을 검색하고 둘러볼 수 있어요.

1. [data.go.kr](https://www.data.go.kr/index.do) 접속
2. 아래 두 가지 방법 중 편한 방법으로 자료를 둘러보세요.
   - **검색으로 찾기**: 상단 검색창에 관심 키워드 입력 (예: '미세먼지', '반려동물', '축제', '교통사고')
   - **분야별로 찾기**: 홈페이지의 **'분야별'** 메뉴에서 위에서 고른 관심 분야와 비슷한 카테고리
     (예: 환경기상, 사회복지, 보건의료, 문화관광, 교통물류, 과학기술 등)를 클릭해서 어떤 데이터들이
     있는지 훑어보기
3. 마음에 드는 데이터셋을 하나 골라서, 그 **제목**과 **링크(URL)** 를 아래에 적어보세요.
4. 파일 형식(CSV, 엑셀 등)이나 미리보기가 제공되면 실제로 어떤 항목(컬럼)이 있는지 확인해보면
   탐구 주제를 구체화하는 데 도움이 돼요.
""")

st.divider()

st.subheader("🔎 내가 찾은 공공데이터")
dataset_title = st.text_input(
    "데이터셋 제목",
    placeholder="예: 서울특별시 미세먼지 측정 자료",
)
dataset_link = st.text_input(
    "데이터셋 링크 (URL)",
    placeholder="예: https://www.data.go.kr/data/...",
)

idea = st.text_area(
    "이 데이터로 탐구하고 싶은 주제와 이유를 자유롭게 적어보세요.",
    placeholder="예: 우리 동네 미세먼지 농도와 호흡기 질환 발생률의 관계가 궁금하다. 왜냐하면...",
    height=150
)

if st.button("제출하기"):
    has_dataset = bool(dataset_title.strip()) and bool(dataset_link.strip())
    has_idea = bool(idea.strip())

    if not has_dataset and not has_idea:
        st.warning("공공데이터포털에서 찾은 데이터셋 제목·링크와, 탐구 아이디어를 모두 적어주세요.")
    elif not has_dataset:
        st.info("탐구 아이디어는 잘 적었어요! 위에서 실제로 찾은 **데이터셋 제목과 링크**도 함께 적어주면 "
                "탐구 계획이 더 구체적으로 완성돼요.")
    elif not has_idea:
        st.info("데이터셋은 잘 찾았어요! 이 데이터로 **어떤 걸 탐구하고 싶은지, 왜 궁금한지**도 적어볼까요?")
    else:
        reason_keywords = ["왜냐하면", "때문", "궁금", "싶어서", "싶다", "알아보고"]
        has_reason = any(k in idea for k in reason_keywords)
        if has_reason:
            st.success("탐구 주제 구상이 아주 잘 정리됐어요! 실제 공공데이터까지 찾아서 이유도 명확하게 "
                       "적었네요. 이 주제로 학기말 탐구를 시작해봐도 좋겠어요. 👏")
            st.balloons()
        else:
            st.success("데이터셋과 탐구 아이디어를 잘 적었어요! 여기에 **왜 그 주제가 궁금한지 이유**까지 "
                       "한 문장 덧붙이면 더 완성도 있는 탐구 계획이 될 거예요.")

        st.markdown("---")
        st.write("**선택한 관심 분야:**", ", ".join(interest_area) if interest_area else "없음")
        st.write("**찾은 데이터셋:**", f"[{dataset_title}]({dataset_link})" if dataset_title else "없음")
        st.write("**탐구 아이디어:**", idea if idea else "없음")
