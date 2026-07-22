import streamlit as st

st.title("📰 2차시 - ③ 기사 조사 요약")
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
