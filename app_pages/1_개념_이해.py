import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw
import tempfile
import os

st.title("📖 1차시 - ① 개념 이해")

# ---------------------------------------------------------
# 1) 복사 평형 개념 먼저 제시
# ---------------------------------------------------------
st.markdown("""
<div style="background-color:#F4F9F4; border:1px solid #6FAE3E; border-radius:10px;
            padding:18px 22px; margin-bottom:18px;">
<h4 style="margin-top:0;">지구 복사 평형은 어떻게 일어날까?</h4>
<p style="font-size:16px; line-height:1.7;">
태양이 방출하는 복사 에너지를 <b>태양 복사 에너지</b>라 하고, <br>
지구가 방출하는 복사 에너지를 <b>지구 복사 에너지</b>라고 합니다. <br>
지구는 태양 복사 에너지를 <b style="color:#D8443C;">흡수</b>하고 지구 복사 에너지를
<b style="color:#2C6FBB;">방출</b>하면서 <b>복사 평형</b>을 이루고 있습니다.
</p>
<div style="background-color:#3FA34D; color:white; display:inline-block; padding:6px 18px;
            border-radius:20px; font-weight:bold; margin-bottom:8px;">복사 평형</div>
<p style="font-size:17px; text-align:center; line-height:1.8;">
흡수하는 복사 에너지와<br>
방출하는 복사 에너지의 양이 <span style="color:#D8443C; font-weight:bold;">같은</span> 상태
</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2) 달 vs 지구 비교 (좌: 달, 우: 지구 / 각 이미지 아래 설명)
# ---------------------------------------------------------
st.markdown("#### 🌙🌍 대기가 없는 달과 대기가 있는 지구의 복사 평형 비교")

col1, col2 = st.columns(2)

with col1:
    st.image("assets/moon_only.png", use_container_width=True)
    st.markdown("**🌙 대기가 없는 달**")
    st.markdown(
        "태양 복사 에너지를 흡수한 만큼 그대로 방출하며 복사 평형을 이룹니다."
    )

with col2:
    st.image("assets/earth_only.png", use_container_width=True)
    st.markdown("**🌍 대기가 있는 지구**")
    st.markdown(
        "지표가 방출한 에너지의 일부를 대기가 흡수했다가 다시 지표로 되돌려줍니다(**재복사**). "
        "이 때문에 지구는 대기가 없을 때보다 더 높은 온도에서 복사 평형을 이룹니다."
    )

st.write("")

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
<div style="text-align:center; font-size:18px; font-weight:bold; color:#712B13;">
수증기 · 이산화 탄소 · 메테인
</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# 3) 인터랙티브 확인 문제: 화살표 클릭 미션
# ---------------------------------------------------------
st.subheader("🎯 확인 문제 - 화살표를 클릭해보자!")
st.markdown("""
아래 그림은 대기가 있는 지구의 복사 평형을 나타낸 것입니다. 이 그림에는 화살표가 4개 있어요.
**대기가 생김으로 인해 새롭게 추가된 화살표**를 찾아 숫자를 클릭해보세요!
""")

# 이미지(600x600px) 안에서 각 화살표 번호가 위치한 정확한 픽셀 좌표
ARROWS = {
    "①": (144, 273),
    "②": (276, 435),
    "③": (384, 435),
    "④": (477, 168),
}
CORRECT = "③"
THRESHOLD = 65

if "quiz_last_raw" not in st.session_state:
    st.session_state.quiz_last_raw = None
if "quiz_selected" not in st.session_state:
    st.session_state.quiz_selected = None

col_img, col_reaction = st.columns([1.3, 1])

with col_img:
    coords = streamlit_image_coordinates(
        "assets/radiation_arrows_quiz.png",
        width=600,
        key="arrow_quiz",
    )

    if coords is not None and coords != st.session_state.quiz_last_raw:
        st.session_state.quiz_last_raw = coords
        best_label, best_dist = None, 10 ** 9
        for label, (ax_, ay_) in ARROWS.items():
            dist = ((coords["x"] - ax_) ** 2 + (coords["y"] - ay_) ** 2) ** 0.5
            if dist < best_dist:
                best_dist, best_label = dist, label
        st.session_state.quiz_selected = best_label if best_dist <= THRESHOLD else None
        st.rerun()

with col_reaction:
    st.write("")
    selected = st.session_state.quiz_selected

    if selected is None:
        st.markdown(
            "<p style='font-size:22px;'>👆 그림에서 숫자를 클릭해보세요!</p>",
            unsafe_allow_html=True,
        )
    else:
        # 선택한 화살표 번호를 빨간 원으로 표시한 확인용 이미지 생성
        base = Image.open("assets/radiation_arrows_quiz.png").convert("RGB")
        draw = ImageDraw.Draw(base)
        cx, cy = ARROWS[selected]
        r = 38
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(214, 39, 39), width=9)
        tmp_path = os.path.join(tempfile.gettempdir(), "ghg_quiz_marked.png")
        base.save(tmp_path)
        st.image(tmp_path, caption=f"{selected}번을 선택했어요", width=240)

        if selected == CORRECT:
            st.markdown(
                "<p style='font-size:32px; font-weight:800; color:#2E9E44; margin-top:12px;'>"
                "딩동댕~ 잘 했어! 🎉🎈</p>",
                unsafe_allow_html=True,
            )
            st.balloons()
        else:
            st.markdown(
                "<p style='font-size:32px; font-weight:800; color:#D8443C; margin-top:12px;'>"
                "다시 생각해보자~ 😢💧</p>",
                unsafe_allow_html=True,
            )
