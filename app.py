"""
╔══════════════════════════════════════════════════════════╗
║   BurnSmartAI — Side-by-Side AI Model Comparison        ║
║   Gemini 2.0 Flash  ×  Llama 4 Scout 17B (Groq)        ║
╚══════════════════════════════════════════════════════════╝
"""

import streamlit as st
import time
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BurnSmartAI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    /* ── Base & background ── */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0814 0%, #120f24 50%, #0d1117 100%);
        min-height: 100vh;
    }
    [data-testid="stHeader"] { background: transparent !important; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c24 0%, #13102a 100%) !important;
        border-right: 1px solid rgba(139,92,246,0.25) !important;
    }
    [data-testid="stSidebar"] * { color: #d1d5db !important; }

    /* ── Hero title ── */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(120deg, #8B5CF6, #a78bfa, #f0abfc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .hero-sub {
        text-align: center;
        color: #6b7280;
        font-size: 1rem;
        margin-bottom: 1.2rem;
    }

    /* ── Divider ── */
    .glowline {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139,92,246,.55), transparent);
        margin: 1.2rem 0;
    }

    /* ── Model header badges ── */
    .badge-gemini {
        display: inline-block;
        background: linear-gradient(135deg, #4285F4, #0d6efd);
        color: #fff !important;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: .03em;
        margin-bottom: .6rem;
    }
    .badge-llama4 {
        display: inline-block;
        background: linear-gradient(135deg, #22D3EE, #0891b2);
        color: #fff !important;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: .03em;
        margin-bottom: .6rem;
    }

    /* ── Response boxes ── */
    .resp-box-gemini {
        background: rgba(66,133,244,0.06);
        border: 1px solid rgba(66,133,244,0.22);
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        min-height: 180px;
        font-size: 0.93rem;
        line-height: 1.7;
        color: #e2e8f0;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .resp-box-llama4 {
        background: rgba(34,211,238,0.06);
        border: 1px solid rgba(34,211,238,0.22);
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        min-height: 180px;
        font-size: 0.93rem;
        line-height: 1.7;
        color: #e2e8f0;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .resp-box-placeholder {
        background: rgba(75,85,99,0.12);
        border: 1px dashed rgba(107,114,128,0.35);
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        min-height: 180px;
        color: #4b5563;
        font-style: italic;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
    }

    /* ── Stats caption ── */
    .stats-bar {
        display: flex;
        gap: 1.2rem;
        margin-top: 0.6rem;
        font-size: 0.78rem;
        color: #6b7280;
        flex-wrap: wrap;
    }
    .stat-chip {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 8px;
        padding: 0.15rem 0.6rem;
    }

    /* ── Metric cards ── */
    [data-testid="stMetric"] {
        background: rgba(139,92,246,0.08);
        border: 1px solid rgba(139,92,246,0.2);
        border-radius: 10px;
        padding: 0.7rem 1rem;
    }
    [data-testid="stMetricLabel"] { color: #9ca3af !important; font-size:.8rem !important; }
    [data-testid="stMetricValue"] { color: #e2e8f0 !important; }
    [data-testid="stMetricDelta"] { font-size:.78rem !important; }

    /* ── Template buttons ── */
    div[data-testid="column"] .stButton > button {
        background: rgba(139,92,246,0.12) !important;
        border: 1px solid rgba(139,92,246,0.3) !important;
        color: #a78bfa !important;
        border-radius: 8px !important;
        font-size: 0.82rem !important;
        padding: 0.4rem 0.7rem !important;
        font-weight: 600 !important;
        transition: all .2s !important;
        width: 100% !important;
    }
    div[data-testid="column"] .stButton > button:hover {
        background: rgba(139,92,246,0.28) !important;
        border-color: rgba(139,92,246,0.6) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Compare button ── */
    .compare-btn > button {
        background: linear-gradient(135deg,#8B5CF6,#6d28d9) !important;
        color: #fff !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 2.5rem !important;
        box-shadow: 0 4px 20px rgba(139,92,246,0.4) !important;
        transition: all .25s !important;
        width: 100% !important;
    }
    .compare-btn > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(139,92,246,0.55) !important;
    }

    /* ── Sidebar toggle button ── */
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(139,92,246,0.15) !important;
        border: 1px solid rgba(139,92,246,0.35) !important;
        color: #a78bfa !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }

    /* ── History box ── */
    .history-entry {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.8rem;
        font-size: 0.85rem;
    }
    .history-prompt {
        color: #a78bfa;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .history-meta {
        color: #4b5563;
        font-size: 0.75rem;
    }

    /* ── Expander ── */
    [data-testid="stExpander"] summary {
        color: #9ca3af !important;
        font-weight: 600 !important;
    }

    /* ── Hide branding ── */
    #MainMenu, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "history": [],
        "last_prompt": "",
        "last_system": "",
        "gemini_result": None,
        "llama4_result": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ── Prompt templates ──────────────────────────────────────────────────────────
TEMPLATES = {
    "💻 Code Explain":    "Explain the following code step by step, covering what it does, how it works, and any potential improvements:\n\n",
    "✍️ Writing Help":    "Help me improve the following text for clarity, tone, and impact:\n\n",
    "📊 Analysis":        "Provide a thorough analysis of the following topic, including key factors, implications, and evidence:\n\n",
    "🧠 Brainstorm":      "Generate 10 creative and diverse ideas related to the following topic, with a brief rationale for each:\n\n",
    "🔬 Research":        "Summarise the current state of research on the following topic, covering key findings, debates, and open questions:\n\n",
}


# ── API call: Gemini ──────────────────────────────────────────────────────────
def call_gemini(api_key: str, meta_prompt: str) -> str:
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=meta_prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=2048,
            ),
        )
        return response.text
    except Exception as e:
        raise RuntimeError(str(e))


# ── API call: Llama 4 Scout via Groq ─────────────────────────────────────────
def call_llama4(prompt: str, system_prompt: str, api_key: str, temperature: float, max_tokens: int) -> dict:
    """
    Calls Llama 4 Scout 17B via Groq. Returns same shape as call_gemini().
    """
    try:
        from groq import Groq

        client = Groq(api_key=api_key)

        messages = []
        if system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt.strip()})
        messages.append({"role": "user", "content": prompt})

        t0 = time.time()
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
        )
        elapsed = round(time.time() - t0, 2)

        text      = response.choices[0].message.content or ""
        tokens_in  = response.usage.prompt_tokens
        tokens_out = response.usage.completion_tokens

        return {"text": text, "tokens_in": tokens_in, "tokens_out": tokens_out,
                "elapsed": elapsed, "error": None}

    except ImportError:
        return {"text": "", "tokens_in": 0, "tokens_out": 0, "elapsed": 0,
                "error": "Package missing — run: pip install groq"}
    except Exception as e:
        return {"text": "", "tokens_in": 0, "tokens_out": 0, "elapsed": 0,
                "error": str(e)}


