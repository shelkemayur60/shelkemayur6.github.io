"""
SafeCheck — Personal Data Leak Detector
A premium-looking Streamlit web app to check password breaches
and analyze password strength, built on the HIBP k-anonymity API.

Run with: streamlit run app.py
"""

import streamlit as st
from leak_detector_core import check_password_breach, analyze_password_strength

st.set_page_config(
    page_title="SafeCheck | Data Leak Detector",
    page_icon="🛡️",
    layout="centered",
)

# ---------- Custom CSS for a premium look ----------
st.markdown(
    """
    <style>
    .main {
        background-color: #0f1117;
    }
    .stApp {
        background: linear-gradient(135deg, #0f1117 0%, #1a1d29 100%);
    }
    h1 {
        font-weight: 800;
        background: linear-gradient(90deg, #6366f1, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        color: #9ca3af;
        font-size: 16px;
        margin-bottom: 30px;
    }
    div[data-testid="stTextInput"] input {
        border-radius: 10px;
        border: 1px solid #374151;
        background-color: #1f2330;
        color: white;
    }
    .result-card {
        padding: 20px;
        border-radius: 14px;
        margin-top: 15px;
    }
    .safe {
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid #10b981;
    }
    .danger {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
    }
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 13px;
        margin-top: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown("<h1>🛡️ SafeCheck</h1>", unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Personal Data Leak Detector — check if your password '
    "has been exposed in a known data breach, privately and securely.</p>",
    unsafe_allow_html=True,
)

# ---------- Input ----------
password = st.text_input("Enter a password to check", type="password")
check_clicked = st.button("🔍 Check Now", use_container_width=True)

if check_clicked:
    if not password:
        st.warning("Please enter a password first.")
    else:
        with st.spinner("Checking against breach database..."):
            try:
                breach_count = check_password_breach(password)
            except Exception:
                breach_count = None

        strength = analyze_password_strength(password)

        # --- Breach result ---
        if breach_count is None:
            st.error("Could not reach the breach database. Check your internet connection.")
        elif breach_count > 0:
            st.markdown(
                f"""
                <div class="result-card danger">
                    <h3>⚠️ Password Compromised!</h3>
                    <p>This password has appeared in <b>{breach_count:,}</b> known data breaches.
                    Do NOT use it — change it immediately wherever it's used.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="result-card safe">
                    <h3>✅ No Breach Found</h3>
                    <p>This password was not found in any known data breach.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # --- Strength result ---
        st.markdown("### 💪 Password Strength")
        st.progress(strength["score"] / 5)
        st.write(f"**Rating:** {strength['label']} ({strength['score']}/5)")

        if strength["issues"]:
            st.write("**Suggestions to improve:**")
            for issue in strength["issues"]:
                st.write(f"- {issue}")
        else:
            st.write("Tumcha password already strong ahe! 🎉")

# ---------- Footer ----------
st.markdown(
    '<p class="footer">🔒 Privacy-first: only a hash prefix is sent over the network. '
    "Your real password never leaves your device. Powered by the HIBP k-anonymity API.</p>",
    unsafe_allow_html=True,
)
