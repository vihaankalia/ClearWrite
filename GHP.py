# -------- Install first --------
# pip install streamlit google-genai

import streamlit as st
from google import genai
import base64

# ---------------- GEMINI CLIENT ----------------
API_KEY = "AIzaSyBWlShnCteDlZ4JVfk8Oaoci-wxMR08r-w"
client = genai.Client(api_key=API_KEY)

def simplify_text(text):
    """
    Send text to Gemini API to simplify.
    """
    prompt = f"Simplify this text so it is clear and easy to read:\n\n{text}"
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    return getattr(response, "text", getattr(response, "output_text", "Error: no text returned"))

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="ClearWrite", page_icon="🖋️", layout="centered")

# ----- EMBED YEEZY FONT -----
with open("yeezy.ttf", "rb") as f:
    font_data = f.read()
    font_base64 = base64.b64encode(font_data).decode()

st.markdown(f"""
<style>
@font-face {{
    font-family: 'Yeezy';
    src: url(data:font/ttf;base64,{font_base64}) format('truetype');
    font-weight: normal;
    font-style: normal;
}}

.stApp {{
    background-color: #000000; /* Dark mode background */
    font-family: 'Yeezy', Helvetica, Arial, sans-serif;
}}

/* Title */
.title {{
    font-size: 48px;
    font-weight: 300;
    color: #ffffff;
    text-align: center;
    letter-spacing: 12px;
    text-transform: uppercase;
    margin-bottom: 0;
}}

/* Subtitle */
.subtitle {{
    font-size: 18px;
    color: #ffffff;
    text-align: center;
    margin-bottom: 30px;
    font-family: 'Yeezy', Helvetica, Arial, sans-serif;
}}

/* Text area */
textarea {{
    border-radius: 12px;
    border: none;
    padding: 18px;
    font-size: 18px;
    background-color: #ffffff; /* Always white */
    color: #000000; /* Black text */
    width: 100%;
    box-sizing: border-box;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    font-family: 'Yeezy', Helvetica, Arial, sans-serif;
}}

/* Simplified text box */
.simplified-box {{
    border-left: 6px solid #000000;
    padding: 18px;
    background-color: #ffffff; /* Always white */
    font-size: 18px;
    color: #000000;
    border-radius: 12px;
    margin-top: 20px;
    white-space: pre-wrap;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    font-family: 'Yeezy', Helvetica, Arial, sans-serif;
}}

/* Footer */
.footer {{
    font-size: 12px;
    color: #aaaaaa;
    text-align: center;
    margin-top: 40px;
}}

/* Simplify Button */
.stButton>button {{
    background-color: #ffffff;
    color: #000000;
    border-radius: 12px;
    padding: 10px 30px;
    font-size: 16px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 2px;
    transition: all 0.2s ease;
    cursor: pointer;
    font-family: 'Yeezy', Helvetica, Arial, sans-serif;
}}
.stButton>button:hover {{
    opacity: 0.85;
}}
</style>
""", unsafe_allow_html=True)

# ----- TITLE AND DESCRIPTION -----
st.markdown('<div class="title">C L E A R W R I T E</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Paste text below and simplify it instantly.</div>', unsafe_allow_html=True)

# ----- INITIALIZE SESSION STATE -----
if "user_text" not in st.session_state:
    st.session_state.user_text = ""

# ----- TEXT INPUT AREA -----
st.session_state.user_text = st.text_area("", value=st.session_state.user_text, height=220)

# ----- CENTERED SIMPLIFY BUTTON -----
col1, col2, col3 = st.columns([1.5, 1, 1.5])
simplified = None
with col2:
    if st.button("Simplify Text"):
        if st.session_state.user_text.strip() == "":
            st.warning("Please enter some text first.")
        else:
            with st.spinner("Simplifying..."):
                simplified = simplify_text(st.session_state.user_text)

# ----- DISPLAY SIMPLIFIED TEXT CENTERED -----
if simplified:
    st.subheader("Simplified Text")
    st.markdown(f'<div class="simplified-box">{simplified}</div>', unsafe_allow_html=True)

# ----- FOOTER -----
st.markdown('<div class="footer">Made by Vihaan Kalia | Uses Gemini API</div>', unsafe_allow_html=True)
