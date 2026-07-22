import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="시뮬레이션 체험", page_icon="🎛️", layout="wide")

st.title("🎛️ 1차시 - ② 시뮬레이션 체험")
st.caption("CO2 농도를 조절하면 대기의 재복사 에너지량이 어떻게 달라질까?")

co2 = st.slider(
    "대기 중 CO2 농도 (ppm)",
    min_value=280, max_value=1000, value=420, step=10,
    help="산업혁명 이전 대기 중 CO2 농도는 약 280ppm이었습니다."
)

# 간단한 학습용 모델: 재복사 비율과 평균기온은 CO2 농도에 비례해 완만히 증가한다고 가정
# (실제 기후모델의 정밀한 계산이 아니라, 개념 이해를 돕기 위한 단순화된 시각화입니다)
reradiation_pct = 70 + 25 * (np.log(co2 / 280) / np.log(1000 / 280))
line_width = 3 + 22 * (np.log(co2 / 280) / np.log(1000 / 280))
est_temp = 15 + 3.5 * (np.log(co2 / 280) / np.log(2))  # 대략 CO2 두 배 증가 시 +3.5℃ 가정

col1, col2 = st.columns(2)

with col1:
    st.subheader("대기 재복사 강조 그림")
    fig = go.Figure()
    # 지표
    fig.add_shape(type="rect", x0=0.1, x1=0.9, y0=0.0, y1=0.15,
                  fillcolor="#639922", line=dict(width=0), opacity=0.6)
    # 대기
    fig.add_shape(type="rect", x0=0.05, x1=0.95, y0=0.35, y1=0.55,
                  fillcolor="#B5D4F4", line=dict(width=0), opacity=0.5)
    # 태양복사 (얇은 고정 화살표)
    fig.add_annotation(x=0.25, y=0.35, ax=0.15, ay=0.9, xref="x", yref="y", axref="x", ayref="y",
                        showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=3, arrowcolor="#D85A30")
    # 지표->대기 방출
    fig.add_annotation(x=0.45, y=0.35, ax=0.42, ay=0.15, xref="x", yref="y", axref="x", ayref="y",
                        showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=3, arrowcolor="#993C1D")
    # 대기->지표 재복사 (굵기가 CO2에 따라 변함)
    fig.add_annotation(x=0.55, y=0.15, ax=0.58, ay=0.35, xref="x", yref="y", axref="x", ayref="y",
                        showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=line_width, arrowcolor="#A32D2D")
    fig.update_xaxes(visible=False, range=[0, 1])
    fig.update_yaxes(visible=False, range=[0, 1])
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10),
                       plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    st.metric("대기 재복사 비율(추정)", f"{reradiation_pct:.0f} %")

with col2:
    st.subheader("CO2 농도와 예상 평균 기온")
    co2_range = np.linspace(280, 1000, 100)
    temp_range = 15 + 3.5 * (np.log(co2_range / 280) / np.log(2))
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=co2_range, y=temp_range, mode="lines",
                               line=dict(color="#D85A30", width=3), name="예상 평균 기온"))
    fig2.add_trace(go.Scatter(x=[co2], y=[est_temp], mode="markers",
                               marker=dict(size=14, color="#791F1F"), name="현재 설정"))
    fig2.update_layout(
        xaxis_title="CO2 농도 (ppm)", yaxis_title="예상 평균 기온 (℃)",
        height=380, margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.metric("예상 평균 기온", f"{est_temp:.1f} ℃")

st.caption("※ 이 그래프는 온실효과 개념 이해를 돕기 위해 단순화한 모델입니다. 실제 기후 예측값이 아닙니다.")

st.divider()
st.subheader("✅ 형성평가")

quiz = st.radio(
    "CO2 농도가 늘어나면 지표의 평균 기온은 어떻게 될까?",
    ["선택해주세요", "오른다", "변화 없다", "내려간다"]
)

if quiz != "선택해주세요":
    if quiz == "오른다":
        st.success("맞아요! CO2가 늘어나면 대기의 재복사가 늘어나 지표 기온이 오릅니다.")
    else:
        st.error("다시 생각해볼까요? 슬라이더를 움직여 재복사 비율이 어떻게 변하는지 다시 확인해보세요.")

reason = st.text_area("왜 그렇게 생각했는지 한 문장으로 써보세요.", height=80)
