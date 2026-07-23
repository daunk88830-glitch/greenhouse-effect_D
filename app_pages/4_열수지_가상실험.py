import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("🧪 2차시 - ① 지구 열수지 가상실험")
st.caption("교과서 실험 '지구 온난화에 따른 지구 열수지 변동 탐구'를 웹에서 가상으로 체험해봅니다.")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    ##### 🎯 목표
    온실 효과 강화에 따른 지구 온난화의 메커니즘과 지구 열수지 변동을 설명할 수 있다.

    ##### 🧰 준비물 (실제 실험 시)
    발포 바이타민, 물, 투명 페트병 2개, 구멍 뚫린 고무마개, 전등(150W 열전구),
    블루투스 온도계, 스마트 기기, 파라 필름
    """)

with col2:
    st.markdown("""
    ##### 🔬 실험 과정 요약
    1. 페트병 A와 B에 물을 절반 정도 채운다.
    2. 페트병 B에만 발포 바이타민을 넣어 이산화 탄소를 발생시킨다.
    3. 전등에서 20cm 떨어진 곳에 두 페트병을 나란히 놓고 전등을 켠다.
    4. 1분 간격으로 10분 동안 온도 변화를 측정한다.

    ##### ⚠️ 안전 수칙
    - 열 전구에 화상을 입지 않도록 주의한다.
    - 발포 바이타민을 녹인 물은 마시지 않는다.
    """)

st.divider()

# ---------------------------------------------------------
# 1) 실험 전 예측하기
# ---------------------------------------------------------
st.subheader("🔮 실험 전 예측해보기")
prediction = st.text_area(
    "페트병 A(CO2 없음)와 페트병 B(CO2 있음) 중 어느 쪽의 온도가 더 높이 올라갈까요? "
    "그렇게 생각한 이유도 함께 적어보세요.",
    height=100,
    placeholder="예: 페트병 B의 온도가 더 높이 올라갈 것 같다. 왜냐하면 이산화 탄소가 온실효과를 일으키기 때문이다."
)

st.divider()

# ---------------------------------------------------------
# 2) 가상실험
# ---------------------------------------------------------
st.subheader("💻 가상실험 해보기")
st.write("센서가 없어도 결과를 볼 수 있도록, 아래 버튼을 누르면 실제 실험 결과 패턴을 반영한 "
         "가상 온도 변화 그래프가 그려집니다.")

if "trials" not in st.session_state:
    st.session_state.trials = []


def run_trial(label, asymptote, color):
    t = np.arange(0, 11)
    noise = np.random.normal(0, 0.15, size=t.shape)
    temp = 20 + (asymptote - 20) * (1 - np.exp(-0.35 * t)) + noise
    st.session_state.trials.append({"label": label, "t": t, "temp": temp, "color": color})


c1, c2 = st.columns(2)
with c1:
    if st.button("🅰️ 페트병 A (CO2 없음) 실험 시작", use_container_width=True):
        run_trial("A: CO2 없음", 24.0, "#378ADD")
with c2:
    if st.button("🅱️ 페트병 B (CO2 있음) 실험 시작", use_container_width=True):
        run_trial("B: CO2 있음", 29.0, "#D85A30")

if st.session_state.trials:
    fig = go.Figure()
    for trial in st.session_state.trials:
        fig.add_trace(go.Scatter(x=trial["t"], y=trial["temp"], mode="lines+markers",
                                  name=trial["label"], line=dict(color=trial["color"], width=3)))
    fig.update_layout(xaxis_title="시간 (분)", yaxis_title="온도 (℃)", height=420,
                       margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig, use_container_width=True)

    if st.button("🔄 실험 초기화"):
        st.session_state.trials = []
        st.rerun()
else:
    st.info("위 버튼을 눌러 가상실험을 시작해보세요.")

st.divider()
st.subheader("✍️ 관찰 및 해석")
obs = st.text_area("두 페트병의 온도 변화 차이로 알 수 있는 것을 설명해보세요.", height=100, key="obs")

if st.button("제출하기", key="obs_submit"):
    text = obs.strip()
    if not text:
        st.warning("관찰한 내용을 적어주세요.")
    else:
        greenhouse_keywords = ["온실", "이산화 탄소", "이산화탄소", "co2"]
        temp_keywords = ["기온", "온도", "상승", "높"]
        has_greenhouse = any(k in text.lower() for k in greenhouse_keywords)
        has_temp = any(k in text for k in temp_keywords)

        if has_greenhouse and has_temp:
            st.success(
                "정확해요! 이산화 탄소(온실 기체)가 있으면 온실효과가 강화되어 기온이 더 크게 "
                "상승한다는 핵심을 잘 짚었어요. 👏"
            )
        elif has_greenhouse or has_temp:
            st.info("좋은 방향이에요! '온실효과'와 '기온 상승'을 연결지어서 한 문장으로 더 정리해볼까요?")
        else:
            st.warning("페트병 B(CO2 있음)가 더 높은 온도까지 올라간 이유를 온실효과와 연결지어 다시 생각해볼까요?")

        with st.expander("💡 예시 답안과 비교해보기"):
            st.write("이산화 탄소가 있으면 온실효과 때문에 기온이 상승한다.")
            st.caption("내가 쓴 답과 비교해보고, 빠진 내용이 있다면 스스로 보완해보세요.")
