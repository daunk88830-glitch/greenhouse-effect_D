import streamlit as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import plotly.graph_objects as go
import os

# 한글 폰트 등록: 배포 서버(Streamlit Cloud)에는 packages.txt로 설치한
# 나눔고딕 폰트가 아래 경로에 깔리므로, 그 파일을 직접 찾아서 등록합니다.
# (서버마다 폰트 설치 위치가 다를 수 있어 여러 경로를 순서대로 확인합니다)
_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
]

_font_name = "DejaVu Sans"
for _path in _FONT_CANDIDATES:
    if os.path.exists(_path):
        try:
            fm.fontManager.addfont(_path)
            _font_name = fm.FontProperties(fname=_path).get_name()
            break
        except Exception:
            continue

plt.rcParams["font.family"] = _font_name
plt.rcParams["axes.unicode_minus"] = False

st.title("🎛️ 1차시 - ② 시뮬레이션 체험")
st.caption("CO2 농도를 조절하면 대기의 재복사 에너지량이 어떻게 달라질까?")

co2 = st.slider(
    "대기 중 CO2 농도 (ppm)",
    min_value=280, max_value=1000, value=420, step=10,
    help="산업혁명 이전 대기 중 CO2 농도는 약 280ppm이었습니다."
)

st.caption(
    "※ 실제 드래그 앤 드롭(마우스로 끌어오기)은 Streamlit에서 안정적으로 구현하기 어려워, "
    "슬라이더로 CO2 농도를 직접 조절하는 방식으로 대신했어요. 슬라이더를 움직이면 "
    "그림 속 이산화 탄소 개수와 재복사 화살표 굵기가 함께 바뀝니다."
)


