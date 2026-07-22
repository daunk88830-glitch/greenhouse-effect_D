import streamlit as st

st.set_page_config(page_title="개념 이해", page_icon="📖", layout="wide")

st.title("📖 1차시 - ① 개념 이해")
st.caption("복사 평형이란 무엇인가?")

col1, col2 = st.columns([1.3, 1])

with col1:
    st.image(
        "assets/radiation_balance.png",
        caption="달(대기 없음)과 지구(대기 있음)의 복사 평형 비교",
        use_container_width=True
    )

with col2:
    st.markdown("""
    ### 학습지 안내

    - 달과 지구는 태양으로부터 거리가 거의 같지만, 지구의 평균 온도가 훨씬 높습니다.
    - 그 이유는 지구를 둘러싼 **대기** 때문입니다.
    - 대기가 없는 달은 태양 복사 에너지를 흡수한 만큼 그대로 우주로 방출하며 복사 평형을
      이룹니다.
    - 대기가 있는 지구는 지표가 방출한 복사 에너지의 일부를 대기가 흡수했다가 다시
      지표로 되돌려줍니다(**재복사**). 이 때문에 지구는 더 높은 온도에서 복사 평형을
      이루는데, 이 현상을 **온실효과**라고 합니다.
    """)

st.divider()

st.subheader("✍️ 확인 문제")
st.write("위 내용을 참고하여, **복사 평형이란 무엇인지** 자신의 말로 한 문장으로 써보세요.")

answer = st.text_area(
    "복사 평형이란?",
    placeholder="예: 물체가 흡수하는 에너지양과 방출하는 에너지양이 같아서 온도가 일정하게 유지되는 상태이다.",
    height=100
)

if st.button("제출하기"):
    if answer.strip():
        st.success("제출되었습니다! 다음 페이지(시뮬레이션 체험)로 이동해보세요. 👉")
        st.write(f"**내가 쓴 답:** {answer}")
    else:
        st.warning("답을 입력한 후 제출해주세요.")
