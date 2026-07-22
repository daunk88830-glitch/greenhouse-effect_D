import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="열수지 가상실험", page_icon="🧪", layout="wide")

st.title("🧪 2차시 - ① 지구 열수지 가상실험")
st.caption("교과서의 페트병 실험(발포 바이타민으로 CO2를 만들어 온도 변화 비교하기)을 웹에서 가상으로 체험해봅니다.")

st.markdown("""
**실제 실험 방법 요약**: 페트병 A(물만)와 페트병 B(물 + 발포 바이타민)에 전등을 비추고,
10분 동안 1분 간격으로 온도를 측정하면 이산화 탄소가 있는 페트병 B의 온도가 더 높게 올라갑니다.

센서가 없어도 결과를 볼 수 있도록, 아래 버튼을 누르면 실제 실험 결과 패턴을 반영한
**가상 온도 변화 그래프**가 그려집니다.
""")

if "trials" not in st.session_state:
    st.session_state.trials = []


def run_trial(label, asymptote, color):
    t = np.arange(0, 11)
    noise = np.random.normal(0, 0.15, size=t.shape)
    temp = 20 + (asymptote - 20) * (1 - np.exp(-0.35 * t)) + noise
    st.session_state.trials.append({"label": label, "t": t, "temp": temp, "color": color})


col1, col2 = st.columns(2)
with col1:
    if st.button("🅰️ 페트병 A (CO2 없음) 실험 시작"):
        run_trial("A: CO2 없음", 24.0, "#378ADD")
with col2:
    if st.button("🅱️ 페트병 B (CO2 있음) 실험 시작"):
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
obs = st.text_area("두 페트병의 온도 변화 차이로 알 수 있는 것을 설명해보세요.", height=100)
