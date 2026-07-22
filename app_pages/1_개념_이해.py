import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

st.title("📖 1차시 - ① 개념 이해")

# ---------------------------------------------------------
# 1) 복사 평형 개념 먼저 제시
# ---------------------------------------------------------
st.markdown("""
<div style="background-color:#F4F9F4; border:1px solid #6FAE3E; border-radius:10px;
            padding:18px 22px; margin-bottom:18px;">
<h4 style="margin-top:0;">지구 복사 평형은 어떻게 일어날까?</h4>
<p style="font-size:16px; line-height:1.7;">
태양이 방출하는 복사 에너지를 <b>태양 복사 에너지</b>라 하고, <br> 지구가 방출하는 복사 에너지를
<b>지구 복사 에너지</b>라고 합니다. <br> 지구는 태양 복사 에너지를 <b style="color:#D8443C;">흡수</b> 하고 지구 복사 에너지를
<b style="color:#2C6FBB;">방출</b>하면서 <b>복사 평형</b>을 이루고 있습니다.
</p>
<div style="background-color:#3FA34D; color:white; display:inline-block; padding:6px 18px;
            border-radius:20px; font-weight:bold; margin-bottom:8px;">복사 평형</div>
<p style="font-size:17px; text-align:center; line-height:1.8;">
<b style="color:#D8443C;">흡수</b>하는 복사 에너지의 양 = <b style="color:#2C6FBB;">방출</b>하는 복사 에너지의 양 
</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2) 달 vs 지구 비교 삽화 + 온실효과 설명
# ---------------------------------------------------------
col1, col2 = st.columns([1.3, 1])

with col1:
    st.image("assets/moon_earth_characters.png",
              caption="대기가 없는 달과 대기가 있는 지구의 복사 평형 비교",
              use_container_width=True)

with col2:
    st.markdown("""
    <div style="background-color:#FFF7E6; border:2px solid #F2A623; border-radius:10px;
                padding:16px 20px;">
    <h4 style="margin-top:0; color:#B5760F;">🌡️ 온실효과란?</h4>
    <p style="font-size:15px; line-height:1.7;">
    <b>대기가 지표로 방출하는 복사 에너지 때문에 평균 기온이 높게 나타나는 현상</b>을
    온실효과라고 합니다.
    </p>
    <p style="font-size:14px; line-height:1.6;">
    지구 대기를 이루는 기체 중 이 온실효과를 일으키는 기체를 <b>온실 기체</b>라고 하며,
    대표적으로 다음이 있습니다.
    </p>
    <div style="text-align:center; font-size:16px; font-weight:bold; color:#712B13;">
    수증기 · 이산화 탄소 · 메테인
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown("""
    - 대기가 없는 **달**은 태양 복사 에너지를 흡수한 만큼 그대로 방출하며 복사 평형을 이룹니다.
    - 대기가 있는 **지구**는 지표가 방출한 에너지의 일부를 대기가 흡수했다가 다시
      지표로 되돌려줍니다(**재복사**). 이 때문에 지구는 대기가 없을 때보다
      더 높은 온도에서 복사 평형을 이룹니다.
    """)

st.divider()

# ---------------------------------------------------------
# 3) 인터랙티브 확인 문제: 화살표 클릭 미션
# ---------------------------------------------------------
st.subheader("🎯 확인 문제 - 화살표를 클릭해보자!")
st.markdown("""
아래 그림은 대기가 있는 지구의 복사 평형을 나타낸 것입니다. 이 그림에는 화살표가 4개 있어요.
**대기가 생김으로 인해 새롭게 추가된 화살표**를 찾아 클릭해보세요!
""")

coords = streamlit_image_coordinates(
    "assets/radiation_arrows_quiz.png",
    width=500,
    key="arrow_quiz"
)

# 이미지 원본은 600x600px 기준으로 제작되었고, width=500으로 표시되므로
# 클릭 좌표를 원본 비율(600/500)로 환산합니다.
ARROWS = {
    "①": (144, 273, "태양 복사 에너지"),
    "②": (276, 435, "지표 방출"),
    "③": (384, 435, "대기 재복사"),
    "④": (477, 168, "우주로 방출"),
}
CORRECT = "③"
THRESHOLD = 60

if coords is not None:
    scale = 600 / 500
    click_x = coords["x"] * scale
    click_y = coords["y"] * scale

    best_label, best_dist = None, 999999
    for label, (ax_, ay_, _) in ARROWS.items():
        dist = ((click_x - ax_) ** 2 + (click_y - ay_) ** 2) ** 0.5
        if dist < best_dist:
            best_dist = dist
            best_label = label

    if best_dist <= THRESHOLD:
        if best_label == CORRECT:
            st.success("딩동댕~ 잘했어! 🎉 대기가 생기면서 '대기 재복사' 화살표가 새로 추가되었어요.")
            st.balloons()
        else:
            st.error(f"{best_label}번 화살표를 클릭했어요. 다시 생각해보자~ 🤔")
    else:
        st.warning("화살표에 조금 더 가깝게 클릭해볼까요?")
else:
    st.caption("👆 위 그림에서 화살표를 클릭해보세요.")
