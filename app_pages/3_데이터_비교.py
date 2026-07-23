import streamlit as st
import pandas as pd
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
img_col1, img_col2, img_col3 = st.columns([1, 2, 1])
with img_col2:
    st.image(
        "assets/textbook_co2_temp_graph.png",
        caption="출처: 기상청 종합기후변화감시정보",
        width=620,
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
st.markdown(
    "위 그래프와 같이 **CO2 농도 자료**와 **기온 자료**, 이렇게 2개의 자료를 각각 찾아서 올려보세요. "
    "(아직 하나만 찾았다면 하나만 올려도 괜찮아요.)"
)

up_col1, up_col2 = st.columns(2)
with up_col1:
    st.markdown("**🔵 ① 이산화 탄소 농도 자료**")
    co2_file = st.file_uploader("CO2 농도 CSV 업로드", type=["csv"], key="co2_file")
    co2_source = st.text_input(
        "출처",
        key="co2_source",
        placeholder="예: NOAA, https://gml.noaa.gov/ccgg/trends/",
    )
with up_col2:
    st.markdown("**🟠 ② 기온 자료**")
    temp_file = st.file_uploader("기온 CSV 업로드", type=["csv"], key="temp_file")
    temp_source = st.text_input(
        "출처",
        key="temp_source",
        placeholder="예: 기상청, https://data.kma.go.kr",
    )

student_reason = st.text_area(
    "이 지역·기간의 자료를 선택한 이유를 적어주세요.",
    placeholder="예: 내가 사는 지역의 최근 10년간 기온 변화가 궁금해서 서울 지점, 2014~2023년 자료를 선택했다.",
    height=80,
)


def read_csv_safe(f):
    try:
        return pd.read_csv(f)
    except UnicodeDecodeError:
        f.seek(0)
        return pd.read_csv(f, encoding="cp949")


# 학생들이 기상청/NOAA/GISTEMP/Our World in Data 등에서 흔히 받게 되는 컬럼명을
# 영어를 몰라도 고를 수 있도록 한글 라벨로 바꿔서 보여준다.
_X_KEYWORDS = ["year", "연도", "년도", "date", "날짜", "decimal", "time", "월", "month", "일시", "시각"]
_Y_CO2_KEYWORDS = ["co2", "ppm", "농도", "concentration", "average", "interpolated", "trend"]
_Y_TEMP_KEYWORDS = ["temp", "기온", "anomaly", "편차", "온도"]


def korean_col_label(col, axis_kind):
    """axis_kind: 'x' (연도/날짜) / 'y_co2' (CO2 농도) / 'y_temp' (기온)"""
    name = str(col).lower()
    if axis_kind == "x" and any(k in name for k in _X_KEYWORDS):
        return f"📅 연도/날짜 (원본 컬럼명: {col})"
    if axis_kind == "y_co2" and any(k in name for k in _Y_CO2_KEYWORDS):
        return f"🔵 CO2 농도 (원본 컬럼명: {col})"
    if axis_kind == "y_temp" and any(k in name for k in _Y_TEMP_KEYWORDS):
        return f"🟠 기온 (원본 컬럼명: {col})"
    return f"{col} (직접 확인 필요)"


def guess_default_index(cols, axis_kind):
    keywords = {"x": _X_KEYWORDS, "y_co2": _Y_CO2_KEYWORDS, "y_temp": _Y_TEMP_KEYWORDS}.get(axis_kind, [])
    for i, c in enumerate(cols):
        if any(k in str(c).lower() for k in keywords):
            return i
    if axis_kind in ("y_co2", "y_temp"):
        # 값 컬럼 키워드와 매칭되지 않으면, 최소한 연도/날짜로 보이는 컬럼은 피해서 고른다.
        for i, c in enumerate(cols):
            if not any(k in str(c).lower() for k in _X_KEYWORDS):
                return i
    return 0


st.subheader("📈 내가 찾은 자료로 그래프 그려보기")
if co2_file is not None or temp_file is not None:
    fig_student = go.Figure()
    both_uploaded = (co2_file is not None) and (temp_file is not None)
    co2_y = temp_y = None

    if co2_file is not None:
        co2_student_df = read_csv_safe(co2_file)
        co2_num_cols = co2_student_df.select_dtypes(include="number").columns.tolist()
        if co2_num_cols:
            co2_x_options = co2_student_df.columns.tolist()
            cc1, cc2 = st.columns(2)
            with cc1:
                co2_x = st.selectbox(
                    "CO2 자료 - 가로축(연도/날짜) 선택", co2_x_options,
                    index=guess_default_index(co2_x_options, "x"),
                    format_func=lambda c: korean_col_label(c, "x"),
                    key="co2_x",
                )
            with cc2:
                co2_y = st.selectbox(
                    "CO2 자료 - 세로축(CO2 농도) 선택", co2_num_cols,
                    index=guess_default_index(co2_num_cols, "y_co2"),
                    format_func=lambda c: korean_col_label(c, "y_co2"),
                    key="co2_y",
                )
            fig_student.add_trace(go.Scatter(
                x=co2_student_df[co2_x], y=co2_student_df[co2_y],
                name="🔵 CO2 농도", mode="lines+markers",
                line=dict(color="#3B7FC4", width=3),
            ))
        else:
            st.warning("CO2 자료에서 숫자로 된 값 컬럼을 찾지 못했어요. 아래 표를 확인해주세요.")
            st.dataframe(co2_student_df.head())

    if temp_file is not None:
        temp_student_df = read_csv_safe(temp_file)
        temp_num_cols = temp_student_df.select_dtypes(include="number").columns.tolist()
        if temp_num_cols:
            temp_x_options = temp_student_df.columns.tolist()
            tc1, tc2 = st.columns(2)
            with tc1:
                temp_x = st.selectbox(
                    "기온 자료 - 가로축(연도/날짜) 선택", temp_x_options,
                    index=guess_default_index(temp_x_options, "x"),
                    format_func=lambda c: korean_col_label(c, "x"),
                    key="temp_x",
                )
            with tc2:
                temp_y = st.selectbox(
                    "기온 자료 - 세로축(기온) 선택", temp_num_cols,
                    index=guess_default_index(temp_num_cols, "y_temp"),
                    format_func=lambda c: korean_col_label(c, "y_temp"),
                    key="temp_y",
                )
            fig_student.add_trace(go.Scatter(
                x=temp_student_df[temp_x], y=temp_student_df[temp_y],
                name="🟠 기온", mode="lines+markers",
                line=dict(color="#E8752C", width=3),
                yaxis="y2" if both_uploaded and co2_y else "y",
            ))
        else:
            st.warning("기온 자료에서 숫자로 된 값 컬럼을 찾지 못했어요. 아래 표를 확인해주세요.")
            st.dataframe(temp_student_df.head())

    if co2_y or temp_y:
        st.markdown("**📊 내가 찾은 자료로 그린 그래프**")
        layout_kwargs = dict(
            height=420,
            margin=dict(l=10, r=10, t=20, b=70),
            legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
        )
        if both_uploaded and co2_y and temp_y:
            layout_kwargs["yaxis"] = dict(title="🔵 CO2 농도")
            layout_kwargs["yaxis2"] = dict(title="🟠 기온", overlaying="y", side="right")
        elif co2_y:
            layout_kwargs["yaxis"] = dict(title="🔵 CO2 농도")
        elif temp_y:
            layout_kwargs["yaxis"] = dict(title="🟠 기온")
        fig_student.update_layout(**layout_kwargs)
        st.plotly_chart(fig_student, use_container_width=True)

        src_lines = []
        if co2_y:
            src_lines.append(f"CO2 자료 출처: {co2_source if co2_source else '(출처를 입력해주세요)'}")
        if temp_y:
            src_lines.append(f"기온 자료 출처: {temp_source if temp_source else '(출처를 입력해주세요)'}")
        st.caption(" · ".join(src_lines))
        if student_reason:
            st.caption(f"선택 이유: {student_reason}")
else:
    st.info("⬆️ 위에서 CO2 자료 또는 기온 자료를 업로드하면(둘 다 올리면 더 좋아요!) 그래프가 여기에 나타납니다.")

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
        st.markdown(
            f"**📊 연도별 CO2 농도 및 기온 이상치 ({teacher_df['Year'].min()}~{teacher_df['Year'].max()}, 실제 관측)**"
        )
        fig_teacher = go.Figure()
        fig_teacher.add_trace(go.Scatter(
            x=teacher_df["Year"], y=teacher_df["Temp_Anomaly_C"],
            name="🟠 기온 편차 (℃)", mode="lines",
            line=dict(color="#E8752C", width=3),
        ))
        fig_teacher.add_trace(go.Scatter(
            x=teacher_df["Year"], y=teacher_df["CO2_ppm"],
            name="🔵 CO2 농도 (ppm)", mode="lines",
            line=dict(color="#3B7FC4", width=3),
            yaxis="y2",
        ))
        fig_teacher.update_layout(
            xaxis_title="연도(년)",
            yaxis=dict(title="🟠 기온 편차 (℃)"),
            yaxis2=dict(title="🔵 CO2 농도 (ppm)", overlaying="y", side="right"),
            legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
            height=460,
            margin=dict(l=10, r=10, t=20, b=80),
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
topic_1 = st.text_area("이 데이터로 하고 싶은 탐구 주제를 적어보세요.", height=100, key="topic_1")

if st.button("제출하기", key="topic_1_submit"):
    text = topic_1.strip()
    if not text:
        st.warning("탐구 주제를 적어주세요.")
    else:
        reason_keywords = ["왜냐하면", "때문", "궁금", "싶어서", "싶다", "알아보고"]
        has_reason = any(k in text for k in reason_keywords)
        if len(text) < 15:
            st.info(
                "좋은 시작이에요! 조금 더 구체적으로 적어볼까요? "
                "**어떤 자료로, 무엇을, 왜** 알아보고 싶은지 한두 문장 더 써보면 훨씬 좋아져요."
            )
        elif not has_reason:
            st.success(
                "탐구 주제를 잘 적었어요! 여기에 **왜 그 주제가 궁금한지 이유**까지 한 문장 덧붙이면 "
                "더 완성도 있는 주제가 될 거예요."
            )
        else:
            st.success("주제와 이유까지 아주 잘 정리했어요! 이 주제로 학기말 탐구를 시작해봐도 좋겠어요. 👏")
            st.balloons()
