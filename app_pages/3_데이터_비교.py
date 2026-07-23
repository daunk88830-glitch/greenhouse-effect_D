import io
from collections import Counter
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
**① Our World in Data — CO2 농도 자료 (전 세계, 기간·지역 선택 가능)**
1. [ourworldindata.org/co2-and-greenhouse-gas-emissions](https://ourworldindata.org/co2-and-greenhouse-gas-emissions) 접속
2. 그래프에서 원하는 **국가/지역**과 **기간**을 선택
3. 그래프 아래 **'Download' 버튼**을 클릭해서 CSV 다운로드
4. 'Download' 버튼 대신 **'Data API'라는 회색 박스**가 보인다면, 그 안의
   **'Data URL (CSV format)'** 옆 복사 아이콘을 눌러 링크를 복사하고, 새 브라우저 탭 주소창에
   붙여넣은 뒤 Enter를 누르세요. 그러면 CSV 파일이 그대로 다운로드됩니다.

**② Our World in Data — 기온 자료 (전 세계, 기간·지역 선택 가능)**
1. [ourworldindata.org/explorers/climate-change](https://ourworldindata.org/explorers/climate-change?country=ATA~Gulkana+Glacier~Lemon+Creek+Glacier~OWID_NAM~South+Cascade+Glacier~Wolverine+Glacier~Hawaii~Arctic+Ocean~OWID_NH&Metric=Temperature+anomaly&Long-run+series=false) 접속
2. 그래프에서 원하는 **국가/지역**과 **기간**을 선택
3. ①번과 같은 방법으로 **'Download' 버튼** 또는 **'Data API'** 박스에서 CSV 다운로드

로그인 없이 두 사이트 모두 바로 이용할 수 있어요. (선생님이 사용한 NASA GISTEMP 전 지구 자료는 사이트
구조가 복잡해서 이번 활동에서는 제외했어요. 대신 아래 "선생님이 사용한 그래프"에서 NASA GISTEMP
자료와 출처를 확인할 수 있습니다.)

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
        placeholder="예: Our World in Data, https://ourworldindata.org/co2-and-greenhouse-gas-emissions",
    )
with up_col2:
    st.markdown("**🟠 ② 기온 자료**")
    temp_file = st.file_uploader("기온 CSV 업로드", type=["csv"], key="temp_file")
    temp_source = st.text_input(
        "출처",
        key="temp_source",
        placeholder="예: Our World in Data, https://ourworldindata.org/explorers/climate-change",
    )

student_reason = st.text_area(
    "이 지역·기간의 자료를 선택한 이유를 적어주세요.",
    placeholder="예: 내가 사는 지역의 최근 10년간 기온 변화가 궁금해서 서울 지점, 2014~2023년 자료를 선택했다.",
    height=80,
    key="student_reason",
)

if st.button("제출하기", key="student_reason_submit"):
    reason_text = student_reason.strip()
    if not reason_text:
        st.warning("자료를 선택한 이유를 적어주세요.")
    else:
        reason_keywords = ["왜냐하면", "때문", "궁금", "싶어서", "싶다", "알아보고"]
        place_time_keywords = ["지역", "지점", "년", "월", "기간", "최근", "동안"]
        has_reason = any(k in reason_text for k in reason_keywords)
        has_place_time = any(k in reason_text for k in place_time_keywords)

        if len(reason_text) < 10:
            st.info(
                "좋은 시작이에요! **어떤 지역·기간**의 자료를 골랐는지, **왜** 그 자료를 골랐는지 "
                "조금 더 자세히 적어볼까요?"
            )
        elif has_reason and has_place_time:
            st.success(
                "이유가 아주 명확해요! 지역·기간을 구체적으로 선택하고, 그 이유까지 잘 설명했어요. 👏"
            )
        elif has_place_time:
            st.success(
                "어떤 지역·기간의 자료인지 잘 설명했어요! 왜 그 자료가 궁금했는지 이유도 한 문장 덧붙이면 더 좋아져요."
            )
        else:
            st.info(
                "이유를 잘 적었어요! 다음엔 **어떤 지역·기간**의 자료를 선택했는지도 함께 적어보면 "
                "더 명확한 기록이 될 거예요."
            )


def _decode_bytes(raw):
    """기상청(cp949/euc-kr)·NOAA(utf-8) 등 출처마다 다른 인코딩을 순서대로 시도해서 디코딩한다."""
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="ignore")


