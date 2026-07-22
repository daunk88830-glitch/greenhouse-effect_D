import streamlit as st

st.set_page_config(page_title="열수지 계산하기", page_icon="🧮", layout="wide")

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

    if st.button("정답 확인"):
        correct = {"A": 30, "B": 50, "C": 70}
        results = []
        results.append(("A (반사)", a, correct["A"]))
        results.append(("B (지표 흡수)", b, correct["B"]))
        results.append(("C (지구 복사 에너지 방출)", c, correct["C"]))

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
