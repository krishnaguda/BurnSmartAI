"""
BurnSmartAI — Side-by-Side AI Model Comparison
Cohere Command R+  x  Llama 4 Scout 17B (Groq)
Both FREE tier — no credit card needed
"""

import streamlit as st
import time
from datetime import datetime

st.set_page_config(
    page_title="BurnSmartAI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

def inject_css():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0814 0%, #120f24 55%, #0d1117 100%);
        min-height: 100vh;
    }
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c24, #13102a) !important;
        border-right: 1px solid rgba(139,92,246,0.22) !important;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span { color: #c4b5fd !important; }

    .hero-title {
        font-size:2.75rem; font-weight:900;
        background:linear-gradient(120deg,#8B5CF6 20%,#a78bfa 60%,#f0abfc 100%);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        text-align:center; line-height:1.15; margin-bottom:.25rem;
    }
    .hero-sub { text-align:center; color:#6b7280; font-size:1rem; }
    .glowline {
        height:1px;
        background:linear-gradient(90deg,transparent,rgba(139,92,246,.5),transparent);
        margin:1.1rem 0;
    }

    /* Cohere badge — coral brand color */
    .badge-cohere {
        display:inline-block;
        background:linear-gradient(135deg,#FF7F57,#d94f2b);
        color:#fff !important; padding:.28rem 1rem; border-radius:20px;
        font-weight:700; font-size:.92rem; margin-bottom:.55rem;
    }
    /* Llama 4 Scout badge — cyan */
    .badge-llama4 {
        display:inline-block;
        background:linear-gradient(135deg,#22D3EE,#0891b2);
        color:#fff !important; padding:.28rem 1rem; border-radius:20px;
        font-weight:700; font-size:.92rem; margin-bottom:.55rem;
    }

    /* Cohere response box — coral tint */
    .resp-box-cohere {
        background:rgba(255,127,87,.06); border:1px solid rgba(255,127,87,.22);
        border-radius:12px; padding:1.1rem 1.25rem; min-height:200px;
        font-size:.92rem; line-height:1.75; color:#e2e8f0;
        white-space:pre-wrap; word-wrap:break-word;
    }
    /* Llama 4 response box — cyan tint */
    .resp-box-llama4 {
        background:rgba(34,211,238,.06); border:1px solid rgba(34,211,238,.22);
        border-radius:12px; padding:1.1rem 1.25rem; min-height:200px;
        font-size:.92rem; line-height:1.75; color:#e2e8f0;
        white-space:pre-wrap; word-wrap:break-word;
    }
    .resp-box-placeholder {
        background:rgba(75,85,99,.10); border:1px dashed rgba(107,114,128,.3);
        border-radius:12px; padding:1.1rem 1.25rem; min-height:200px;
        color:#4b5563; font-style:italic;
        display:flex; align-items:center; justify-content:center; font-size:.88rem;
    }

    .stats-bar { display:flex; gap:1rem; margin-top:.55rem; flex-wrap:wrap; }
    .stat-chip {
        background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.09);
        border-radius:8px; padding:.13rem .55rem; font-size:.76rem; color:#6b7280;
    }

    .stButton > button {
        background:linear-gradient(135deg,#8B5CF6,#6d28d9) !important;
        color:#fff !important; font-weight:800 !important; font-size:1rem !important;
        border:none !important; border-radius:10px !important; padding:.6rem 2rem !important;
        box-shadow:0 4px 18px rgba(139,92,246,.38) !important;
        transition:transform .2s,box-shadow .2s !important; width:100% !important;
    }
    .stButton > button:hover {
        transform:translateY(-2px) !important;
        box-shadow:0 8px 26px rgba(139,92,246,.55) !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background:rgba(139,92,246,.12) !important;
        border:1px solid rgba(139,92,246,.3) !important;
        color:#a78bfa !important; font-size:.84rem !important;
        font-weight:600 !important; padding:.32rem .9rem !important; box-shadow:none !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background:rgba(139,92,246,.24) !important; transform:none !important; box-shadow:none !important;
    }

    .history-card {
        background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.07);
        border-radius:10px; padding:.85rem 1.1rem; margin-bottom:.7rem;
    }
    .history-q { color:#a78bfa; font-weight:600; font-size:.88rem; margin-bottom:.3rem; }
    .history-meta { color:#4b5563; font-size:.75rem; }
    [data-testid="stExpander"] summary {
        color:#9ca3af !important; font-weight:600 !important; font-size:.9rem !important;
    }
    #MainMenu, footer { visibility:hidden; }
    </style>""", unsafe_allow_html=True)


def init_state():
    for k, v in {
        "history":[], "cohere_result":None, "llama4_result":None,
        "last_prompt":"", "last_system":"",
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ── API: Cohere Command R+ (free tier) ────────────────────────────────────────
def call_cohere(prompt, system_prompt, api_key):
    """
    Calls Cohere Command R+ via ClientV2.
    Free tier: https://dashboard.cohere.com/api-keys
    Returns { text, tokens_in, tokens_out, elapsed, error }
    """
    try:
        import cohere  # pip install cohere

        co = cohere.ClientV2(api_key=api_key)

        messages = []
        if system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt.strip()})
        messages.append({"role": "user", "content": prompt})

        t0 = time.time()
        response = co.chat(
            model="command-r-plus-08-2024",   # free-tier flagship model
            messages=messages,
        )
        elapsed = round(time.time() - t0, 2)

        text = response.message.content[0].text or ""

        # Token counts from billing units
        try:
            tokens_in  = response.usage.billed_units.input_tokens
            tokens_out = response.usage.billed_units.output_tokens
        except Exception:
            tokens_in  = len(prompt.split())
            tokens_out = len(text.split())

        return {"text": text, "tokens_in": tokens_in, "tokens_out": tokens_out,
                "elapsed": elapsed, "error": None}

    except ImportError:
        return {"text":"","tokens_in":0,"tokens_out":0,"elapsed":0,
                "error":"Package missing — run: pip install cohere"}
    except Exception as e:
        return {"text":"","tokens_in":0,"tokens_out":0,"elapsed":0,"error":str(e)}


# ── API: Llama 4 Scout 17B via Groq (free tier) ───────────────────────────────
def call_llama4(prompt, system_prompt, api_key):
    """
    Calls Llama 4 Scout 17B via Groq.
    Free tier: https://console.groq.com/keys
    Returns { text, tokens_in, tokens_out, elapsed, error }
    """
    try:
        from groq import Groq  # pip install groq

        client = Groq(api_key=api_key)
        messages = []
        if system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt.strip()})
        messages.append({"role": "user", "content": prompt})

        t0 = time.time()
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            max_tokens=1024,
            temperature=0.7,
            messages=messages,
        )
        elapsed    = round(time.time() - t0, 2)
        text       = response.choices[0].message.content or ""
        tokens_in  = response.usage.prompt_tokens
        tokens_out = response.usage.completion_tokens

        return {"text": text, "tokens_in": tokens_in, "tokens_out": tokens_out,
                "elapsed": elapsed, "error": None}

    except ImportError:
        return {"text":"","tokens_in":0,"tokens_out":0,"elapsed":0,
                "error":"Package missing — run: pip install groq"}
    except Exception as e:
        return {"text":"","tokens_in":0,"tokens_out":0,"elapsed":0,"error":str(e)}


# ── Render one model column ───────────────────────────────────────────────────
def render_column(result, badge_html, box_class, placeholder):
    st.markdown(badge_html, unsafe_allow_html=True)
    if result is None:
        st.markdown(f'<div class="resp-box-placeholder">{placeholder}</div>',
                    unsafe_allow_html=True)
        return
    if result["error"]:
        st.error(f"⚠️ {result['error']}")
        return
    st.markdown(f'<div class="{box_class}">{result["text"]}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="stats-bar">'
        f'<span class="stat-chip">⏱ {result["elapsed"]}s</span>'
        f'<span class="stat-chip">📥 {result["tokens_in"]} in</span>'
        f'<span class="stat-chip">📤 {result["tokens_out"]} out</span>'
        f'</div>', unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        if st.button("☰  Hide Sidebar", use_container_width=True):
            st.markdown("""<script>
            const ctrl = window.parent.document
                .querySelector('[data-testid="collapsedControl"]');
            if (ctrl) ctrl.click();
            </script>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🔑 API Keys")

        cohere_key = st.text_input(
            "Cohere API Key",
            type="password",
            placeholder="••••••••••••••••••••",
            help="Free → https://dashboard.cohere.com/api-keys",
        )
        groq_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_…",
            help="Free → https://console.groq.com/keys",
        )

        c1, c2 = st.columns(2)
        c1.success("✅ Cohere") if cohere_key else c1.warning("⚠️ Cohere")
        c2.success("✅ Groq")   if groq_key   else c2.warning("⚠️ Groq")

        st.markdown("---")
        st.markdown("### 🤖 Models")
        st.markdown(
            "| | Model |\n|---|---|\n"
            "| 🟠 | Cohere Command R+ |\n"
            "| 🩵 | Llama 4 Scout 17B |"
        )
        st.markdown("---")
        st.markdown("### 💡 Get Free Keys")
        st.markdown(
            "**Cohere:** [dashboard.cohere.com](https://dashboard.cohere.com/api-keys)\n\n"
            "**Groq:** [console.groq.com](https://console.groq.com/keys)"
        )
        st.markdown("---")
        st.caption("BurnSmartAI · Dual-AI Comparison")

    return cohere_key or "", groq_key or ""


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    inject_css()
    init_state()

    cohere_key, groq_key = render_sidebar()

    # Hero
    st.markdown('<div class="hero-title">🔍 BurnSmartAI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Side-by-side AI comparison &nbsp;·&nbsp; '
        '<span style="color:#FF7F57;font-weight:600;">Cohere Command R+</span>'
        ' &nbsp;×&nbsp; '
        '<span style="color:#22D3EE;font-weight:600;">Llama 4 Scout 17B</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="glowline"></div>', unsafe_allow_html=True)

    # System prompt expander
    with st.expander("🧩 System Prompt  *(optional)*", expanded=False):
        system_prompt = st.text_area(
            "Instructions sent to both models",
            value=st.session_state.get("last_system", ""),
            placeholder="e.g. You are a concise technical assistant. Use bullet points.",
            height=85,
            label_visibility="collapsed",
        )
        st.session_state["last_system"] = system_prompt
    system_prompt = st.session_state.get("last_system", "")

    # Prompt input
    prompt = st.text_area(
        "💬 Your Prompt",
        value=st.session_state.get("last_prompt", ""),
        placeholder="Ask anything — both models respond simultaneously…",
        height=130,
    )

    # Compare button
    btn_col, _ = st.columns([2, 5])
    with btn_col:
        compare = st.button("⚡ Compare Models", use_container_width=True)

    st.markdown('<div class="glowline"></div>', unsafe_allow_html=True)

    # Run comparison
    if compare:
        if not prompt.strip():
            st.error("⚠️ Please enter a prompt first.")
            st.stop()

        st.session_state["last_prompt"] = prompt
        prog = st.progress(0, text="Sending to models…")
        cohere_res = llama4_res = None

        if cohere_key:
            prog.progress(15, text="⏳ Calling Cohere Command R+…")
            with st.spinner("Cohere thinking…"):
                cohere_res = call_cohere(prompt, system_prompt, cohere_key)

        prog.progress(55, text="⏳ Calling Llama 4 Scout…")
        if groq_key:
            with st.spinner("Llama thinking…"):
                llama4_res = call_llama4(prompt, system_prompt, groq_key)

        prog.progress(100, text="✅ Done!")
        time.sleep(0.3)
        prog.empty()

        st.session_state["cohere_result"] = cohere_res
        st.session_state["llama4_result"] = llama4_res
        st.session_state["history"].insert(0, {
            "ts":     datetime.now().strftime("%H:%M:%S"),
            "prompt": prompt[:110] + ("…" if len(prompt) > 110 else ""),
            "cohere": cohere_res,
            "llama4": llama4_res,
        })

    # Results — 2 equal columns
    c_res = st.session_state.get("cohere_result")
    l_res = st.session_state.get("llama4_result")

    if c_res is not None or l_res is not None:
        col_c, col_l = st.columns(2, gap="large")
        with col_c:
            render_column(
                c_res,
                '<div class="badge-cohere">🟠 Cohere Command R+</div>',
                "resp-box-cohere",
                "Add your Cohere API key in the sidebar to enable.",
            )
        with col_l:
            render_column(
                l_res,
                '<div class="badge-llama4">🩵 Llama 4 Scout 17B</div>',
                "resp-box-llama4",
                "Add your Groq API key in the sidebar to enable.",
            )

    # Session history
    if st.session_state["history"]:
        st.markdown('<div class="glowline"></div>', unsafe_allow_html=True)
        with st.expander(
            f"🕓 Session History  ({len(st.session_state['history'])} runs)",
            expanded=False,
        ):
            for idx, entry in enumerate(st.session_state["history"]):
                c = entry.get("cohere")
                l = entry.get("llama4")
                c_time = f"{c['elapsed']}s" if c and not c["error"] else "—"
                l_time = f"{l['elapsed']}s" if l and not l["error"] else "—"
                c_tok  = c["tokens_out"]    if c and not c["error"] else "—"
                l_tok  = l["tokens_out"]    if l and not l["error"] else "—"
                num    = len(st.session_state["history"]) - idx
                st.markdown(
                    f'<div class="history-card">'
                    f'<div class="history-q">#{num} &nbsp;·&nbsp; {entry["ts"]} &nbsp;—&nbsp; {entry["prompt"]}</div>'
                    f'<div class="history-meta">'
                    f'🟠 Cohere: {c_time} &nbsp;·&nbsp; {c_tok} tokens out'
                    f'&nbsp;&nbsp;|&nbsp;&nbsp;'
                    f'🩵 Llama 4: {l_time} &nbsp;·&nbsp; {l_tok} tokens out'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )
            if st.button("🗑️ Clear History"):
                st.session_state["history"] = []
                st.rerun()

    # Footer
    st.markdown('<div class="glowline"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center;color:#374151;font-size:.78rem;padding:.4rem 0;">'
        '🔍 BurnSmartAI &nbsp;·&nbsp; Cohere Command R+ × Llama 4 Scout 17B &nbsp;·&nbsp; Dual-AI Comparison'
        '</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
