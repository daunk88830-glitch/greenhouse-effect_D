import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 1차시 - ③ 데이터 비교")
st.caption("실제 CO2·기온 데이터를 찾아 업로드하고, 교사가 제공한 데이터와 비교해보세요.")

with st.expander("🔗 추천 데이터 (데이터를 못 찾았다면 여기서 받아보세요)", expanded=True):
    st.markdown("""
    - **기상청 기상자료개방포털**: https://data.kma.go.kr
    - **NOAA 마우나로아 CO2 월평균 농도**: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt
    - **NASA GISTEMP 전지구 기온 이상치**: https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv
    """)

st.subheader("① CSV 업로드 및 출처 입력")
uploaded_file = st.file_uploader("내가 찾은 CSV 파일을 업로드하세요", type=["csv"])
student_source = st.text_input("이 데이터의 출처를 입력하세요", placeholder="예: 기상청 기상자료개방포털, https://data.kma.go.kr")

# 교사 제공 데이터 불러오기
try:
    teacher_df = pd.read_csv("data/teacher_co2_temperature_1959_2023.csv")
except FileNotFoundError:
    teacher_df = None

st.subheader("② 그래프 비교")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**교사 제공 데이터**")
    if teacher_df is not None:
        fig1 = px.line(teacher_df, x="Year", y=["CO2_ppm", "Temp_Anomaly_C"],
                        title="연도별 CO2 농도 및 기온 이상치 (1959~2023)")
        st.plotly_chart(fig1, use_container_width=True)
        st.caption("출처: NOAA Global Monitoring Laboratory / NASA GISTEMP (data/sources.txt 참고)")
    else:
        st.warning("teacher_co2_temperature_1959_2023.csv 파일을 data 폴더에서 찾을 수 없습니다.")

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
    else:
        st.info("⬆️ 위에서 CSV 파일을 업로드하면 그래프가 여기에 나타납니다.")

st.divider()
st.subheader("✍️ 비교 후 생각해보기")
match_check = st.radio(
    "실제로 CO2가 늘어난 시기와 기온이 오른 시기가 일치하나요?",
    ["선택해주세요", "대체로 일치한다", "일치하지 않는다", "판단하기 어렵다"]
)
topic_1 = st.text_area("이 데이터로 하고 싶은 탐구 주제를 적어보세요.", height=100)
