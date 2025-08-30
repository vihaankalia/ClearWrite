# -------- Install first --------
# pip install streamlit google-genai

import streamlit as st
from google import genai

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

# ----- CUSTOM CSS -----
st.markdown("""
    <style>
    /* Background */
    .stApp {
        background-color: #000000;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* Title */
    .title {
        font-size: 48px;
        font-weight: 300;
        color: #fffbe6;
        text-align: center;
        letter-spacing: 12px;
        text-transform: uppercase;
        margin-bottom: 0;
    }

    /* Subtitle */
    .subtitle {
        font-size: 18px;
        color: #aaaaaa;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Text area */
    textarea {
        border-radius: 8px;
        border: 1px solid #333333;
        padding: 15px;
        font-size: 16px;
        background-color: #111111;
        color: #ffffff;
        width: 100%;
        box-sizing: border-box;
    }

    /* Simplified text box */
    .simplified-box {
        border-left: 4px solid #f5d95e;
        padding: 15px;
        background-color: #111111;
        font-size: 16px;
        color: #ffffff;
        border-radius: 6px;
        margin-top: 15px;
        white-space: pre-wrap;
    }

    /* Footer text */
    .footer {
        font-size: 12px;
        color: #777777;
        text-align: center;
        margin-top: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# ----- TITLE AND DESCRIPTION -----
st.markdown('<div class="title">C L E A R W R I T E</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Paste text below and simplify it instantly.</div>', unsafe_allow_html=True)

# ----- INITIALIZE SESSION STATE -----
if "user_text" not in st.session_state:
    st.session_state.user_text = ""

# ----- TEXT INPUT AREA -----
st.session_state.user_text = st.text_area("", value=st.session_state.user_text, height=200)

# ----- CENTERED SIMPLIFY BUTTON -----
col1, col2, col3 = st.columns([1.15, 0.6, 1])
simplified = None
with col2:
    if st.button("Simplify Text"):
        if st.session_state.user_text.strip() == "":
            st.warning("Please enter some text first.")
        else:
            with st.spinner("Simplifying..."):
                simplified = simplify_text(st.session_state.user_text)

# ----- CLEAR BUTTON IN MANUAL COLUMN (ADJUSTABLE) -----
# Change col3 to col2 or col4 to shift it left/right
col1, col2, col3, col4, col5 = st.columns([1.11, 0.4, 0.4, 0.4, 1])
with col3:
    if st.button("Clear", key="clear_button"):
        st.session_state.user_text = ""

# ----- DISPLAY SIMPLIFIED TEXT CENTERED -----
if simplified:
    st.subheader("Simplified Text")
    st.markdown(f'<div class="simplified-box">{simplified}</div>', unsafe_allow_html=True)

# ----- FOOTER -----
st.markdown('<div class="footer">Made by Vihaan Kalia | Uses Gemini API</div>', unsafe_allow_html=True)
