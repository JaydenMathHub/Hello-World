import html
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("Hello World Motion Lab")
st.caption("A beginner-friendly playground for text, styles, backgrounds, and looping animations.")

# -----------------------------
# Controls
# -----------------------------
with st.sidebar:
    st.header("Customize your app")
    name = st.text_input("Enter your name", value="Hello World")

    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact", "Comic Sans MS"],
    )
    font_size = st.slider("Font size", min_value=20, max_value=110, value=52, step=2)

    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Sky", "Sunset", "Forest", "Lavender", "Ocean"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
    )
    speed = st.slider(
        "Animation speed",
        min_value=1,
        max_value=10,
        value=5,
        help="1 is slow and 10 is fast.",
    )
    bold = st.checkbox("Bold text", value=True)
    italic = st.checkbox("Italic text", value=False)

# -----------------------------
# Theme and safe text handling
# -----------------------------
themes = {
    "Light": ("#f7f8fc", "#182230", "#dbeafe"),
    "Dark": ("#10131a", "#f8fafc", "#273449"),
    "Sky": ("linear-gradient(135deg, #dff6ff, #a8d8ff)", "#10324a", "#ffffff66"),
    "Sunset": ("linear-gradient(135deg, #ffb199, #ff6a88, #7b61ff)", "#ffffff", "#ffffff33"),
    "Forest": ("linear-gradient(135deg, #0b3d2e, #1b6b4a)", "#f0fff4", "#ffffff24"),
    "Lavender": ("linear-gradient(135deg, #f3e8ff, #c4b5fd)", "#35245e", "#ffffff80"),
    "Ocean": ("linear-gradient(135deg, #042f4b, #0e7490, #67e8f9)", "#ffffff", "#ffffff30"),
}
bg, text_color, accent = themes[background]
safe_name = html.escape(name) if name.strip() else "Hello World"
font_css = "'" + font_family.replace("'", "") + "', sans-serif"
weight = "700" if bold else "400"
style = "italic" if italic else "normal"
duration = round(11 - speed, 1)

# -----------------------------
# Animation layer
# CSS animations run in the browser continuously without rerunning Streamlit.
# -----------------------------
effect_markup = ""
if effect == "Rain":
    effect_markup = '<div class="particles rain">' + "".join(
        f'<i style="--x:{(i * 37) % 100}%;--delay:{(i % 17) * -0.31}s;--dur:{1.0 + (i % 7) * 0.13}s"></i>'
        for i in range(75)
    ) + "</div>"
elif effect == "Snow":
    effect_markup = '<div class="particles snow">' + "".join(
        f'<i style="--x:{(i * 29) % 100}%;--delay:{(i % 19) * -0.7}s;--dur:{4 + (i % 8) * 0.7}s;--size:{4 + (i % 5) * 2}px"></i>'
        for i in range(48)
    ) + "</div>"
elif effect == "Hail":
    effect_markup = '<div class="particles hail">' + "".join(
        f'<i style="--x:{(i * 31) % 100}%;--delay:{(i % 13) * -0.4}s;--dur:{1.4 + (i % 6) * 0.2}s;--size:{5 + (i % 4) * 2}px"></i>'
        for i in range(42)
    ) + "</div>"
elif effect == "Wind Gust":
    effect_markup = '<div class="particles wind">' + "".join(
        f'<i style="--y:{(i * 17) % 100}%;--delay:{(i % 15) * -0.45}s;--dur:{1.8 + (i % 6) * 0.25}s"></i>'
        for i in range(24)
    ) + "</div>"
elif effect == "Confetti":
    colors = ["#ff4d6d", "#ffd166", "#06d6a0", "#4cc9f0", "#b5179e", "#ffffff"]
    effect_markup = '<div class="particles confetti">' + "".join(
        f'<i style="--x:{(i * 23) % 100}%;--delay:{(i % 21) * -0.42}s;--dur:{3 + (i % 8) * 0.45}s;--color:{colors[i % len(colors)]};--rot:{(i * 47) % 360}deg"></i>'
        for i in range(64)
    ) + "</div>"
elif effect == "Tornado":
    effect_markup = '<div class="particles tornado">' + "".join(
        f'<i style="--ring:{i % 8};--delay:{(i % 8) * -0.35}s;--dur:{2.5 + (i % 5) * 0.45}s"></i>'
        for i in range(48)
    ) + "</div>"

