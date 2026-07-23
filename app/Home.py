import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="DataMind",
    page_icon="🤖",
    layout="wide"
)

# ── PASSWORD PROTECTION ──
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.title("🤖 DataMind")
    st.markdown("*Autonomous Data Intelligence Agent*")
    st.divider()

    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.markdown("### Enter Access Password")
        password = st.text_input("Password", type="password", placeholder="Enter password...")
        if st.button("Access DataMind", use_container_width=True):
            if password == os.getenv("APP_PASSWORD"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Slide into my DMs on LinkedIn to request access.")
        st.markdown("---")
        st.markdown("**Built by Vedant Thakur**")
        st.markdown("[LinkedIn](https://linkedin.com/in/vedantthakur02) · [GitHub](https://github.com/Vedant2022)")

    return False

if not check_password():
    st.stop()

# ── SIDEBAR (only shown after login) ──
with st.sidebar:
    st.title("🤖 DataMind")
    st.markdown("*Autonomous Data Intelligence Agent*")
    st.divider()
    page = st.radio(
        "Navigate",
        ["Dashboard", "Chat with your data"],
        label_visibility="collapsed"
    )
    st.divider()
    st.markdown("**Built by Vedant Thakur**")
    st.markdown("MSc Data Science · NTU")
    st.markdown("[GitHub](https://github.com/Vedant2022/datamind-agent)")
    if st.button("🔒 Logout"):
        st.session_state.authenticated = False
        st.rerun()

# ── ROUTING ──
import importlib.util
import sys
sys.path.insert(0, '/home/vedantroot/projects/datamind-agent')
if page == "Dashboard":
    from app import _Dashboard as Dashboard
    Dashboard.show()
elif page == "Chat with your data":
    from app import _Chat as Chat
    Chat.show()