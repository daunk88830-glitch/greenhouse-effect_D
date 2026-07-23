import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 1차시 - ③ 데이터 비교")

# ---------------------------------------------------------
# 1) 교사 제공 그래프를 먼저 보여주고 질문 던지기
# ---------------------------------------------------------
st.subheader("🔎 정말 그럴까?")
st.markdown(
    "아래 그래프는 실제 관측 자료를 바탕으로 그린 **CO2 농도와 지구 평균 기온 변화**입니다. "
    "교과서에서 본 것과 비슷한 그래프예요."
)

try:
    teacher_df = pd.read_csv("data/teacher_co2_temperature_1959_2025.csv")
except FileNotFoundError:
    teacher_df = None

if teacher_df is not None:
    fig0 = px.line(teacher_df, x="Year", y=["CO2_ppm", "Temp_Anomaly_C"],
                    title="연도별 CO2 농도 및 기온 이상치 (1959~2025)")
    st.plotly_chart(fig0, use_container_width=True)
    st.caption("출처: NOAA Global Monitoring Laboratory / NASA GISTEMP (data/sources.txt 참고)")

st.radio(
    "이 그래프를 보고 어떤 생각이 드나요? **정말 CO2가 늘어나면 기온도 오를까요?**",
    ["선택해주세요", "그렇다, 확실히 관련 있어 보인다", "우연의 일치일 수도 있다", "잘 모르겠다, 더 확인해보고 싶다"],
    key="hook_question",
)

with st.expander("🧑‍🏫 선생님은 왜 이 데이터를 골랐을까?"):
    st.markdown("""
    - **지역(마우나로아)**: 하와이 마우나로아 관측소는 도시나 공장 같은 오염원에서 멀리 떨어져 있어,
      **지역적 영향을 받지 않는 전 지구 대기의 평균적인 CO2 농도**를 잘 보여줍니다. 그래서 전 세계
      과학자들이 가장 신뢰하는 CO2 기준 자료로 씁니다.
    - **기간(1959~2025년)**: 마우나로아에서 CO2를 측정하기 시작한 1958년 이후, 두 자료(CO2, 기온)가
      **공통으로 겹치는 전체 기간**을 다 보여주기 위해 이 범위를 선택했습니다.
    - **기온 자료(GISTEMP)**: 특정 지역이 아니라 **전 지구 평균 기온 이상치**를 쓴 이유는, CO2 증가가
      특정 나라만이 아니라 지구 전체에 미치는 영향이기 때문입니다.

    여러분이 자료를 고를 때도 "왜 이 지역/기간을 골랐는지" 이런 식으로 이유를 생각해보면 좋아요!
    """)

st.divider()

# ---------------------------------------------------------
# 2-1) 원본 파일 다운로드 실습
# ---------------------------------------------------------
st.subheader("💻 원본 데이터로 직접 실습해보기")
st.markdown(
    "선생님이 위 그래프를 만들 때 사용한 **원본 파일 그대로**를 다운로드해서, "
    "엑셀이나 이 웹앱 말고 다른 도구(엑셀, 구글 시트, 파이썬 등)로 직접 그래프를 그려보는 연습을 해볼 수 있어요."
)

dl_col1, dl_col2 = st.columns(2)
with dl_col1:
    with open("data/co2_mm_mlo.csv", "rb") as f:
        st.download_button(
            "⬇️ co2_mm_mlo.csv 다운로드 (마우나로아 월별 CO2 농도)",
            data=f,
            file_name="co2_mm_mlo.csv",
            mime="text/csv",
            use_container_width=True,
        )
with dl_col2:
    with open("data/global_temp_annual.csv", "rb") as f:
        st.download_button(
            "⬇️ global_temp_annual.csv 다운로드 (전지구 연평균 기온 이상치)",
            data=f,
            file_name="global_temp_annual.csv",
            mime="text/csv",
            use_container_width=True,
        )

st.caption("두 파일 모두 data 폴더의 sources.txt에 정확한 출처가 정리되어 있습니다.")

st.divider()

# ---------------------------------------------------------
# 2) 학생 데이터 찾기 안내 (상세 가이드)
# ---------------------------------------------------------
st.subheader("🔗 나만의 자료 찾아보기")
st.markdown(
    "이제 여러분 차례예요! CO2 농도나 기온 변화에 관한 자료를 직접 찾아보고, "
    "**어떤 지역·기간의 자료를 골랐는지, 왜 그렇게 골랐는지**도 함께 적어볼 거예요."
)

