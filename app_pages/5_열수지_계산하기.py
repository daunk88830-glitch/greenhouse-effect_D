import streamlit as st

st.title("🧮 2차시 - ② 지구 열수지 계산하기")
st.caption("빈칸에 알맞은 값을 계산해서 채워보세요.")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.image("assets/earth_heat_budget.png", caption="지구 열수지 (빈칸 A, B, C를 계산해보세요)",
              use_container_width=True)

with col2:
    st.markdown("""
    ### 힌트
    - 지구에 들어오는 태양 복사 에너지를 **100%**라고 합니다.
    - 이 중 일부는 **반사**되어 우주로 돌아가고, 나머지는 **대기와 지표에 흡수**됩니다.
    - 지구는 복사 평형을 이루므로, **흡수한 만큼 지구 복사 에너지로 방출**합니다.
    - 대기 흡수는 20%로 주어져 있습니다.
    """)

    a = st.number_input("A. 반사되는 비율 (%)", min_value=0, max_value=100, value=0, step=1)
    b = st.number_input("B. 지표가 흡수하는 비율 (%)", min_value=0, max_value=100, value=0, step=1)
    c = st.number_input("C. 지구가 방출하는 지구 복사 에너지 비율 (%)", min_value=0, max_value=100, value=0, step=1)

    if st.button("정답 확인", key="check1"):
        correct = {"A": 30, "B": 50, "C": 70}
        results = [("A (반사)", a, correct["A"]),
                   ("B (지표 흡수)", b, correct["B"]),
                   ("C (지구 복사 에너지 방출)", c, correct["C"])]

        all_correct = True
        for name, student_val, correct_val in results:
            if student_val == correct_val:
                st.success(f"{name}: {student_val}% 정답입니다!")
            else:
                st.error(f"{name}: {student_val}% → 다시 계산해보세요. (힌트: 100%를 기준으로 계산)")
                all_correct = False

        if all_correct:
            st.balloons()

st.divider()

# ---------------------------------------------------------
# 온실 기체 증가 상황을 가정한 두 번째 빈칸 채우기
# ---------------------------------------------------------
st.subheader("🌫️ 온실 기체가 증가했다면? 같은 그림으로 다시 생각해보기")
st.markdown("""
이번엔 대기 중 온실 기체(CO2 등)의 양이 크게 늘어났다고 가정해봅시다.
**위와 똑같은 그림**에서 A, B, C 값은 온실 기체가 늘어나기 전과 비교했을 때 어떻게 달라질까요?
(숫자가 아니라 변화 방향을 골라보세요)
""")

col3, col4 = st.columns([1.2, 1])
with col3:
    st.image("assets/earth_heat_budget.png", caption="동일한 지구 열수지 그림 (온실 기체 증가 가정)",
              use_container_width=True)

with col4:
    a2 = st.selectbox("A. 반사되는 비율(30%)은?", ["선택해주세요", "증가한다", "변화없다", "감소한다"], key="a2")
    b2 = st.selectbox("B. 지표가 흡수하는 비율(50%)은?", ["선택해주세요", "증가한다", "변화없다", "감소한다"], key="b2")
    c2 = st.selectbox("C. 지구 복사 에너지 방출 비율(70%)은?", ["선택해주세요", "증가한다", "변화없다", "감소한다"], key="c2")

    if st.button("정답 확인", key="check2"):
        if "선택해주세요" in (a2, b2, c2):
            st.warning("세 항목을 모두 선택한 뒤 확인해주세요.")
        else:
            if a2 == "변화없다" and b2 == "변화없다" and c2 == "변화없다":
                st.success("정답입니다! 이 그림의 A, B, C는 태양에서 들어오는 에너지(반사·흡수)에 대한 값이라, "
                           "온실 기체가 늘어나도 바뀌지 않아요.")
            else:
                st.error("다시 생각해볼까요?")
            st.info(
                "💡 **왜 변화가 없을까요?** 온실 기체는 지구가 **내보내는(방출하는)** 복사 에너지를 대기가 "
                "흡수했다가 되돌려주는 과정에 영향을 줍니다. 반면 이 그림의 A, B, C는 태양에서 **들어오는** "
                "에너지가 반사·흡수되는 비율이라서, 온실 기체 양과는 직접 관련이 없어요. 대신 온실 기체가 늘면 "
                "**대기가 지표로 재복사하는 에너지의 양**이 늘어나서 지표 온도가 올라가고, 그 결과 지구가 "
                "다시 내보내는 지구 복사 에너지의 '온도'가 높아지는 방식으로 평형이 새롭게 맞춰집니다."
            )

st.divider()
st.subheader("✅ 온실 기체 증가 퀴즈")

quiz1 = st.radio(
    "대기 중 온실 기체(CO2 등)가 증가하면 대기가 지표 복사 에너지를 흡수하는 양은 어떻게 될까?",
    ["선택해주세요", "증가한다", "변화 없다", "감소한다"], key="q1"
)
quiz2 = st.radio(
    "온실 기체가 증가하면 대기가 지표로 재복사하는 양은 어떻게 될까?",
    ["선택해주세요", "증가한다", "변화 없다", "감소한다"], key="q2"
)

if quiz1 != "선택해주세요" and quiz2 != "선택해주세요":
    if quiz1 == "증가한다" and quiz2 == "증가한다":
        st.success("정확해요! 온실 기체가 늘어나면 대기의 흡수량과 재복사량이 모두 늘어나 지구 온난화가 심해집니다.")
    else:
        st.error("다시 생각해볼까요? 온실 기체가 많아지면 대기가 붙잡아두는 에너지가 어떻게 변할지 떠올려보세요.")
