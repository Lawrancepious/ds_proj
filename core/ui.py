"""Shared look & feel: animated CSS, hero banners, footer."""
from __future__ import annotations

import streamlit as st

RED = "#E63946"

_CSS = """
<style>
/* ---------- keyframes ---------- */
@keyframes fadeUp   { from {opacity:0; transform:translateY(18px)} to {opacity:1; transform:none} }
@keyframes slideIn  { from {opacity:0; transform:translateX(-14px)} to {opacity:1; transform:none} }
@keyframes gradient { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
@keyframes float    { 0%,100%{transform:translateY(0) rotate(-4deg)} 50%{transform:translateY(-10px) rotate(4deg)} }
@keyframes shine    { from {left:-60%} to {left:130%} }
@keyframes pulse    { 0%,100%{box-shadow:0 0 0 0 rgba(230,57,70,.45)} 50%{box-shadow:0 0 0 10px rgba(230,57,70,0)} }

/* ---------- page chrome ---------- */
[data-testid="stDecoration"] {
  background: linear-gradient(90deg,#9D0208,#E63946,#FF8FA3,#E63946,#9D0208);
  background-size: 300% 100%; animation: gradient 6s ease infinite; height: 4px;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stMainBlockContainer"] { padding-top: 2.5rem; animation: fadeUp .55s ease-out both; }
[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#22070C 0%,#170D0F 45%,#120A0C 100%);
}
[data-testid="stSidebarNav"] a { border-radius: .6rem; transition: background .2s, transform .2s; }
[data-testid="stSidebarNav"] a:hover { transform: translateX(4px); background: rgba(230,57,70,.15); }
[data-testid="stSidebarNav"] a[aria-current="page"] { background: rgba(230,57,70,.22); }

/* ---------- hero banner ---------- */
.hero {
  position: relative; overflow: hidden; border-radius: 1.25rem;
  padding: 2rem 2.25rem; margin-bottom: 1.5rem;
  background: linear-gradient(120deg,#5A0710,#B3121F,#E63946,#B3121F,#5A0710);
  background-size: 300% 300%; animation: gradient 10s ease infinite, fadeUp .6s ease-out both;
  box-shadow: 0 12px 40px -12px rgba(230,57,70,.55);
}
.hero::after {           /* light sweep across the banner */
  content:""; position:absolute; top:0; left:-60%; width:40%; height:100%;
  background: linear-gradient(100deg,transparent,rgba(255,255,255,.18),transparent);
  animation: shine 4.5s ease-in-out infinite;
}
.hero .icon  { font-size: 3rem; display:inline-block; animation: float 4s ease-in-out infinite; }
.hero h1     { color:#fff !important; margin:.25rem 0 .35rem; font-size:2.3rem; font-weight:700; padding:0; }
.hero p      { color:rgba(255,255,255,.88); margin:0; font-size:1.05rem; max-width:52rem; }
.hero .badge { display:inline-block; margin-top:.9rem; margin-right:.4rem; padding:.2rem .75rem;
               border-radius:999px; background:rgba(255,255,255,.16); color:#fff; font-size:.8rem;
               backdrop-filter: blur(4px); }

/* ---------- cards / metrics ---------- */
[data-testid="stMetric"] {
  background: linear-gradient(160deg,#21141A,#170E11); border:1px solid #3A2328;
  border-left: 4px solid #E63946; border-radius: .9rem; padding: .9rem 1.1rem;
  transition: transform .25s ease, box-shadow .25s ease, border-color .25s;
  animation: fadeUp .6s ease-out both;
}
[data-testid="stMetric"]:hover {
  transform: translateY(-4px); border-color:#E63946;
  box-shadow: 0 10px 28px -10px rgba(230,57,70,.6);
}
[data-testid="stMetricValue"] { color:#FF6B78; font-weight:700; }
[data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] { animation-delay:.08s; }
[data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"] { animation-delay:.16s; }
[data-testid="stColumn"]:nth-child(4) [data-testid="stMetric"] { animation-delay:.24s; }
[data-testid="stColumn"]:nth-child(5) [data-testid="stMetric"] { animation-delay:.32s; }

/* bordered containers (st.container(border=True)) */
[data-testid="stVerticalBlockBorderWrapper"], [data-testid="stVerticalBlock"][class*="border"] {
  transition: transform .3s ease, box-shadow .3s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
  transform: translateY(-4px); box-shadow: 0 14px 36px -14px rgba(230,57,70,.5);
}
[data-testid="stImage"] { overflow: hidden; border-radius: .9rem; }
[data-testid="stImageContainer"] { width: 100% !important; }
[data-testid="stImage"] img { border-radius: .9rem; height: 200px !important; width: 100% !important; object-fit: cover;
                              transition: transform .5s ease; }
[data-testid="stImage"]:hover img { transform: scale(1.03); }

/* charts sit on soft cards */
[data-testid="stPlotlyChart"] {
  background:#160E10; border:1px solid #2E1B20; border-radius:1rem; padding:.4rem;
  animation: fadeUp .7s ease-out both; transition: border-color .3s, box-shadow .3s;
}
[data-testid="stPlotlyChart"]:hover { border-color:#5A2A32; box-shadow:0 8px 26px -14px rgba(230,57,70,.5); }

/* ---------- buttons ---------- */
.stButton > button, .stDownloadButton > button, [data-testid="stPageLink"] a {
  transition: transform .18s ease, box-shadow .25s ease, background .25s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  transform: translateY(-2px) scale(1.02); border-color:#E63946; color:#fff;
  box-shadow: 0 8px 22px -8px rgba(230,57,70,.7);
}
.stButton > button:active { transform: scale(.97); }
.stButton > button[kind="primary"] {
  background: linear-gradient(120deg,#B3121F,#E63946,#FF6B78); background-size:200% 200%;
  border:none; animation: gradient 5s ease infinite, pulse 2.4s infinite;
}
[data-testid="stPageLink"] a { border-radius:.7rem; }
[data-testid="stPageLink"] a:hover { transform: translateX(6px); background: rgba(230,57,70,.12); }

/* ---------- tabs ---------- */
[data-baseweb="tab-list"] { gap: .35rem; }
[data-baseweb="tab"] { border-radius:.6rem .6rem 0 0; padding:.4rem 1rem; transition: background .2s, color .2s; }
[data-baseweb="tab"]:hover { background: rgba(230,57,70,.12); color:#FF6B78; }
[data-baseweb="tab-highlight"] { background:#E63946; height:3px; transition: all .35s cubic-bezier(.4,0,.2,1); }
[data-baseweb="tab-panel"] { animation: fadeUp .45s ease-out both; }

/* ---------- chat ---------- */
[data-testid="stChatMessage"] {
  border-radius: 1rem; border:1px solid #2E1B20; background:#170E11; animation: slideIn .4s ease-out both;
}
[data-testid="stChatInput"] { border-radius: 1rem; }
[data-testid="stChatInput"]:focus-within { box-shadow: 0 0 0 2px rgba(230,57,70,.55); }

/* ---------- misc ---------- */
hr { border-color:#3A2328 !important; }
.ai-card { border:1px solid #5A2A32; border-radius:1rem; padding:1rem 1.25rem; animation: fadeUp .5s ease-out both;
           background: linear-gradient(160deg,rgba(230,57,70,.10),rgba(230,57,70,.02)); }
.footer  { text-align:center; color:#9A8A8D; font-size:.85rem; padding:2.5rem 0 .5rem; }
.footer .heart { color:#E63946; display:inline-block; animation: pulse 1.6s infinite; border-radius:50%; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
}
</style>
"""


def setup() -> None:
    """Inject the global stylesheet (call once from app.py, before the page runs)."""
    st.html(_CSS)


def hero(title: str, subtitle: str, icon: str, badges: list[str] | None = None) -> None:
    """Animated red gradient banner used at the top of every page."""
    chips = "".join(f'<span class="badge">{b}</span>' for b in badges or [])
    st.markdown(
        f'<div class="hero"><span class="icon">{icon}</span><h1>{title}</h1>'
        f"<p>{subtitle}</p>{chips}</div>",
        unsafe_allow_html=True,
    )


def footer() -> None:
    st.markdown(
        '<div class="footer">Built with Streamlit, scikit-learn &amp; Google Gemini · '
        'made with <span class="heart">❤</span></div>',
        unsafe_allow_html=True,
    )