with st.expander("📍 어디서, 어떻게 자료를 찾을까? (자세한 안내)", expanded=True):
    st.markdown("""
**① 기상청 기상자료개방포털 (국내 기온 자료, 추천)**
1. [data.kma.go.kr](https://data.kma.go.kr) 접속
2. 상단 메뉴에서 **'기후통계분석' → '기온분석'** (또는 '지상관측자료') 클릭
3. 원하는 **지점(예: 서울, 부산, 우리 지역)** 과 **기간**을 선택
4. 조회 결과 화면에서 **'다운로드' 또는 'CSV' 버튼** 클릭

**② NOAA 마우나로아 CO2 농도 (전 지구 CO2 자료)**
1. [gml.noaa.gov/ccgg/trends](https://gml.noaa.gov/ccgg/trends) 접속
2. 화면의 **'Data' 탭**에서 Monthly 또는 Annual CSV/TXT 파일 링크 클릭 → 다운로드

**③ Our World in Data (초보자에게 가장 쉬움, 추천)**
1. [ourworldindata.org/co2-and-greenhouse-gas-emissions](https://ourworldindata.org/co2-and-greenhouse-gas-emissions) 접속
2. 페이지를 내려서 원하는 그래프를 찾고, 그래프 아래 **'Download' 버튼**에서 CSV 다운로드
3. 국가별·연도별로 이미 깔끔하게 정리되어 있어서 **엑셀처럼 바로 열어볼 수 있어요**

**④ NASA GISTEMP (전 지구 기온 이상치)**
1. [data.giss.nasa.gov/gistemp](https://data.giss.nasa.gov/gistemp) 접속
2. 'Global-mean monthly, seasonal, and annual means' 표에서 CSV 다운로드

자료를 다운로드했으면, 엑셀이나 이 웹앱에서 열어 어떤 열(컬럼)이 있는지 먼저 확인해보세요.
""")

st.divider()

# ---------------------------------------------------------
# 3) 업로드 + 출처 + 선택 이유
# ---------------------------------------------------------
st.subheader("① CSV 업로드 및 출처 · 선택 이유 입력")

uploaded_file = st.file_uploader("내가 찾은 CSV 파일을 업로드하세요", type=["csv"])
student_source = st.text_input(
    "이 데이터의 출처를 입력하세요",
    placeholder="예: 기상청 기상자료개방포털, https://data.kma.go.kr"
)
student_reason = st.text_area(
    "이 지역·기간의 자료를 선택한 이유를 적어주세요.",
    placeholder="예: 내가 사는 지역의 최근 10년간 기온 변화가 궁금해서 서울 지점, 2014~2023년 자료를 선택했다.",
    height=80,
)

st.subheader("② 그래프 비교")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**교사 제공 데이터**")
    if teacher_df is not None:
        fig1 = px.line(teacher_df, x="Year", y=["CO2_ppm", "Temp_Anomaly_C"],
                        title="연도별 CO2 농도 및 기온 이상치 (1959~2025)")
        st.plotly_chart(fig1, use_container_width=True)
        st.caption("출처: NOAA Global Monitoring Laboratory / NASA GISTEMP (data/sources.txt 참고)")
    else:
        st.warning("teacher_co2_temperature_1959_2025.csv 파일을 data 폴더에서 찾을 수 없습니다.")

with col2:
    st.markdown("**내가 업로드한 데이터**")
    if uploaded_file is not None:
        try:
            student_df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            student_df = pd.read_csv(uploaded_file, encoding="cp949")

        numeric_cols = student_df.select_dtypes(include="number").columns.tolist()
        if numeric_cols:
            y_cols = st.multiselect("그래프로 볼 변수 선택", numeric_cols, default=numeric_cols[:1])
            if y_cols:
                fig2 = px.line(student_df, y=y_cols, title="내가 업로드한 데이터")
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.dataframe(student_df.head())
        st.caption(f"출처: {student_source if student_source else '(출처를 입력해주세요)'}")
        if student_reason:
            st.caption(f"선택 이유: {student_reason}")
    else:
        st.info("⬆️ 위에서 CSV 파일을 업로드하면 그래프가 여기에 나타납니다.")

st.divider()
st.subheader("✍️ 비교 후 생각해보기")
match_check = st.radio(
    "실제로 CO2가 늘어난 시기와 기온이 오른 시기가 일치하나요?",
    ["선택해주세요", "대체로 일치한다", "일치하지 않는다", "판단하기 어렵다"]
)
topic_1 = st.text_area("이 데이터로 하고 싶은 탐구 주제를 적어보세요.", height=100)
