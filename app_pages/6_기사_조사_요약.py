import streamlit as st

st.title("📰 2차시 - ③ 기사 조사 및 요약")
st.caption("지구온난화로 나타날 수 있는 자연환경·인간생활의 변화에 대한 기사를 찾아 요약해보세요.")

st.markdown("""
### 안내
1. 포털 사이트나 뉴스 앱에서 **'지구온난화 영향'**, **'기후변화 피해'** 같은 검색어로 기사를 찾아보세요.
2. 기사 링크를 붙여넣고, 어떤 내용인지 한 문단으로 요약해서 적어보세요.
3. 여러 개 조사했다면 아래에 계속 추가할 수 있습니다.
""")

if "articles" not in st.session_state:
    st.session_state.articles = []

with st.form("article_form", clear_on_submit=True):
    link = st.text_input("기사 링크 (URL)")
    summary = st.text_area("기사 요약 (한 문단)", height=100)
    submitted = st.form_submit_button("추가하기")
    if submitted:
        if link.strip() and summary.strip():
            st.session_state.articles.append({"link": link, "summary": summary})
            st.success("추가되었습니다!")
        else:
            st.warning("링크와 요약을 모두 입력해주세요.")

if st.session_state.articles:
    st.divider()
    st.subheader("📋 내가 조사한 기사 목록")
    for i, article in enumerate(st.session_state.articles, start=1):
        st.markdown(f"**{i}. {article['link']}**")
        st.write(article["summary"])
        st.markdown("---")

st.divider()

# ---------------------------------------------------------
# 나 / 국가 / 전 지구 관점에서 할 수 있는 일 생각해보기
# ---------------------------------------------------------
st.subheader("🌏 지구온난화 피해를 줄이기 위해 할 수 있는 일")
st.markdown("찾아본 기사를 바탕으로, 지구온난화의 피해를 줄이기 위해 **나·국가·전 지구** 관점에서 "
            "각각 할 수 있는 일은 무엇인지 생각해서 적어보자.")

action_me = st.text_area(
    "🙋 나 (개인) 차원에서 할 수 있는 일",
    placeholder="내가 일상에서 실천할 수 있는 일을 자유롭게 적어보세요.",
    height=80, key="action_me",
)
action_nation = st.text_area(
    "🏛️ 국가 차원에서 할 수 있는 일",
    placeholder="정부나 국가 정책 차원에서 할 수 있는 일을 자유롭게 적어보세요.",
    height=80, key="action_nation",
)
action_global = st.text_area(
    "🌍 전 지구 차원에서 할 수 있는 일",
    placeholder="여러 나라가 함께, 전 지구적으로 할 수 있는 일을 자유롭게 적어보세요.",
    height=80, key="action_global",
)

if st.button("제출하기", key="actions_submit"):
    filled = [bool(action_me.strip()), bool(action_nation.strip()), bool(action_global.strip())]
    if not any(filled):
        st.warning("나·국가·전 지구 중 최소 한 가지 관점에서라도 적어주세요.")
    elif all(filled):
        st.success("나·국가·전 지구, 세 관점을 모두 생각해봤네요! 개인의 실천부터 국제 협력까지 "
                   "다양한 층위에서 대응이 필요하다는 걸 잘 이해했어요. 👏")
        st.balloons()
    else:
        missing = []
        if not filled[0]:
            missing.append("나(개인)")
        if not filled[1]:
            missing.append("국가")
        if not filled[2]:
            missing.append("전 지구")
        st.info("좋은 시작이에요! " + ", ".join(missing) + " 관점에서도 할 수 있는 일을 생각해서 "
                "채워보면 더 풍부한 답이 될 거예요.")

    with st.expander("🌱 다른 사람은 이렇게도 생각했어요 (참고 예시)"):
        st.markdown("""
- 🙋 **나**: 대중교통을 이용하고, 사용하지 않는 전자기기의 전원을 꺼둔다.
- 🏛️ **국가**: 재생에너지 발전 비중을 늘리고, 탄소 배출 규제를 강화한다.
- 🌍 **전 지구**: 국제 협약(파리협정 등)을 통해 국가 간 온실가스 감축 목표를 함께 지키고 협력한다.
""")
        st.caption("정답이 정해진 문제가 아니에요. 내가 적은 답과 비교하며 새로운 아이디어를 더 떠올려보세요.")