def _smart_table_extract(text):
    """기상청 자료처럼 파일 맨 위에 '[검색조건]', '자료구분 : 년' 같은 안내 문구가 여러 줄
    섞여 있는 경우, 실제 표(헤더+데이터)가 시작하는 지점을 자동으로 찾아서 읽는다.
    (콤마로 구분된 필드 수가 가장 많이 반복되는 지점을 '진짜 표'로 판단)
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    if len(lines) < 2:
        return None

    def field_count(ln):
        return len(ln.split(","))

    counts = [field_count(ln) for ln in lines]
    candidate_counts = [c for c in counts if c >= 2]
    if not candidate_counts:
        return None
    mode_width = Counter(candidate_counts).most_common(1)[0][0]
    start_idx = next(i for i, c in enumerate(counts) if c == mode_width)
    table_lines = lines[start_idx:]
    if len(table_lines) < 2:
        return None

    def looks_numeric_row(ln):
        fields = [f.strip().strip('"') for f in ln.split(",")]
        numeric = 0
        for f in fields:
            try:
                float(f)
                numeric += 1
            except ValueError:
                pass
        return numeric >= max(1, len(fields) // 2)

    first_row_is_data = looks_numeric_row(table_lines[0])
    buf = io.StringIO("\n".join(table_lines))
    try:
        if first_row_is_data:
            df = pd.read_csv(buf, header=None, on_bad_lines="skip")
            df.columns = [f"컬럼{i + 1}" for i in range(df.shape[1])]
        else:
            df = pd.read_csv(buf, header=0, on_bad_lines="skip")
    except Exception:
        return None
    if df.shape[1] < 2 or len(df) == 0:
        return None
    return df


def read_csv_safe(f):
    """여러 인코딩·주석 형식을 순서대로 시도해서 최대한 안전하게 CSV를 읽는다.
    (기상청 자료처럼 맨 위에 안내 문구가 여러 줄 섞여 있거나 cp949로 인코딩된 경우,
    NOAA 자료처럼 '#' 설명 줄이 섞여 있거나 헤더·데이터 컬럼 수가 어긋난 경우 모두 시도한다.)
    반환값: (DataFrame 또는 None, 오류 또는 None)
    """
    attempts = [
        dict(),
        dict(encoding="cp949"),
        dict(comment="#"),
        dict(comment="#", encoding="cp949"),
        dict(on_bad_lines="skip"),
        dict(comment="#", on_bad_lines="skip"),
    ]
    last_err = None
    for kwargs in attempts:
        try:
            f.seek(0)
            df = pd.read_csv(f, **kwargs)
            # 컬럼이 1개뿐이면 대부분 구분자/주석 처리가 잘못돼 한 줄이 통째로 붙어버린
            # 경우라서(진짜 데이터로 보기 어려움) 실패로 간주하고 다음 방법을 시도한다.
            if df.shape[1] >= 2 and len(df) > 0:
                return df, None
        except Exception as e:
            last_err = e
            continue

    # 마지막 수단: 안내 문구·주석 줄을 건너뛰고 실제 표가 시작하는 지점을 스스로 찾아서 읽는다.
    try:
        f.seek(0)
        raw = f.read()
        text = _decode_bytes(raw) if isinstance(raw, bytes) else raw
        df = _smart_table_extract(text)
        if df is not None:
            return df, None
    except Exception as e:
        last_err = e

    return None, last_err


# 학생들이 기상청/NOAA/GISTEMP/Our World in Data 등에서 흔히 받게 되는 컬럼명을
# 영어를 몰라도 고를 수 있도록 한글 라벨로 바꿔서 보여준다.
_X_KEYWORDS = ["year", "연도", "년도", "년", "date", "날짜", "decimal", "time", "월", "month", "일시", "시각"]
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


_ENTITY_KEYWORDS = ["entity", "country", "지역", "국가", "region", "nation"]


def filter_to_world_if_mixed(df):
    """Our World in Data 자료처럼 한 CSV 안에 여러 지역/국가(Entity) 데이터가 연도별로
    섞여 있는 경우, 그대로 그래프를 그리면 연도 순서가 지역별로 뒤섞여 선이 지그재그로
    엉키게 된다. 이런 컬럼이 보이면 자동으로 'World'(전 지구) 데이터만 남긴다.
    반환값: (필터링된 DataFrame, 실제로 필터링이 일어났는지 여부)
    """
    entity_col = None
    for c in df.columns:
        name = str(c).lower()
        if any(k in name for k in _ENTITY_KEYWORDS):
            entity_col = c
            break
    if entity_col is None:
        return df, False

    values = df[entity_col].astype(str).str.strip()
    world_mask = values.str.lower() == "world"
    if world_mask.any():
        return df[world_mask].reset_index(drop=True), True

    # 'World'라는 값이 없다면(예: 국가별 자료만 있는 경우), 가장 먼저 나오는
    # 지역/국가 하나만 남긴다. 여러 지역이 섞인 채로 그리는 것보다는 안전하다.
    first_val = values.iloc[0]
    return df[values == first_val].reset_index(drop=True), True


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
st.caption("파일을 업로드하면 가로축(연도/날짜)과 세로축(값)을 자동으로 인식해서 바로 그래프를 그려줘요.")
if co2_file is not None or temp_file is not None:
    fig_student = go.Figure()
    both_uploaded = (co2_file is not None) and (temp_file is not None)
    co2_y = temp_y = None

    if co2_file is not None:
        co2_student_df, co2_err = read_csv_safe(co2_file)
        if co2_student_df is None:
            st.error(
                "CO2 자료를 읽는 중 문제가 발생했어요. 파일이 진짜 CSV(쉼표로 구분된 표) 형식인지 확인해주세요."
            )
        else:
            co2_student_df, co2_was_filtered = filter_to_world_if_mixed(co2_student_df)
            if co2_was_filtered:
                st.caption("ℹ️ 이 자료에는 여러 지역/국가 데이터가 섞여 있어서, 'World'(전 지구, 없으면 첫 번째 지역) "
                           "데이터만 사용했어요.")
            try:
                co2_num_cols = co2_student_df.select_dtypes(include="number").columns.tolist()
                if co2_num_cols:
                    co2_x_options = co2_student_df.columns.tolist()
                    auto_co2_x = co2_x_options[guess_default_index(co2_x_options, "x")]
                    auto_co2_y = co2_num_cols[guess_default_index(co2_num_cols, "y_co2")]
                    with st.expander(
                        f"⚙️ CO2 그래프 축 자동 인식 결과 — 가로축: {auto_co2_x} · 세로축: {auto_co2_y} "
                        "(다르게 바꾸고 싶다면 클릭)"
                    ):
                        cc1, cc2 = st.columns(2)
                        with cc1:
                            co2_x = st.selectbox(
                                "가로축(연도/날짜) 선택", co2_x_options,
                                index=guess_default_index(co2_x_options, "x"),
                                format_func=lambda c: korean_col_label(c, "x"),
                                key="co2_x",
                            )
                        with cc2:
                            co2_y = st.selectbox(
                                "세로축(CO2 농도) 선택", co2_num_cols,
                                index=guess_default_index(co2_num_cols, "y_co2"),
                                format_func=lambda c: korean_col_label(c, "y_co2"),
                                key="co2_y",
                            )
                    co2_plot_df = co2_student_df[[co2_x, co2_y]].dropna().sort_values(co2_x)
                    fig_student.add_trace(go.Scatter(
                        x=co2_plot_df[co2_x], y=co2_plot_df[co2_y],
                        name="🔵 CO2 농도", mode="lines+markers",
                        line=dict(color="#3B7FC4", width=3),
                    ))
                else:
                    st.warning("CO2 자료에서 숫자로 된 값 컬럼을 찾지 못했어요. 아래 표를 확인해주세요.")
                    st.dataframe(co2_student_df.head())
            except Exception as e:
                st.error(f"CO2 자료로 그래프를 그리는 중 문제가 발생했어요: {e}")

    if temp_file is not None:
        temp_student_df, temp_err = read_csv_safe(temp_file)
        if temp_student_df is None:
            st.error(
                "기온 자료를 읽는 중 문제가 발생했어요. 파일이 진짜 CSV(쉼표로 구분된 표) 형식인지 확인해주세요."
            )
        else:
            temp_student_df, temp_was_filtered = filter_to_world_if_mixed(temp_student_df)
            if temp_was_filtered:
                st.caption("ℹ️ 이 자료에는 여러 지역/국가 데이터가 섞여 있어서, 'World'(전 지구, 없으면 첫 번째 지역) "
                           "데이터만 사용했어요.")
            try:
                temp_num_cols = temp_student_df.select_dtypes(include="number").columns.tolist()
                if temp_num_cols:
                    temp_x_options = temp_student_df.columns.tolist()
                    auto_temp_x = temp_x_options[guess_default_index(temp_x_options, "x")]
                    auto_temp_y = temp_num_cols[guess_default_index(temp_num_cols, "y_temp")]
                    with st.expander(
                        f"⚙️ 기온 그래프 축 자동 인식 결과 — 가로축: {auto_temp_x} · 세로축: {auto_temp_y} "
                        "(다르게 바꾸고 싶다면 클릭)"
                    ):
                        tc1, tc2 = st.columns(2)
                        with tc1:
                            temp_x = st.selectbox(
                                "가로축(연도/날짜) 선택", temp_x_options,
                                index=guess_default_index(temp_x_options, "x"),
                                format_func=lambda c: korean_col_label(c, "x"),
                                key="temp_x",
                            )
                        with tc2:
                            temp_y = st.selectbox(
                                "세로축(기온) 선택", temp_num_cols,
                                index=guess_default_index(temp_num_cols, "y_temp"),
                                format_func=lambda c: korean_col_label(c, "y_temp"),
                                key="temp_y",
                            )
                    temp_plot_df = temp_student_df[[temp_x, temp_y]].dropna().sort_values(temp_x)
                    fig_student.add_trace(go.Scatter(
                        x=temp_plot_df[temp_x], y=temp_plot_df[temp_y],
                        name="🟠 기온", mode="lines+markers",
                        line=dict(color="#E8752C", width=3),
                        yaxis="y2" if both_uploaded and co2_y else "y",
                    ))
                else:
                    st.warning("기온 자료에서 숫자로 된 값 컬럼을 찾지 못했어요. 아래 표를 확인해주세요.")
                    st.dataframe(temp_student_df.head())
            except Exception as e:
                st.error(f"기온 자료로 그래프를 그리는 중 문제가 발생했어요: {e}")

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
