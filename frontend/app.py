import streamlit as st
import requests
import pandas as pd
import io
import time

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LogLens · AI Log Classifier",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

import os
API_BASE = os.environ.get("API_BASE", "http://localhost:8000")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global reset ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Gradient background ── */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        min-height: 100vh;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Hero banner ── */
    .hero {
        text-align: center;
        padding: 3.5rem 1rem 2.5rem;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(139, 92, 246, 0.2);
        border: 1px solid rgba(139, 92, 246, 0.5);
        color: #c4b5fd;
        padding: 0.35rem 1.1rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }
    .hero h1 {
        font-size: 3.4rem;
        font-weight: 800;
        line-height: 1.15;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 1rem;
    }
    .hero p {
        color: #94a3b8;
        font-size: 1.15rem;
        max-width: 580px;
        margin: 0 auto 2rem;
        line-height: 1.7;
    }

    /* ── Stat pills ── */
    .stat-row {
        display: flex;
        justify-content: center;
        gap: 1.2rem;
        flex-wrap: wrap;
        margin-bottom: 2.5rem;
    }
    .stat-pill {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 0.7rem 1.4rem;
        color: #e2e8f0;
        font-size: 0.88rem;
        font-weight: 500;
    }
    .stat-pill span {
        font-weight: 700;
        color: #a78bfa;
    }

    /* ── Glass card ── */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
    }
    .card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
    }
    .card-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    .icon-purple { background: rgba(139, 92, 246, 0.2); }
    .icon-blue   { background: rgba(59, 130, 246, 0.2); }
    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 0;
    }
    .card-sub {
        font-size: 0.82rem;
        color: #64748b;
        margin: 0;
    }

    /* ── Result badge ── */
    .result-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, rgba(52,211,153,0.15), rgba(59,130,246,0.15));
        border: 1px solid rgba(52,211,153,0.3);
        border-radius: 999px;
        padding: 0.5rem 1.2rem;
        color: #34d399;
        font-weight: 700;
        font-size: 1.05rem;
        margin-top: 0.5rem;
    }

    /* ── Divider ── */
    .gradient-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139,92,246,0.5), transparent);
        margin: 2rem 0;
    }

    /* ── Streamlit widget overrides ── */
    div[data-testid="stFileUploader"] {
        border: 2px dashed rgba(139,92,246,0.4) !important;
        border-radius: 14px !important;
        background: rgba(139,92,246,0.05) !important;
        padding: 1rem !important;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: rgba(139,92,246,0.8) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.6rem !important;
        font-size: 0.95rem !important;
        transition: transform 0.15s, box-shadow 0.15s !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(124,58,237,0.4) !important;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669, #0d9488) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.6rem !important;
        font-size: 0.95rem !important;
        width: 100% !important;
    }
    /* Inputs — dark bg so light text is readable */
    .stTextInput > div > div > input {
        background: #1e1b4b !important;
        border: 1px solid rgba(139,92,246,0.35) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTextInput > div > div > input::placeholder { color: #64748b !important; }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background: #1e1b4b !important;
        border: 1px solid rgba(139,92,246,0.35) !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        color: #e2e8f0 !important;
        background: transparent !important;
    }
    /* Selectbox dropdown menu items */
    ul[data-baseweb="menu"] { background: #1e1b4b !important; border: 1px solid rgba(139,92,246,0.3) !important; }
    ul[data-baseweb="menu"] li { color: #e2e8f0 !important; }
    ul[data-baseweb="menu"] li:hover { background: rgba(139,92,246,0.2) !important; }

    /* Textarea */
    .stTextArea > div > div > textarea {
        background: #1e1b4b !important;
        border: 1px solid rgba(139,92,246,0.35) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTextArea > div > div > textarea::placeholder { color: #64748b !important; }

    /* Widget labels */
    label, p { color: #94a3b8 !important; font-size: 0.88rem !important; }

    /* st.metric — label and value */
    div[data-testid="stMetric"] label,
    div[data-testid="stMetricLabel"] p,
    div[data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 0.82rem !important; }
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricValue"] { color: #f1f5f9 !important; font-size: 1.6rem !important; font-weight: 700 !important; }

    /* File-uploader label text */
    div[data-testid="stFileUploader"] p,
    div[data-testid="stFileUploader"] span { color: #94a3b8 !important; }

    /* ── DataFrame ── */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* ── Alert overrides ── */
    div[data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    /* ── Step chips ── */
    .steps {
        display: flex;
        gap: 0.8rem;
        margin-bottom: 1.2rem;
        flex-wrap: wrap;
    }
    .step {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 8px;
        padding: 0.4rem 0.8rem;
        color: #94a3b8;
        font-size: 0.82rem;
    }
    .step-num {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: linear-gradient(135deg,#7c3aed,#4f46e5);
        color: white;
        font-size: 0.7rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">⚡ Powered by BERT · Regex · LLM</div>
        <h1>LogLens<br>AI Log Classifier</h1>
        <p>
            Instantly classify system logs at scale using a hybrid NLP pipeline.
            Upload a CSV for bulk predictions or test a single entry in real time.
        </p>
        <div class="stat-row">
            <div class="stat-pill">🔍 <span>3-Stage</span> Classification Pipeline</div>
            <div class="stat-pill">📄 <span>CSV</span> Bulk Upload &amp; Download</div>
            <div class="stat-pill">⚡ <span>Real-time</span> Single Prediction</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Layout: two columns ───────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

# ════════════════════════════════════════════════════════════════════════════════
# LEFT COLUMN — Bulk CSV Prediction
# ════════════════════════════════════════════════════════════════════════════════
with col_left:
    st.markdown(
        """
        <div class="glass-card">
          <div class="card-header">
            <div class="card-icon icon-purple">📂</div>
            <div>
              <p class="card-title">Bulk CSV Prediction</p>
              <p class="card-sub">Upload a CSV → classify all rows → download results</p>
            </div>
          </div>
          <div class="steps">
            <div class="step"><div class="step-num">1</div>Upload CSV</div>
            <div class="step"><div class="step-num">2</div>Run Classifier</div>
            <div class="step"><div class="step-num">3</div>Download Output</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Drop your CSV here (must have **source** & **log_message** columns)",
        type=["csv"],
        key="bulk_uploader",
    )

    if uploaded_file:
        preview_df = pd.read_csv(uploaded_file)
        uploaded_file.seek(0)  # reset pointer for later use

        st.markdown("**Preview — first 5 rows**")
        st.dataframe(preview_df.head(5), use_container_width=True, height=200)

        if st.button("🚀  Run Bulk Classification", key="btn_bulk"):
            with st.spinner("Classifying logs… this may take a moment"):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                    resp = requests.post(f"{API_BASE}/classify/", files=files, timeout=120)

                    if resp.status_code == 200:
                        result_df = pd.read_csv(io.StringIO(resp.text))
                        st.success(f"✅  Classification complete — **{len(result_df)}** rows processed")

                        # ── Results table ──
                        st.markdown("**Results**")
                        st.dataframe(result_df, use_container_width=True, height=280)

                        # ── Download button ──
                        csv_bytes = result_df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            label="⬇️  Download Output CSV",
                            data=csv_bytes,
                            file_name="classified_logs.csv",
                            mime="text/csv",
                            key="download_btn",
                        )
                    else:
                        detail = resp.json().get("detail", resp.text)
                        st.error(f"❌  Server error {resp.status_code}: {detail}")
                except requests.exceptions.ConnectionError:
                    st.error("❌  Cannot connect to the API. Make sure `server.py` is running on port 8000.")
                except Exception as ex:
                    st.error(f"❌  Unexpected error: {ex}")


# ════════════════════════════════════════════════════════════════════════════════
# RIGHT COLUMN — Single Log Prediction
# ════════════════════════════════════════════════════════════════════════════════
with col_right:
    st.markdown(
        """
        <div class="glass-card">
          <div class="card-header">
            <div class="card-icon icon-blue">🔬</div>
            <div>
              <p class="card-title">Single Log Prediction</p>
              <p class="card-sub">Test one log entry and see the predicted label instantly</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    SOURCE_OPTIONS = [
        "ModernCRM",
        "BillingSystem",
        "AnalyticsEngine",
        "ModernHR",
        "LegacyCRM",
    ]

    source = st.selectbox("Source System", options=SOURCE_OPTIONS, key="single_source")
    log_message = st.text_area(
        "Log Message",
        placeholder='e.g.  "IP 192.168.1.45 blocked due to potential attack"',
        height=130,
        key="single_log",
    )

    if st.button("⚡  Predict Label", key="btn_single"):
        if not log_message.strip():
            st.warning("⚠️  Please enter a log message before predicting.")
        else:
            with st.spinner("Running classification…"):
                try:
                    payload = {"source": source, "log_message": log_message}
                    resp = requests.post(
                        f"{API_BASE}/classify_single/",
                        json=payload,
                        timeout=30,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        label = data.get("predicted_label", "Unknown")

                        st.markdown(
                            f"""
                            <div style="margin-top:1rem;">
                                <p style="color:#64748b;font-size:0.85rem;margin-bottom:0.3rem;">PREDICTED LABEL</p>
                                <div class="result-badge">✦ {label}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        # ── Detail row ──
                        st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)
                        detail_col1, detail_col2 = st.columns(2)
                        with detail_col1:
                            st.metric("Source", source)
                        with detail_col2:
                            st.metric("Label", label)

                    else:
                        detail = resp.json().get("detail", resp.text)
                        st.error(f"❌  Server error {resp.status_code}: {detail}")
                except requests.exceptions.ConnectionError:
                    st.error("❌  Cannot connect to API. Make sure `server.py` is running on port 8000.")
                except Exception as ex:
                    st.error(f"❌  Unexpected error: {ex}")

    # ── Quick reference card ──
    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                    border-radius:14px;padding:1.2rem;">
            <p style="color:#94a3b8;font-size:0.85rem;font-weight:600;margin-bottom:0.7rem;">
                📋  Classification Pipeline
            </p>
            <p style="color:#64748b;font-size:0.82rem;line-height:1.8;margin:0;">
                🔵 <b style="color:#94a3b8;">LegacyCRM</b> → LLM (Groq)<br>
                🟣 <b style="color:#94a3b8;">Other sources</b> → Regex → BERT (fallback)<br>
                <br>
                <b style="color:#94a3b8;">Supported labels</b><br>
                Security Alert · HTTP Status · System Notification<br>
                Workflow Error · Deprecation Warning
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <p style="text-align:center;color:#334155;font-size:0.8rem;padding-bottom:1rem;">
        LogLens · NLP Log Classification · FastAPI + Streamlit
    </p>
    """,
    unsafe_allow_html=True,
)
