import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("📊 1차시 - ③ 데이터 비교")


# ---------------------------------------------------------
# 0) 교사 제공 데이터 로딩 (co2_mm_mlo.csv + global_temp_annual.csv를
#    직접 연평균으로 가공해서 사용. co2_mm_mlo.csv는 헤더와 실제 데이터 컬럼
#    수가 하나 어긋나 있어(NOAA 원자료 특성) 위치 기준으로 읽는다.)
# ---------------------------------------------------------
@st.cache_data
def load_teacher_data():
    cols = ["Date", "Decimal_Date", "Average", "Interpolated", "Days", "StdDev", "Unc"]
    co2 = pd.read_csv("data/co2_mm_mlo.csv", skiprows=1, header=None, names=cols)
    co2["Year"] = co2["Date"].str.slice(0, 4).astype(int)
    co2_annual = (
        co2[co2["Average"] > 0].groupby("Year")["Average"].mean().reset_index()
    )
    co2_annual.columns = ["Year", "CO2_ppm"]

    temp = pd.read_csv("data/global_temp_annual.csv")
    temp_g = temp[temp["Source"] == "GISTEMP"][["Year", "Mean"]].rename(
        columns={"Mean": "Temp_Anomaly_C"}
    )

    merged = pd.merge(co2_annual, temp_g, on="Year", how="inner").sort_values("Year")
    return merged


try:
    teacher_df = load_teacher_data()
except FileNotFoundError:
    teacher_df = None


# ---------------------------------------------------------
# 1) 훅(hook) — 교과서 그래프를 먼저 보여주고 질문 던지기
# ---------------------------------------------------------
st.subheader("🔎 정말 그럴까?")
st.markdown(
    "아래는 통합과학2 교과서에 나오는 그래프입니다. "
    "**이산화 탄소 농도와 지구 평균 기온 변화**를 함께 나타낸 것이에요."
)
st.image(
    "assets/textbook_co2_temp_graph.png",
    caption="출처: 기상청 종합기후변화감시정보",
    use_container_width=True,
)

st.markdown(
    "**이 그래프, 정말 사실일까요?** 혹시 특정 구간만 잘라서 보여주거나, "
    "우연히 두 그래프의 모양이 비슷해 보이는 건 아닐까요?"
)
st.radio(
    "이 그래프를 보고 어떤 생각이 드나요? **정말 CO2가 늘어나면 기온도 오를까요?**",
    ["선택해주세요", "그렇다, 확실히 관련 있어 보인다", "우연의 일치일 수도 있다", "잘 모르겠다, 더 확인해보고 싶다"],
    key="hook_question",
)

st.info("직접 자료를 찾아서 나만의 그래프를 그려보고, 그 다음에 선생님이 준비한 실제 관측 자료와 비교해봅시다. 👇")

st.divider()

# ---------------------------------------------------------
# 2) 학생 데이터 찾기 안내 (상세 가이드) — 기존 내용 그대로 유지
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
# 3) 업로드 + 출처 + 선택 이유 (기존 내용 그대로 유지)
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

st.subheader("📈 내가 찾은 자료로 그래프 그려보기")
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
            fig_student = px.line(student_df, y=y_cols, title="내가 업로드한 데이터")
            st.plotly_chart(fig_student, use_container_width=True)
    else:
        st.dataframe(student_df.head())
    st.caption(f"출처: {student_source if student_source else '(출처를 입력해주세요)'}")
    if student_reason:
        st.caption(f"선택 이유: {student_reason}")
else:
    st.info("⬆️ 위에서 CSV 파일을 업로드하면 그래프가 여기에 나타납니다.")

st.divider()