def draw_greenhouse(co2_ppm):
    frac = np.log(co2_ppm / 280) / np.log(1000 / 280)
    frac = max(0.0, min(1.0, frac))
    n_molecules = int(3 + frac * 12)
    line_width = 3 + 14 * frac

    fig, ax = plt.subplots(figsize=(6, 5.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off"); ax.set_aspect("equal")
    ax.add_patch(plt.Rectangle((0, 0), 10, 10, color="#EAF4FC", zorder=-1))

    ax.add_patch(plt.Circle((1.3, 9.0), 0.5, color="#F7B733", zorder=2))
    ax.add_patch(plt.Rectangle((1.0, 4.3), 8.0, 1.3, color="#CFE6F9", alpha=0.7, zorder=0))
    ax.text(1.2, 5.6, "대기", fontsize=12, color="#0C447C", weight="bold")
    ax.add_patch(plt.Rectangle((1.0, 1.0), 8.0, 1.0, color="#6FAE3E", zorder=1))
    ax.text(1.2, 1.5, "지표", fontsize=12, color="#12432F", weight="bold")

    rng = np.random.default_rng(42)
    xs = rng.uniform(1.3, 8.7, n_molecules)
    ys = rng.uniform(4.5, 5.4, n_molecules)
    labels = rng.choice(["CO2", "CH4", "H2O"], n_molecules)
    for x, y, lab in zip(xs, ys, labels):
        ax.add_patch(plt.Circle((x, y), 0.22, color="#F5D48A", alpha=0.9, zorder=3))
        ax.text(x, y, lab, fontsize=6, ha="center", va="center", zorder=4)

    ax.annotate("", xy=(3.0, 4.3), xytext=(2.0, 8.6),
                arrowprops=dict(arrowstyle="-|>", color="#FFC300", lw=3))
    ax.text(1.7, 6.7, "태양 복사\n에너지", color="#B8860B", fontsize=9, ha="center")

    ax.annotate("", xy=(5.6, 4.3), xytext=(5.3, 2.0),
                arrowprops=dict(arrowstyle="-|>", color="#F2994A", lw=2.6))
    ax.text(6.3, 3.2, "지표 방출\n(지구 복사 에너지)", color="#B15C1D", fontsize=8, ha="center")

    ax.annotate("", xy=(4.6, 2.0), xytext=(4.9, 4.3),
                arrowprops=dict(arrowstyle="-|>", color="#E63946", lw=line_width))
    ax.text(3.3, 3.2, "대기의 재복사", color="#B01F2C", fontsize=9, ha="center")

    ax.annotate("", xy=(7.8, 8.6), xytext=(7.0, 5.7),
                arrowprops=dict(arrowstyle="-|>", color="#F2994A", lw=2.6))
    ax.text(8.4, 7.2, "우주로 방출\n(지구 복사 에너지)", color="#B15C1D", fontsize=8, ha="center")

    plt.tight_layout()
    return fig


# ---------------------------------------------------------
# 과학적으로 검증된 식 사용
# IPCC 표준 CO2 복사강제력 공식: ΔF = 5.35 × ln(C/C0)  [W/m²]
# 평형 기후 민감도(ECS) 약 3℃/이산화탄소 두 배 증가 가정 → λ ≈ 0.81 K/(W/m²)
# ---------------------------------------------------------
delta_F = 5.35 * np.log(co2 / 280)
delta_T = 0.81 * delta_F
est_temp = 15 + delta_T

col1, col2 = st.columns(2)

with col1:
    st.subheader("대기 재복사 강조 그림")
    fig = draw_greenhouse(co2)
    st.pyplot(fig, use_container_width=True)
    st.metric("복사 강제력 (추정)", f"{delta_F:.2f} W/m²",
              help="대기 중 CO2가 늘어나 지구가 추가로 붙잡아두는 에너지의 양(IPCC 공식 기반)")

with col2:
    st.subheader("CO2 농도와 예상 평균 기온")
    co2_range = np.linspace(280, 1000, 100)
    temp_range = 15 + 0.81 * 5.35 * np.log(co2_range / 280)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=co2_range, y=temp_range, mode="lines",
                               line=dict(color="#D85A30", width=3), name="예상 평균 기온"))
    fig2.add_trace(go.Scatter(x=[co2], y=[est_temp], mode="markers",
                               marker=dict(size=14, color="#791F1F"), name="현재 설정"))
    fig2.update_layout(
        xaxis_title="CO2 농도 (ppm)", yaxis_title="예상 평균 기온 (℃)",
        height=420, margin=dict(l=10, r=10, t=30, b=10),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.metric("예상 평균 기온", f"{est_temp:.1f} ℃")

with st.expander("🔬 이 그래프의 계산식이 궁금하다면"):
    st.markdown("""
    - **복사강제력(radiative forcing)** 계산에는 IPCC가 실제로 사용하는 근사식을 그대로 썼습니다.

      $$\\Delta F = 5.35 \\times \\ln\\left(\\frac{C}{C_0}\\right) \\text{ [W/m}^2\\text{]}$$

      ($C$: 현재 CO2 농도, $C_0$ = 280ppm, 산업혁명 이전 농도)
    - CO2가 두 배가 되면(280→560ppm) 복사강제력은 약 3.7 W/m² 늘어나고, 이때 평형 기후
      민감도(equilibrium climate sensitivity)를 약 3℃로 가정하면 λ ≈ 0.81 K/(W/m²)이 됩니다.
    - 즉 이 그래프의 곡선은 실제 기후과학에서 쓰는 단순화된 근사 모델이며, 실제 지구는
      해양·구름·빙하 반사 등 다양한 되먹임 작용이 얽혀 있어 더 복잡합니다.
    """)

st.caption("※ 위 모델은 온실효과의 방향성과 크기를 이해하기 위한 단순화된 교육용 근사식입니다.")

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
        st.error("다시 생각해볼까요? 슬라이더를 움직여 재복사 화살표가 어떻게 변하는지 다시 확인해보세요.")

reason = st.text_area("왜 그렇게 생각했는지 한 문장으로 써보세요.", height=80)
