"""
BurnSmartAI — Side-by-side AI model comparison
Models: Gemini 3 Flash Preview (Google) · Llama 4 Scout 17B (Meta/Groq)
"""

import time
import datetime
import concurrent.futures
import streamlit as st

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BurnSmartAI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base & fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Dark glass background ── */
.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    min-height: 100vh;
}

/* ── Sidebar glass ── */
[data-testid="stSidebar"] {
    background: rgba(15, 15, 30, 0.85) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(139, 92, 246, 0.2);
}
[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }

/* ── Main container ── */
.block-container {
    padding: 2rem 3rem 3rem 3rem;
    max-width: 1400px;
}

/* ── Hero title ── */
.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #8B5CF6, #a78bfa, #22D3EE);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
    line-height: 1.1;
}
.hero-sub {
    color: #94a3b8;
    font-size: 1.05rem;
    font-weight: 400;
    margin-bottom: 2rem;
}

/* ── Model badge headers ── */
.badge-gemini {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, rgba(66,133,244,0.25), rgba(66,133,244,0.08));
    border: 1px solid rgba(66,133,244,0.5);
    color: #93c5fd;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 0.4rem 1rem;
    border-radius: 100px;
    letter-spacing: 0.03em;
    margin-bottom: 1rem;
}
.badge-llama {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, rgba(34,211,238,0.25), rgba(34,211,238,0.08));
    border: 1px solid rgba(34,211,238,0.5);
    color: #67e8f9;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 0.4rem 1rem;
    border-radius: 100px;
    letter-spacing: 0.03em;
    margin-bottom: 1rem;
}

/* ── Response glass cards ── */
.response-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    min-height: 220px;
    backdrop-filter: blur(10px);
    color: #e2e8f0;
    font-size: 0.94rem;
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
}
.response-card-gemini {
    border-left: 3px solid #4285F4;
}
.response-card-llama {
    border-left: 3px solid #22D3EE;
}
.response-placeholder {
    background: rgba(255,255,255,0.02);
    border: 1px dashed rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 2rem 1.5rem;
    color: #475569;
    font-size: 0.92rem;
    text-align: center;
    font-style: italic;
}

/* ── Stats caption ── */
.stats-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-top: 0.75rem;
}
.stat-chip {
    background: rgba(139,92,246,0.12);
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 8px;
    padding: 0.25rem 0.65rem;
    font-size: 0.75rem;
    color: #a78bfa;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
}

/* ── Divider ── */
.section-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 1.8rem 0;
}

/* ── Template buttons ── */
.stButton > button {
    background: rgba(139,92,246,0.12) !important;
    border: 1px solid rgba(139,92,246,0.3) !important;
    color: #c4b5fd !important;
    border-radius: 10px !important;
    font-size: 0.82rem !important;
    padding: 0.4rem 0.8rem !important;
    transition: all 0.2s ease !important;
    font-weight: 500 !important;
}
.stButton > button:hover {
    background: rgba(139,92,246,0.28) !important;
    border-color: rgba(139,92,246,0.6) !important;
    color: #fff !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(139,92,246,0.2) !important;
}

