import streamlit as st

st.title("🧮 2차시 - ② 지구 열수지 계산하기")
st.caption("교과서 자료(『대기과학』, 2016.)의 지구 열수지 평형 그림을 보고 두 가지 문제를 풀어봅시다.")


def parse_int(s):
    """text_input에 입력된 문자열을 정수로 바꿔본다. 숫자가 아니면 None을 반환한다."""
    try:
        return int(str(s).strip())
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------
# 1) 지표·대기·우주로 구분해서 유입·유출 에너지양 비교하기
# ---------------------------------------------------------
col_img, col_input = st.columns([1.15, 1])

with col_img:
    st.image(
        "assets/textbook_heat_budget_diagram_only.png",
        caption="지구의 열수지 평형 (출처: 『대기과학』, 2016.)",
        width=520,
    )

with col_input:
    st.subheader("1️⃣ 유입·유출 에너지양 비교하기")
    st.markdown("""
지표·대기·우주로 구분하여, 각각 **유입되는 에너지양**과 **유출되는 에너지양**을
비교해 보자.

왼쪽 그림 속 화살표 숫자들을 더하고 빼서 계산해보세요.

💡 **힌트 1**: 지표는 태양 복사로 받는 에너지와 대기에서 되돌아오는 에너지를 모두
더해서 유입량을 구해요.

💡 **힌트 2**: 지구는 열수지 평형을 이루므로, 지표·대기·우주 **각각도** 유입되는
에너지양과 유출되는 에너지양이 서로 같아요.
""")

    st.markdown("**지표**")
    sc1, sc2 = st.columns(2)
    with sc1:
        surface_in = st.text_input("유입 에너지양", key="surface_in", placeholder="예: 144")
    with sc2:
        surface_out = st.text_input("유출 에너지양", key="surface_out", placeholder="예: 144")

    st.markdown("**대기**")
    ac1, ac2 = st.columns(2)
    with ac1:
        atmos_in = st.text_input("유입 에너지양", key="atmos_in", placeholder="예: 152")
    with ac2:
        atmos_out = st.text_input("유출 에너지양", key="atmos_out", placeholder="예: 152")

    st.markdown("**우주**")
    uc1, uc2 = st.columns(2)
    with uc1:
        space_in = st.text_input("유입 에너지양", key="space_in", placeholder="예: 100")
    with uc2:
        space_out = st.text_input("유출 에너지양", key="space_out", placeholder="예: 100")

if st.button("정답 확인", key="check1"):
    answers = [
        ("지표 - 유입", surface_in, 144),
        ("지표 - 유출", surface_out, 144),
        ("대기 - 유입", atmos_in, 152),
        ("대기 - 유출", atmos_out, 152),
        ("우주 - 유입", space_in, 100),
        ("우주 - 유출", space_out, 100),
    ]
    all_correct = True
    for name, student_val, correct_val in answers:
        parsed = parse_int(student_val)
        if parsed is None:
            st.warning(f"{name}: 숫자로 입력해주세요.")
            all_correct = False
        elif parsed == correct_val:
            st.success(f"{name}: {parsed} 정답입니다!")
        else:
            st.error(f"{name}: {parsed} → 다시 계산해보세요.")
            all_correct = False

    if all_correct:
        st.balloons()

    with st.expander("🔎 계산 방법 확인하기"):
        st.markdown("""
- **지표 유입 = 144** → 태양 복사로 지표가 흡수하는 에너지(50) + 대기가 지표로 재복사하는 에너지(94)
- **지표 유출 = 144** → 대기로 방출(132) + 우주로 직접 방출(12)
- **대기 유입 = 152** → 태양 복사 중 대기가 흡수하는 에너지(20) + 지표에서 오는 복사 에너지(132)
- **대기 유출 = 152** → 지표로 재복사(94) + 우주로 방출(58)
- **우주 유입 = 100** → 태양 복사(100)
- **우주 유출 = 100** → 반사(30, = 5 + 25) + 지구 복사(70, = 58 + 12)
""")

st.divider()