# ── Render one response column ────────────────────────────────────────────────
def render_response(result: dict | None, model_name: str, badge_class: str, box_class: str, placeholder_msg: str):
    """Render badge, response box, and stats for one model."""
    st.markdown(f'<div class="{badge_class}">{model_name}</div>', unsafe_allow_html=True)

    if result is None:
        # No key provided
        st.markdown(
            f'<div class="resp-box-placeholder">{placeholder_msg}</div>',
            unsafe_allow_html=True,
        )
        return

    if result["error"]:
        st.error(f"⚠️ {result['error']}")
        return

    # Response text
    st.markdown(
        f'<div class="{box_class}">{result["text"]}</div>',
        unsafe_allow_html=True,
    )

    # Stats chips
    words = len(result["text"].split())
    st.markdown(
        f"""
        <div class="stats-bar">
            <span class="stat-chip">⏱ {result['elapsed']}s</span>
            <span class="stat-chip">📥 {result['tokens_in']} in</span>
            <span class="stat-chip">📤 {result['tokens_out']} out</span>
            <span class="stat-chip">🔤 {words} words</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar() -> tuple[str, str, float, int]:
    with st.sidebar:
        st.markdown("## ⚙️ BurnSmartAI")
        st.markdown("---")

        # ── API Keys ──────────────────────────────────────────────────────────
        st.markdown("### 🔑 API Keys")
        gemini_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="AIza...",
            help="Free key → https://aistudio.google.com/app/apikey",
        )
        groq_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Free key → https://console.groq.com/keys",
        )

        # Key status
        c1, c2 = st.columns(2)
        c1.success("✅ Gemini") if gemini_key else c1.warning("⚠️ Gemini")
        c2.success("✅ Groq")   if groq_key   else c2.warning("⚠️ Groq")

        st.markdown("---")

        # ── Generation controls ───────────────────────────────────────────────
        st.markdown("### 🎛️ Generation")
        temperature = st.slider(
            "Temperature",
            min_value=0.0, max_value=1.0,
            value=0.7, step=0.05,
            help="Higher = more creative. Lower = more focused."
        )
        max_tokens = st.slider(
            "Max Tokens",
            min_value=100, max_value=4000,
            value=1024, step=100,
            help="Maximum tokens in the response."
        )

        st.markdown("---")

        # ── Model info ────────────────────────────────────────────────────────
        st.markdown("### 🤖 Models")
        st.markdown("""
| Model | Provider |
|---|---|
| Gemini 2.0 Flash | Google |
| Llama 4 Scout 17B | Groq |
""")

        st.markdown("---")
        st.caption("BurnSmartAI · Dual-AI Comparison")

    return gemini_key or "", groq_key or "", temperature, max_tokens


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    inject_css()
    init_state()

    gemini_key, groq_key, temperature, max_tokens = render_sidebar()

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="hero-title">🔍 BurnSmartAI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Side-by-side AI comparison · '
        '<span style="color:#4285F4;font-weight:600;">Gemini 2.0 Flash</span> &nbsp;×&nbsp; '
        '<span style="color:#22D3EE;font-weight:600;">Llama 4 Scout 17B</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="glowline"></div>', unsafe_allow_html=True)

    # ── Prompt templates ──────────────────────────────────────────────────────
    with st.expander("⚡ Prompt Templates", expanded=False):
        st.caption("Click a template to pre-fill the prompt box.")
        tcols = st.columns(len(TEMPLATES))
        for i, (label, starter) in enumerate(TEMPLATES.items()):
            if tcols[i].button(label, key=f"tpl_{i}"):
                st.session_state["last_prompt"] = starter

    # ── System prompt ─────────────────────────────────────────────────────────
    with st.expander("🧩 System Prompt (optional)", expanded=False):
        system_prompt = st.text_area(
            "System instructions sent to both models",
            value=st.session_state.get("last_system", ""),
            placeholder="e.g. You are a concise technical assistant. Always use bullet points.",
            height=90,
            key="system_input",
            label_visibility="collapsed",
        )
        st.session_state["last_system"] = system_prompt
    else_system = st.session_state.get("last_system", "")

    # ── Prompt input ──────────────────────────────────────────────────────────
    prompt = st.text_area(
        "💬 Your Prompt",
        value=st.session_state.get("last_prompt", ""),
        placeholder="Ask anything — both models will respond simultaneously…",
        height=130,
        key="prompt_input",
    )

    # ── Compare button ────────────────────────────────────────────────────────
    btn_col, _ = st.columns([2, 5])
    with btn_col:
        st.markdown('<div class="compare-btn">', unsafe_allow_html=True)
        compare = st.button("⚡ Compare Models", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glowline"></div>', unsafe_allow_html=True)

    # ── Run comparison ────────────────────────────────────────────────────────
    if compare:
        if not prompt.strip():
            st.error("⚠️ Please enter a prompt before comparing.")
            st.stop()

        st.session_state["last_prompt"] = prompt

        gemini_res = llama4_res = None
        prog = st.progress(0, text="Sending to models…")

        # ── Gemini ────────────────────────────────────────────────────────────
        if gemini_key:
            prog.progress(20, text="⏳ Calling Gemini…")
            with st.spinner("Gemini thinking…"):
                gemini_res = call_gemini(prompt, else_system, gemini_key, temperature, max_tokens)
        prog.progress(55, text="⏳ Calling Llama 4 Scout…")

        # ── Llama 4 Scout ─────────────────────────────────────────────────────
        if groq_key:
            with st.spinner("Llama thinking…"):
                llama4_res = call_llama4(prompt, else_system, groq_key, temperature, max_tokens)
        prog.progress(100, text="✅ Done!")
        time.sleep(0.3)
        prog.empty()

        st.session_state["gemini_result"] = gemini_res
        st.session_state["llama4_result"] = llama4_res

        # Save to history
        st.session_state["history"].insert(0, {
            "ts":      datetime.now().strftime("%H:%M:%S"),
            "prompt":  prompt[:120] + ("…" if len(prompt) > 120 else ""),
            "gemini":  gemini_res,
            "llama4":  llama4_res,
        })

    # ── Results columns ───────────────────────────────────────────────────────
    g_res = st.session_state.get("gemini_result")
    l_res = st.session_state.get("llama4_result")

    if g_res is not None or l_res is not None or not compare:
        col_g, col_l = st.columns(2, gap="large")

        with col_g:
            render_response(
                result=g_res,
                model_name="🔵 Gemini 2.0 Flash",
                badge_class="badge-gemini",
                box_class="resp-box-gemini",
                placeholder_msg="Add your Gemini API key in the sidebar to enable this model.",
            )

        with col_l:
            render_response(
                result=l_res,
                model_name="🩵 Llama 4 Scout 17B",
                badge_class="badge-llama4",
                box_class="resp-box-llama4",
                placeholder_msg="Add your Groq API key in the sidebar to enable this model.",
            )

        # ── Comparison metrics ────────────────────────────────────────────────
        if (g_res and not g_res["error"]) or (l_res and not l_res["error"]):
            st.markdown('<div class="glowline"></div>', unsafe_allow_html=True)
            st.markdown("#### 📊 Head-to-Head Metrics")

            m1, m2, m3, m4, m5, m6 = st.columns(6)

            # Speed
            g_time = g_res["elapsed"] if g_res and not g_res["error"] else None
            l_time = l_res["elapsed"] if l_res and not l_res["error"] else None
            m1.metric("⏱ Gemini Time",   f"{g_time}s"  if g_time  else "—")
            m2.metric("⏱ Llama Time",    f"{l_time}s"  if l_time  else "—")

            # Output tokens
            g_tok = g_res["tokens_out"] if g_res and not g_res["error"] else None
            l_tok = l_res["tokens_out"] if l_res and not l_res["error"] else None
            m3.metric("📤 Gemini Tokens", g_tok if g_tok else "—")
            m4.metric("📤 Llama Tokens",  l_tok if l_tok else "—")

            # Word count
            g_wc = len(g_res["text"].split()) if g_res and not g_res["error"] else None
            l_wc = len(l_res["text"].split()) if l_res and not l_res["error"] else None
            m5.metric("🔤 Gemini Words",  g_wc if g_wc else "—")
            m6.metric("🔤 Llama Words",   l_wc if l_wc else "—")

            # Speed winner callout
            if g_time and l_time:
                if g_time < l_time:
                    st.info(f"⚡ **Gemini** was faster by **{round(l_time - g_time, 2)}s**")
                elif l_time < g_time:
                    st.info(f"⚡ **Llama 4 Scout** was faster by **{round(g_time - l_time, 2)}s**")
                else:
                    st.info("🤝 Both models responded in the same time.")

    # ── Session history ───────────────────────────────────────────────────────
    if st.session_state["history"]:
        st.markdown('<div class="glowline"></div>', unsafe_allow_html=True)
        with st.expander(f"🕓 Session History ({len(st.session_state['history'])} runs)", expanded=False):
            for i, entry in enumerate(st.session_state["history"]):
                g = entry.get("gemini")
                l = entry.get("llama4")
                g_words = len(g["text"].split()) if g and not g["error"] else "err"
                l_words = len(l["text"].split()) if l and not l["error"] else "err"
                g_time  = f"{g['elapsed']}s" if g and not g["error"] else "—"
                l_time  = f"{l['elapsed']}s" if l and not l["error"] else "—"

                st.markdown(
                    f"""
                    <div class="history-entry">
                        <div class="history-prompt">#{len(st.session_state['history'])-i} · {entry['ts']} — {entry['prompt']}</div>
                        <div class="history-meta">
                            🔵 Gemini: {g_time} · {g_words} words &nbsp;|&nbsp;
                            🩵 Llama 4: {l_time} · {l_words} words
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            if st.button("🗑️ Clear History"):
                st.session_state["history"] = []
                st.rerun()

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown('<div class="glowline"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center;color:#374151;font-size:.8rem;padding:.5rem 0;">'
        '🔍 BurnSmartAI · Gemini 2.0 Flash × Llama 4 Scout 17B · Dual-AI Comparison Engine'
        '</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
