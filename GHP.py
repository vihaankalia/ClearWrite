import streamlit as st
import requests
import base64

# ---------------- OPENROUTER CONFIG ----------------
API_KEY = "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"
MODEL = "google/gemini-2.5-flash-preview-09-2025"

def simplify_text(text):
    """
    Send text to OpenRouter API using Gemini 2.5 Flash Preview to simplify.
    """
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": f"Simplify this text so it is clear and easy to read:\n\n{text}"}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

        if response.status_code != 200:
            return f"Error simplifying text: {response.status_code} - {response.text}"

        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Exception simplifying text: {e}"

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
    background-color: #000000;
    font-family: 'Yeezy', Helvetica, Arial, sans-serif;
}}

.title {{
    font-size: 48px;
    font-weight: 300;
    color: #ffffff;
    text-align: center;
    letter-spacing: 12px;
    text-transform: uppercase;
    margin-bottom: 0;
}}

.subtitle {{
    font-size: 18px;
    color: #ffffff;
    text-align: center;
    margin-bottom: 30px;
    font-family: 'Yeezy', Helvetica, Arial, sans-serif;
}}

textarea {{
    border-radius: 12px;
    border: none;
    padding: 18px;
    font-size: 18px;
    background-color: #ffffff;
    color: #000000;
    width: 100%;
    box-sizing: border-box;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    font-family: 'Yeezy', Helvetica, Arial, sans-serif;
}}

.simplified-box {{
    border-left: 6px solid #000000;
    padding: 18px;
    background-color: #ffffff;
    font-size: 18px;
    color: #000000;
    border-radius: 12px;
    margin-top: 20px;
    white-space: pre-wrap;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    font-family: 'Yeezy', Helvetica, Arial, sans-serif;
}}

.footer {{
    font-size: 12px;
    color: #aaaaaa;
    text-align: center;
    margin-top: 40px;
}}

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
st.markdown('<div class="footer">Made by Vihaan Kalia</div>', unsafe_allow_html=True)