# ---------------------------------------------------------
# 2) 이산화 탄소 농도가 증가하면 지구 열수지가 어떻게 변동될까?
# ---------------------------------------------------------
st.subheader("2️⃣ 대기 중 이산화 탄소 농도가 증가하면 지구 열수지가 어떻게 변동되는지 표시해 보자")
st.markdown("위 그림을 다시 참고하면서, 대기 중 CO2가 늘어났을 때 각 에너지양이 **어떻게 변할지** 골라보세요.")

step1 = st.radio(
    "① 대기가 흡수하는 에너지양이 132보다?",
    ["선택해주세요", "증가한다", "변화없다", "감소한다"], key="step1",
)
step2 = st.radio(
    "② 대기가 지표로 방출(재복사)하는 에너지양이 94보다?",
    ["선택해주세요", "증가한다", "변화없다", "감소한다"], key="step2",
)
step3 = st.radio(
    "③ 지표가 다시 흡수하는 에너지양이 94보다?",
    ["선택해주세요", "증가한다", "변화없다", "감소한다"], key="step3",
)
step4 = st.radio(
    "④ 지표 온도는?",
    ["선택해주세요", "상승한다", "변화없다", "하강한다"], key="step4",
)

if st.button("정답 확인", key="check2"):
    if "선택해주세요" in (step1, step2, step3, step4):
        st.warning("네 항목을 모두 선택한 뒤 확인해주세요.")
    else:
        correct = (step1 == "증가한다" and step2 == "증가한다" and
                   step3 == "증가한다" and step4 == "상승한다")
        if correct:
            st.success("정답입니다! 이산화 탄소가 늘어나면 대기가 흡수·재복사하는 에너지가 모두 늘고, "
                       "그만큼 지표가 다시 흡수하는 에너지도 늘어서 지표 온도가 상승해요. 👏")
            st.balloons()
        else:
            st.error("다시 생각해볼까요? 이산화 탄소(온실 기체)가 늘면 대기가 지표 복사를 더 많이 붙잡아두고, "
                     "그만큼 지표로 더 많이 되돌려준다는 흐름을 따라가 보세요.")
        st.info(
            "💡 **정리하면:** 대기 중 CO2 농도 증가 → 대기가 흡수하는 에너지양 **증가**(132보다) → "
            "대기가 지표로 재복사하는 에너지양 **증가**(94보다) → 지표가 다시 흡수하는 에너지양 **증가**"
            "(94보다) → 지표 온도 **상승**. 이것이 온실효과가 강화되어 지구 온난화가 일어나는 원리예요."
        )

st.divider()

# ---------------------------------------------------------
# 3) 형성평가 — 위 그림과는 다른 수치로 A값 구하기 (빈칸 1개)
# ---------------------------------------------------------
st.subheader("✅ 형성평가 — 다른 수치로 A값 구하기")
st.markdown("아래는 위 ①번 그림과는 **다른 값**으로 주어진 지구 열수지 그림입니다. **A**값을 구해보세요.")

col_qimg, col_qinput = st.columns([1.15, 1])

with col_qimg:
    st.image("assets/quiz.png", caption="지구의 열수지 (예시와 다른 수치)", width=460)

with col_qinput:
    st.caption("💡 힌트: 지표(또는 대기)도 열수지 평형을 이루므로, 유입되는 에너지양과 "
               "유출되는 에너지양이 서로 같아야 해요.")
    quiz_answer = st.text_input("A값은?", key="formative_quiz", placeholder="숫자만 입력")

    if st.button("정답 확인", key="check_formative"):
        parsed = parse_int(quiz_answer)
        if parsed is None:
            st.warning("숫자로 입력해주세요.")
        elif parsed == 25:
            st.success("정답입니다! A = 25예요. 👏")
            st.balloons()
        else:
            st.error(f"{parsed} → 다시 계산해보세요.")

        with st.expander("🔎 계산 방법 확인하기"):
            st.markdown("""
- **지표로 풀기**: 지표 유입(45 + 88 = 133) = 지표 유출(A + 104 + 4) → A = 133 − 108 = **25**
- **대기로 풀기**: 대기 유입(25 + A + 104) = 대기 유출(88 + 66 = 154) → A = 154 − 129 = **25**
- 두 compartment 중 어느 쪽으로 풀어도 같은 답이 나와요. 이것이 지표·대기가 각각 열수지 평형을 이루고 있다는 증거예요.
""")
