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
    "페트병 A(CO₂ 없음)와 페트병 B(CO₂ 있음) 중 어느 쪽의 온도가 더 높이 올라갈까요? "
    "그렇게 생각한 이유도 함께 적어보세요.",
    height=100,
    placeholder="예: 페트병 A(또는 B)의 온도가 더 높이 올라갈 것 같다. 왜냐하면 ~라고 생각하기 때문이다.",
    key="prediction",
)

if st.button("제출하기", key="prediction_submit"):
    pred_text = prediction.strip()
    if not pred_text:
        st.warning("예측과 이유를 적어주세요.")
    else:
        mentions_bottle = ("a" in pred_text.lower()) or ("b" in pred_text.lower()) or ("페트병" in pred_text)
        reason_keywords = ["왜냐하면", "때문", "이산화", "온실", "co2", "때문이다"]
        has_reason = any(k in pred_text.lower() for k in reason_keywords)

        if mentions_bottle and has_reason:
            st.success("어느 쪽이 더 오를지, 그리고 왜 그렇게 생각했는지까지 잘 적었어요! 이제 아래에서 직접 실험으로 확인해볼까요? 👇")
        elif mentions_bottle:
            st.info("어느 페트병일지는 잘 골랐어요! **왜 그렇게 생각했는지 이유**도 한 문장 덧붙여볼까요?")
        else:
            st.info("페트병 A와 B 중 **어느 쪽**의 온도가 더 높이 올라갈지, 그리고 그 이유를 함께 적어보세요.")

# 관찰 후 예측과 비교하는 반응이 여기(예측 섹션 바로 아래)에 나타나도록 자리만 미리 잡아둔다.
# (실제 내용은 아래 '관찰 및 해석'에서 제출한 뒤에 채워지지만, 화면에는 예측 바로 아래에 표시된다.)
prediction_match_placeholder = st.empty()

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
    if st.button("🅰️ 페트병 A (CO₂ 없음) 실험 시작", use_container_width=True):
        run_trial("A: CO₂ 없음", 24.0, "#378ADD")
with c2:
    if st.button("🅱️ 페트병 B (CO₂ 있음) 실험 시작", use_container_width=True):
        run_trial("B: CO₂ 있음", 29.0, "#D85A30")

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
            st.warning("페트병 B(CO₂ 있음)가 더 높은 온도까지 올라간 이유를 온실효과와 연결지어 다시 생각해볼까요?")

        with st.expander("💡 예시 답안과 비교해보기"):
            st.write("이산화 탄소가 있으면 온실효과 때문에 기온이 상승한다.")
            st.caption("내가 쓴 답과 비교해보고, 빠진 내용이 있다면 스스로 보완해보세요.")

        # '🔍 나의 예측과 일치하는지' 반응은 위쪽 '실험 전 예측해보기' 바로 아래 자리(placeholder)에
        # 표시한다. 계산은 관찰 답변이 나온 지금 시점에 하지만, 화면 위치는 예측 섹션 바로 다음이다.
        with prediction_match_placeholder.container():
            st.markdown("##### 🔍 나의 예측과 일치하는지 알아봅시다!")
            prediction_text = (prediction or "").strip()
            if not prediction_text:
                st.warning("예측을 적지 않았어요. 위 '실험 전 예측해보기'에 먼저 답을 적으면, "
                           "관찰 결과를 제출한 뒤 여기에서 예측과 비교해볼 수 있어요.")
            else:
                predicted_b_higher = ("b" in prediction_text.lower()) or ("페트병 b" in prediction_text) or \
                                      ("이산화" in prediction_text and "높" in prediction_text)
                observed_b_higher = has_greenhouse and has_temp

                st.caption(f"내가 적은 예측: “{prediction_text}”")

                if predicted_b_higher and observed_b_higher:
                    st.success(
                        "나의 예측과 실험 관찰 결과가 일치해요! 이산화 탄소(B)가 있을 때 온실효과로 기온이 "
                        "더 크게 상승한다는 예측이 실험으로도 확인되었네요. 👏"
                    )
                elif predicted_b_higher and not observed_b_higher:
                    st.info(
                        "예측은 맞는 방향이었어요! 다만 아래 '관찰 및 해석' 답변에는 온실효과·이산화 탄소와 "
                        "기온 상승의 연결이 조금 더 드러나면 좋겠어요. 예측과 관찰을 같은 표현으로 정리해볼까요?"
                    )
                else:
                    st.info(
                        "예측했던 내용과 실제 관찰 결과를 다시 한번 비교해보세요. 페트병 B(CO₂ 있음)의 온도가 "
                        "더 높이 올라간 것과 나의 처음 예측이 같은 방향인지 확인해보면 좋겠어요."
                    )