if name_mode == "Ticker Tape":
    name_markup = f'<div class="ticker"><div class="ticker-track"><span>{safe_name}</span><span>{safe_name}</span><span>{safe_name}</span><span>{safe_name}</span></div></div>'
elif name_mode == "Repeated":
    name_markup = '<div class="repeated">' + "".join(
        f'<span>{safe_name}</span>' for _ in range(12)
    ) + "</div>"
else:
    name_markup = f'<div class="center-name">{safe_name}</div>'

# Keep the text above the effects, while particles remain behind it.
html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
.scene {{
  position: relative; isolation: isolate; overflow: hidden;
  width: 100%; height: 600px; border-radius: 18px;
  background: {bg}; color: {text_color};
  font-family: {font_css}; padding: 28px;
}}
.scene::after {{
  content: ""; position: absolute; inset: 0; z-index: -1;
  background: radial-gradient(circle at 50% 50%, {accent}, transparent 68%);
  pointer-events: none;
}}
.particles {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; z-index: 0; }}
.center-name, .ticker, .repeated {{
  position: absolute; z-index: 2; left: 0; right: 0; top: 50%;
  transform: translateY(-50%); font-size: {font_size}px;
  font-weight: {weight}; font-style: {style}; line-height: 1.2;
  text-shadow: 0 2px 12px rgba(0,0,0,.12);
}}
.center-name {{ text-align: center; padding: 0 24px; overflow-wrap: anywhere; }}
.ticker {{ overflow: hidden; white-space: nowrap; transform: translateY(-50%); }}
.ticker-track {{ display: flex; width: max-content; gap: 1.5em; animation: ticker {max(7, 22 - speed)}s linear infinite; }}
.ticker-track span {{ white-space: nowrap; }}
@keyframes ticker {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-50%); }} }}
.repeated {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; text-align: center; padding: 20px; }}
.repeated span {{ overflow-wrap: anywhere; opacity: .92; }}
.rain i, .snow i, .hail i, .confetti i {{
  position: absolute; top: -12%; left: var(--x); display: block;
  animation: fall var(--dur, 3s) linear var(--delay, 0s) infinite;
}}
.rain i {{ width: 2px; height: 18px; background: #46a9ff; opacity: .75; border-radius: 3px; }}
.snow i {{ width: var(--size); height: var(--size); background: #fff; border-radius: 50%; opacity: .9; box-shadow: 0 0 7px #bfe9ff; animation-name: snowfall; }}
.hail i {{ width: var(--size); height: var(--size); background: #d8f3ff; border: 1px solid #8ac9e8; border-radius: 50%; box-shadow: 0 0 5px #fff; }}
.confetti i {{ width: 9px; height: 15px; background: var(--color); transform: rotate(var(--rot)); border-radius: 2px; }}
@keyframes fall {{ from {{ top: -12%; }} to {{ top: 112%; }} }}
@keyframes snowfall {{ 0% {{ top: -10%; transform: translateX(0); }} 50% {{ transform: translateX(35px); }} 100% {{ top: 110%; transform: translateX(-25px); }} }}
.wind i {{ position: absolute; left: -35%; top: var(--y); width: 38%; height: 2px; border-radius: 50%; background: rgba(255,255,255,.65); box-shadow: 0 0 8px rgba(255,255,255,.4); animation: gust var(--dur) linear var(--delay) infinite; }}
@keyframes gust {{ from {{ transform: translateX(0) skewX(-25deg); opacity: 0; }} 15% {{ opacity: .9; }} to {{ transform: translateX(390%) skewX(-25deg); opacity: 0; }} }}
.tornado i {{ position: absolute; left: 50%; top: 48%; width: calc(30px + var(--ring) * 16px); height: calc(12px + var(--ring) * 8px); border: 2px solid rgba(230,245,255,.65); border-left-color: transparent; border-radius: 50%; transform: translate(-50%, -50%); animation: spin var(--dur) linear var(--delay) infinite; }}
@keyframes spin {{ from {{ rotate: 0deg; }} to {{ rotate: 360deg; }} }}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{ animation-duration: 0.001ms !important; animation-iteration-count: 1 !important; }}
}}
</style>
</head>
<body>
  <div class="scene">
    <div class="particles">{effect_markup}</div>
    {name_markup}
  </div>
</body>
</html>
"""

components.html(html_doc, height=620, scrolling=False)

st.info(
    "Tip: Change the name, font, background, or action in the sidebar. "
    "Animations run continuously in the browser, so Streamlit does not need a rerun loop."
)
