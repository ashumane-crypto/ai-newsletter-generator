import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime
import base64
import streamlit.components.v1 as components

# ---------------- CONFIG ---------------- #
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="AI Newsletter Generator",
    page_icon="📰",
    layout="wide"
)

# ---------------- LOAD LOGO ---------------- #
with open("assets/logo.jpg", "rb") as f:
    LOGO_BASE64 = base64.b64encode(f.read()).decode()

# ---------------- HEADER ---------------- #
st.markdown(
    f"""
    <div style="display:flex;align-items:center;gap:15px;">
        <img src="data:image/png;base64,{LOGO_BASE64}" height="60">
        <h1 style="margin:0;">NEWSLETTER</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------------- INPUT SECTION ---------------- #
st.subheader("✏ Newsletter Details")

col1, col2, col3 = st.columns(3)
with col1:
    headline = st.text_input("Headline", "Welcome Back to a New School Year!")

with col2:
    location = st.text_input("Location", "Sangli, Maharashtra")

with col3:
    author = st.text_input("Author", "Sadaf Mujawar")

story = st.text_area(
    "📝 Story Context",
    height=160,
    placeholder="Explain what the newsletter is about..."
)

highlights = st.text_area(
    "📌 Highlights (one per line)",
    height=120,
    placeholder="School reopens\nNew teachers appointed\nSmart classrooms launched"
)

uploaded_image = st.file_uploader(
    "🖼 Upload Header Image",
    type=["jpg", "jpeg", "png"]
)

# ---------------- THEME ---------------- #
theme = st.selectbox(
    "🎨 Select Theme",
    ["Light Blue", "Warm Yellow", "Classic Gray"]
)

THEMES = {
    "Light Blue": {"left": "#f0f7ff", "right": "#e8f1ff", "accent": "#1f4e79"},
    "Warm Yellow": {"left": "#fff7e6", "right": "#fff0cc", "accent": "#a86f00"},
    "Classic Gray": {"left": "#f5f5f5", "right": "#ededed", "accent": "#333333"},
}
colors = THEMES[theme]

generate = st.button("✨ Generate Newsletter", use_container_width=True)

# ---------------- AI GENERATION ---------------- #
article = ""
if generate and story.strip():
    with st.spinner("Gemini AI is writing your newsletter..."):
        prompt = f"""
Write a professional school newsletter.
Plain text only.
180–220 words.
Formal and friendly tone.

Headline: {headline}
Location: {location}
Author: {author}

Context:
{story}
"""
        model = genai.GenerativeModel("models/gemma-3-1b-it")
        response = model.generate_content(prompt)
        article = response.text.strip()

# ---------------- OUTPUT ---------------- #
if article:
    hero_html = ""
    if uploaded_image:
        encoded = base64.b64encode(uploaded_image.read()).decode()
        hero_html = f"""
        <div class="hero">
            <img src="data:image/png;base64,{encoded}">
        </div>
        """

    highlights_html = "".join(
        f"<li>{h}</li>" for h in highlights.splitlines() if h.strip()
    )

    newsletter_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{
    font-family: Arial;
    background:#f4f6f8;
}}

.wrapper {{
    max-width:1100px;
    margin:auto;
    background:white;
    padding:26px;
    border-radius:16px;
    box-shadow:0 20px 45px rgba(0,0,0,0.12);
}}

.print-btn {{
    text-align:center;
    margin-bottom:10px;
}}

button {{
    padding:10px 22px;
    font-size:15px;
    background:#2563eb;
    color:white;
    border:none;
    border-radius:8px;
    cursor:pointer;
}}

.top-header {{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:12px;
}}

.brand {{
    display:flex;
    align-items:center;
    gap:12px;
}}

.brand img {{
    height:60px;
}}

.brand h1 {{
    font-size:40px;
    margin:0;
    letter-spacing:2px;
}}

.meta {{
    font-size:14px;
    color:#555;
    text-align:right;
}}

.hero {{
    margin:12px 0 18px 0;
}}

.hero img {{
    width:100%;
    height:500px;
    object-fit:cover;
    border-radius:14px;
}}

.content {{
    display:flex;
    gap:22px;
}}

.left {{
    flex:2;
    background:{colors['left']};
    padding:22px;
    border-radius:14px;
}}

.right {{
    flex:1;
    background:{colors['right']};
    padding:22px;
    border-radius:14px;
}}

.article {{
    font-size:16px;
    line-height:1.75;
    color:#222;
}}

h2 {{
    color:{colors['accent']};
    margin-top:0;
    margin-bottom:6px;
}}

@media print {{
    .print-btn {{
        display:none;
    }}
    body {{
        background:white;
    }}
}}
</style>
</head>

<body>

<div class="print-btn">
    <button onclick="window.print()">📄 Download PDF</button>
</div>

<div class="wrapper">

    <!-- TOP TITLE -->
    <div class="top-header">
        <div class="brand">
            <img src="data:image/png;base64,{LOGO_BASE64}">
            <h1>NEWSLETTER</h1>
        </div>
        <div class="meta">
            <b>{author}</b><br>
            {datetime.now().strftime("%d %B %Y")}
        </div>
    </div>

    <!-- IMAGE -->
    {hero_html}

    <!-- CONTENT -->
    <div class="content">
        <div class="left">
            <h2>{headline}</h2>
            <b>{location}</b><br><br>
            <div class="article">
                {article.replace(chr(10), "<br><br>")}
            </div>
        </div>

        <div class="right">
            <h3>📌 Highlights</h3>
            <ul>{highlights_html}</ul>
        </div>
    </div>

</div>

</body>
</html>
"""

    components.html(newsletter_html, height=980, scrolling=True)

# ---------------- FOOTER ---------------- #
st.markdown(
    "<hr><center style='color:gray'>AI Newsletter Generator • Streamlit + Gemini</center>",
    unsafe_allow_html=True
)