/* ── Primary compare button ── */
div[data-testid="stButton"]:has(button[kind="primary"]) button {
    background: linear-gradient(135deg, #7c3aed, #8B5CF6, #6d28d9) !important;
    border: none !important;
    color: white !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    padding: 0.65rem 2.5rem !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 20px rgba(139,92,246,0.35) !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
    color: #94a3b8 !important;
    font-size: 0.9rem !important;
}

/* ── Inputs & sliders ── */
[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stTextArea"] textarea:focus,
[data-testid="stTextInput"] input:focus {
    border-color: rgba(139,92,246,0.5) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.1) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem;
}
[data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 0.8rem !important; }
[data-testid="stMetricValue"] { color: #e2e8f0 !important; font-size: 1.5rem !important; font-weight: 600 !important; }
[data-testid="stMetricDelta"] { font-size: 0.78rem !important; }

/* ── History card ── */
.history-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.7rem;
    color: #94a3b8;
    font-size: 0.85rem;
}
.history-prompt {
    color: #c4b5fd;
    font-weight: 600;
    margin-bottom: 0.35rem;
    font-size: 0.88rem;
}

/* ── Sidebar toggle ── */
[data-testid="collapsedControl"] { color: #8B5CF6 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(139,92,246,0.5); }

/* ── Success / error alerts ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left-width: 3px !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Session state defaults ──────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "prompt_text" not in st.session_state:
    st.session_state.prompt_text = ""
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = True


# ─── Prompt templates ────────────────────────────────────────────────────────
TEMPLATES = {
    "💻 Code Explain": "Explain the following code snippet step by step, including what each part does and any potential improvements:\n\n```python\n# paste code here\n```",
    "✍️ Writing Help": "Help me improve this paragraph for clarity, tone, and engagement. Provide a revised version with brief notes on what you changed and why:\n\n[paste your text here]",
    "🔬 Analysis": "Analyze the following topic from multiple angles — pros/cons, opportunities, risks, and your overall assessment:\n\nTopic: [enter topic]",
    "💡 Brainstorm": "Generate 10 creative and actionable ideas for the following challenge. For each idea, give a one-sentence rationale:\n\nChallenge: [describe your challenge]",
    "🔍 Research": "Provide a comprehensive overview of [topic], covering: background & history, current state, key players or concepts, recent developments, and open questions or debates.",
}


# ─── API call functions ───────────────────────────────────────────────────────

def call_gemini(key: str, prompt: str, system: str, temp: float, max_tok: int) -> dict:
    """Call Gemini 3 Flash Preview via google-genai."""
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=key)
        full_prompt = f"{system}\n\n{prompt}".strip() if system else prompt

        t0 = time.time()
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                temperature=temp,
                max_output_tokens=max_tok,
            ),
        )
        elapsed = time.time() - t0

        text = response.text or ""
        tokens_in  = getattr(getattr(response, "usage_metadata", None), "prompt_token_count", 0) or 0
        tokens_out = getattr(getattr(response, "usage_metadata", None), "candidates_token_count", 0) or 0

        return {"ok": True, "text": text, "time": elapsed,
                "tokens_in": tokens_in, "tokens_out": tokens_out}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def call_llama(key: str, prompt: str, system: str, temp: float, max_tok: int) -> dict:
    """Call Llama 4 Scout 17B via Groq."""
    try:
        from groq import Groq

        client = Groq(api_key=key)
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        t0 = time.time()
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            max_tokens=max_tok,
            temperature=temp,
            messages=messages,
        )
        elapsed = time.time() - t0

        text       = response.choices[0].message.content or ""
        tokens_in  = response.usage.prompt_tokens  if response.usage else 0
        tokens_out = response.usage.completion_tokens if response.usage else 0

        return {"ok": True, "text": text, "time": elapsed,
                "tokens_in": tokens_in, "tokens_out": tokens_out}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def word_count(text: str) -> int:
    return len(text.split()) if text.strip() else 0

def fmt_time(seconds: float) -> str:
    return f"{seconds:.2f}s"

def render_badge(model_name: str, badge_class: str) -> str:
    icons = {"badge-gemini": "✦", "badge-llama": "◈"}
    icon = icons.get(badge_class, "●")
    return f'<span class="{badge_class}">{icon} {model_name}</span>'

def render_stats(r: dict) -> str:
    if not r.get("ok"):
        return ""
    chips = [
        f'<span class="stat-chip">⏱ {fmt_time(r["time"])}</span>',
        f'<span class="stat-chip">↑ {r["tokens_in"]} in</span>',
        f'<span class="stat-chip">↓ {r["tokens_out"]} out</span>',
        f'<span class="stat-chip">📝 {word_count(r["text"])} words</span>',
    ]
    return f'<div class="stats-row">{"".join(chips)}</div>'


# ─── Sidebar ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        "<div style='font-size:1.3rem;font-weight:700;color:#a78bfa;margin-bottom:0.2rem;'>"
        "⚙️ Configuration</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='font-size:0.78rem;color:#475569;margin-bottom:1.2rem;'>"
        "Keys are never stored between sessions.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("**🔑 API Keys**")
    gemini_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIza…",
        help="Get a free key at aistudio.google.com",
    )
    groq_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_…",
        help="Get a free key at console.groq.com (covers Llama 4 Scout)",
    )

    st.markdown("<hr style='border-color:rgba(255,255,255,0.07);margin:1rem 0'>",
                unsafe_allow_html=True)
    st.markdown("**🎛️ Generation Settings**")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05,
                            help="Higher = more creative/random")
    max_tokens  = st.slider("Max Tokens", 100, 4000, 1024, 100,
                            help="Maximum response length")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.07);margin:1rem 0'>",
                unsafe_allow_html=True)
    st.markdown("**ℹ️ Models**")
    st.markdown("""
<div style='font-size:0.78rem;color:#64748b;line-height:1.7;'>
<span style='color:#93c5fd;'>✦ Gemini Flash</span> · Google · Free tier<br>
<span style='color:#67e8f9;'>◈ Llama 4 Scout</span> · Meta/Groq · Free tier
</div>
""", unsafe_allow_html=True)


# ─── Main area ───────────────────────────────────────────────────────────────

st.markdown('<div class="hero-title">🔍 BurnSmartAI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Compare two frontier AI models side by side — '
    'same prompt, instant results, full stats.</div>',
    unsafe_allow_html=True,
)

# ── System prompt (optional) ──
with st.expander("🧩 System Prompt  *(optional)*", expanded=False):
    system_prompt = st.text_area(
        "System instructions sent to both models",
        placeholder="e.g. You are a concise, expert assistant. Always reason step-by-step.",
        height=90,
        label_visibility="collapsed",
    )

# ── Prompt templates ──
with st.expander("⚡ Prompt Templates", expanded=False):
    st.markdown(
        "<div style='color:#64748b;font-size:0.82rem;margin-bottom:0.7rem;'>"
        "Click a template to load it into the prompt box.</div>",
        unsafe_allow_html=True,
    )
    cols_t = st.columns(len(TEMPLATES))
    for col, (label, tpl) in zip(cols_t, TEMPLATES.items()):
        with col:
            if st.button(label, key=f"tpl_{label}"):
                st.session_state.prompt_text = tpl

# ── Prompt input ──
user_prompt = st.text_area(
    "Your prompt",
    value=st.session_state.prompt_text,
    placeholder="Ask anything — compare how each model thinks, writes, and reasons…",
    height=130,
    label_visibility="collapsed",
)

col_btn, col_hint = st.columns([1, 5])
with col_btn:
    compare_clicked = st.button("⚡ Compare", type="primary", use_container_width=True)
with col_hint:
    st.markdown(
        "<div style='color:#334155;font-size:0.8rem;margin-top:0.7rem;'>"
        "Runs both models in parallel — typically 2–8 seconds.</div>",
        unsafe_allow_html=True,
    )

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ─── Results ─────────────────────────────────────────────────────────────────

if compare_clicked:
    if not user_prompt.strip():
        st.warning("Please enter a prompt before comparing.")
        st.stop()

    missing = []
    if not gemini_key: missing.append("Gemini")
    if not groq_key:   missing.append("Groq (Llama 4 Scout)")
    if missing:
        st.error(f"Missing API keys: **{', '.join(missing)}**. Add them in the sidebar.")
        st.stop()

    sys_txt = system_prompt.strip() if "system_prompt" in dir() else ""

    # ── Parallel API calls ──
    with st.spinner("🔄 Querying both models in parallel…"):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            fut_gem  = pool.submit(call_gemini, gemini_key, user_prompt, sys_txt, temperature, max_tokens)
            fut_llama = pool.submit(call_llama,  groq_key,  user_prompt, sys_txt, temperature, max_tokens)
            r_gem   = fut_gem.result()
            r_llama = fut_llama.result()

    # ── Render columns ──
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(render_badge("Gemini 2.0 Flash", "badge-gemini"), unsafe_allow_html=True)
        if r_gem["ok"]:
            st.markdown(
                f'<div class="response-card response-card-gemini">{r_gem["text"]}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(render_stats(r_gem), unsafe_allow_html=True)
        else:
            st.error(f"Gemini error: {r_gem['error']}")

    with col2:
        st.markdown(render_badge("Llama 4 Scout 17B", "badge-llama"), unsafe_allow_html=True)
        if r_llama["ok"]:
            st.markdown(
                f'<div class="response-card response-card-llama">{r_llama["text"]}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(render_stats(r_llama), unsafe_allow_html=True)
        else:
            st.error(f"Llama 4 Scout error: {r_llama['error']}")

    # ── Comparison metrics ──
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown(
        "<div style='color:#94a3b8;font-size:0.85rem;font-weight:600;"
        "letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.8rem;'>"
        "📊 Comparison Metrics</div>",
        unsafe_allow_html=True,
    )

    ok_gem   = r_gem.get("ok",   False)
    ok_llama = r_llama.get("ok", False)

    m1, m2, m3, m4 = st.columns(4)

    gem_time   = r_gem["time"]   if ok_gem   else None
    llama_time = r_llama["time"] if ok_llama else None

    with m1:
        g_t = fmt_time(gem_time) if gem_time is not None else "—"
        st.metric("⏱ Gemini Time", g_t)
    with m2:
        l_t = fmt_time(llama_time) if llama_time is not None else "—"
        st.metric("⏱ Llama 4 Time", l_t)
    with m3:
        g_w = word_count(r_gem["text"])   if ok_gem   else 0
        l_w = word_count(r_llama["text"]) if ok_llama else 0
        delta_w = g_w - l_w
        st.metric("📝 Gemini Words", g_w, delta=f"{delta_w:+d} vs Llama" if ok_llama else None)
    with m4:
        g_out = r_gem["tokens_out"]   if ok_gem   else 0
        l_out = r_llama["tokens_out"] if ok_llama else 0
        delta_tok = g_out - l_out
        st.metric("🔢 Gemini Out Tokens", g_out, delta=f"{delta_tok:+d} vs Llama" if ok_llama else None)

    if ok_gem and ok_llama:
        faster = "Gemini" if gem_time < llama_time else "Llama 4 Scout"
        longer = "Gemini" if word_count(r_gem["text"]) > word_count(r_llama["text"]) else "Llama 4 Scout"
        st.markdown(
            f"<div style='margin-top:0.8rem;padding:0.75rem 1rem;"
            f"background:rgba(139,92,246,0.08);border:1px solid rgba(139,92,246,0.18);"
            f"border-radius:10px;font-size:0.85rem;color:#a78bfa;'>"
            f"⚡ <strong>{faster}</strong> responded faster &nbsp;|&nbsp; "
            f"📄 <strong>{longer}</strong> gave a longer answer</div>",
            unsafe_allow_html=True,
        )

    # ── Save to history ──
    st.session_state.history.append({
        "ts":    datetime.datetime.now().strftime("%H:%M:%S"),
        "prompt": user_prompt[:120] + ("…" if len(user_prompt) > 120 else ""),
        "gem_ok": ok_gem,
        "llama_ok": ok_llama,
        "gem_time":  fmt_time(r_gem["time"])   if ok_gem   else "err",
        "llama_time": fmt_time(r_llama["time"]) if ok_llama else "err",
        "gem_words":   word_count(r_gem["text"])   if ok_gem   else 0,
        "llama_words": word_count(r_llama["text"]) if ok_llama else 0,
    })

# ── Empty state (no results yet) ──
elif not compare_clicked:
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(render_badge("Gemini 2.0 Flash", "badge-gemini"), unsafe_allow_html=True)
        placeholder = "Add Gemini key to enable" if not gemini_key else "Enter a prompt and click Compare"
        st.markdown(f'<div class="response-placeholder">✦ {placeholder}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(render_badge("Llama 4 Scout 17B", "badge-llama"), unsafe_allow_html=True)
        placeholder = "Add Groq key to enable" if not groq_key else "Enter a prompt and click Compare"
        st.markdown(f'<div class="response-placeholder">◈ {placeholder}</div>', unsafe_allow_html=True)


# ─── Session history ─────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)

if st.session_state.history:
    with st.expander(f"📜 Session History  ({len(st.session_state.history)} comparisons)", expanded=False):
        if st.button("🗑 Clear History", key="clear_hist"):
            st.session_state.history = []
            st.rerun()

        for i, h in enumerate(reversed(st.session_state.history), 1):
            gem_info   = f"⏱ {h['gem_time']} · {h['gem_words']} words"   if h["gem_ok"]   else "❌ error"
            llama_info = f"⏱ {h['llama_time']} · {h['llama_words']} words" if h["llama_ok"] else "❌ error"
            st.markdown(
                f"""<div class="history-card">
<div class="history-prompt">#{i} · {h['ts']} — {h['prompt']}</div>
<span style='color:#93c5fd;font-size:0.8rem;'>✦ Gemini: {gem_info}</span> &nbsp;|&nbsp;
<span style='color:#67e8f9;font-size:0.8rem;'>◈ Llama 4: {llama_info}</span>
</div>""",
                unsafe_allow_html=True,
            )