# ---------------------------------------------------------
# 4) 선생님이 제시하는 그래프 — 클릭해야 보이도록 구성
#    (내가 그린 그래프와 먼저 스스로 비교·판단해본 뒤에 확인하도록 유도)
# ---------------------------------------------------------
st.subheader("🧑‍🏫 선생님이 제시하는 그래프와 비교해보기")
st.markdown(
    "내가 찾은 자료로 그린 그래프와 비교해보기 전에, 먼저 스스로 결론을 내려보세요. "
    "준비되었다면 아래를 눌러 선생님이 준비한 **실제 관측 자료** 그래프를 확인해보세요."
)

with st.expander("👀 선생님이 사용한 그래프 확인하기 (클릭해서 펼치기)"):
    if teacher_df is not None:
        fig_teacher = go.Figure()
        fig_teacher.add_trace(go.Scatter(
            x=teacher_df["Year"], y=teacher_df["Temp_Anomaly_C"],
            name="기온 편차 (℃)", mode="lines",
            line=dict(color="#E8752C", width=3),
        ))
        fig_teacher.add_trace(go.Scatter(
            x=teacher_df["Year"], y=teacher_df["CO2_ppm"],
            name="CO2 농도 (ppm)", mode="lines",
            line=dict(color="#3B7FC4", width=3),
            yaxis="y2",
        ))
        fig_teacher.update_layout(
            title=f"연도별 CO2 농도 및 기온 이상치 ({teacher_df['Year'].min()}~{teacher_df['Year'].max()}, 실제 관측)",
            xaxis_title="연도(년)",
            yaxis=dict(title="기온 편차 (℃)"),
            yaxis2=dict(title="CO2 농도 (ppm)", overlaying="y", side="right"),
            legend=dict(orientation="h", y=1.15),
            height=460,
            margin=dict(l=10, r=10, t=60, b=10),
        )
        st.plotly_chart(fig_teacher, use_container_width=True)
        st.caption(
            "출처: CO2 농도 — NOAA Global Monitoring Laboratory (gml.noaa.gov/ccgg/trends, 마우나로아 관측소 연평균) · "
            "기온 편차 — NASA GISTEMP (data.giss.nasa.gov/gistemp). 두 자료 모두 data 폴더의 sources.txt에 정리되어 있습니다."
        )
    else:
        st.warning("co2_mm_mlo.csv 또는 global_temp_annual.csv 파일을 data 폴더에서 찾을 수 없습니다.")

    st.markdown("#### 🧑‍🏫 선생님은 왜 이 데이터를 골랐을까?")
    st.markdown("""
    - **지역(마우나로아)**: 하와이 마우나로아 관측소는 도시나 공장 같은 오염원에서 멀리 떨어져 있어,
      **지역적 영향을 받지 않는 전 지구 대기의 평균적인 CO2 농도**를 잘 보여줍니다. 그래서 전 세계
      과학자들이 가장 신뢰하는 CO2 기준 자료로 씁니다.
    - **기간**: 마우나로아에서 CO2를 측정하기 시작한 1958년 이후, 두 자료(CO2, 기온)가
      **공통으로 겹치는 전체 기간**을 다 보여주기 위해 이 범위를 선택했습니다.
    - **기온 자료(GISTEMP)**: 특정 지역이 아니라 **전 지구 평균 기온 이상치**를 쓴 이유는, CO2 증가가
      특정 나라만이 아니라 지구 전체에 미치는 영향이기 때문입니다.

    여러분이 자료를 고를 때도 "왜 이 지역/기간을 골랐는지" 이런 식으로 이유를 생각해보면 좋아요!
    """)

    st.markdown("#### 💻 원본 데이터로 직접 실습해보기")
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
# 5) 비교 후 생각해보기
# ---------------------------------------------------------
st.subheader("✍️ 비교 후 생각해보기")
match_check = st.radio(
    "실제로 CO2가 늘어난 시기와 기온이 오른 시기가 일치하나요?",
    ["선택해주세요", "대체로 일치한다", "일치하지 않는다", "판단하기 어렵다"]
)
topic_1 = st.text_area("이 데이터로 하고 싶은 탐구 주제를 적어보세요.", height=100)
