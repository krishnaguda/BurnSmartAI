import streamlit as st
import time
import concurrent.futures
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BurnSmartAI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

  /* ── Root palette ── */
  :root {
    --bg-void:      #070710;
    --bg-glass:     rgba(255,255,255,0.04);
    --bg-glass2:    rgba(255,255,255,0.07);
    --border:       rgba(255,255,255,0.08);
    --border-hot:   rgba(139,92,246,0.45);
    --purple:       #8B5CF6;
    --purple-glow:  rgba(139,92,246,0.25);
    --gemini:       #4285F4;
    --llama:        #F97316;
    --text-primary: #F0EEF8;
    --text-muted:   #8B8BA8;
    --text-dim:     #4A4A6A;
    --mono:         'Space Mono', monospace;
    --sans:         'Syne', sans-serif;
  }

  /* ── Global resets ── */
  html, body, [class*="css"] {
    font-family: var(--sans) !important;
    color: var(--text-primary) !important;
  }
  .stApp {
    background: var(--bg-void) !important;
    background-image:
      radial-gradient(ellipse 80% 60% at 20% 10%, rgba(139,92,246,0.08) 0%, transparent 60%),
      radial-gradient(ellipse 60% 50% at 80% 90%, rgba(66,133,244,0.06) 0%, transparent 55%) !important;
    min-height: 100vh;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: rgba(10,10,22,0.95) !important;
    border-right: 1px solid var(--border) !important;
    backdrop-filter: blur(20px);
  }
  [data-testid="stSidebar"] * { color: var(--text-primary) !important; }
  [data-testid="stSidebar"] .stSlider > div > div > div {
    background: var(--purple) !important;
  }
  [data-testid="stSidebarContent"] { padding-top: 1.5rem !important; }

  /* ── Main title ── */
  .burnsmart-title {
    font-family: var(--sans);
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.05;
    background: linear-gradient(135deg, #fff 0%, #C4B5FD 40%, var(--purple) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
  }
  .burnsmart-sub {
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--text-muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
  }

  /* ── Glass card ── */
  .glass-card {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(12px);
    transition: border-color 0.3s ease;
  }
  .glass-card:hover { border-color: var(--border-hot); }

  /* ── Model header badges ── */
  .model-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 999px;
    font-family: var(--mono);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 1rem;
  }
  .badge-gemini {
    background: rgba(66,133,244,0.15);
    border: 1px solid rgba(66,133,244,0.4);
    color: #7FB3FA !important;
  }
  .badge-llama {
    background: rgba(249,115,22,0.15);
    border: 1px solid rgba(249,115,22,0.4);
    color: #FBA96A !important;
  }
  .badge-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    animation: pulse-dot 2s infinite;
  }
  .dot-gemini { background: #4285F4; box-shadow: 0 0 6px #4285F4; }
  .dot-llama  { background: #F97316; box-shadow: 0 0 6px #F97316; }
  @keyframes pulse-dot {
    0%,100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.5; transform: scale(0.7); }
  }

  /* ── Response box ── */
  .response-box {
    background: rgba(255,255,255,0.025);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem 1.4rem;
    font-size: 0.92rem;
    line-height: 1.75;
    color: var(--text-primary);
    min-height: 200px;
    white-space: pre-wrap;
    word-break: break-word;
  }
  .response-placeholder {
    background: rgba(255,255,255,0.02);
    border: 1px dashed var(--border);
    border-radius: 12px;
    padding: 2.5rem 1.5rem;
    text-align: center;
    color: var(--text-dim);
    font-family: var(--mono);
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    min-height: 160px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* ── Stats caption ── */
  .stats-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-top: 0.85rem;
  }
  .stat-chip {
    font-family: var(--mono);
    font-size: 0.68rem;
    color: var(--text-muted);
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 3px 9px;
    white-space: nowrap;
  }

  /* ── Divider ── */
  .section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2rem 0;
  }

  /* ── Metric cards ── */
  [data-testid="stMetric"] {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
  }
  [data-testid="stMetric"] label {
    font-family: var(--mono) !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
  }
  [data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: var(--sans) !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
  }
  [data-testid="stMetricDelta"] {
    font-family: var(--mono) !important;
    font-size: 0.7rem !important;
  }

  /* ── Buttons ── */
  .stButton > button {
    font-family: var(--sans) !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
  }
  .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--purple), #6D28D9) !important;
    border: none !important;
    color: #fff !important;
    box-shadow: 0 4px 20px var(--purple-glow) !important;
  }
  .stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 28px rgba(139,92,246,0.45) !important;
    transform: translateY(-1px) !important;
  }

  /* ── Text inputs / textarea ── */
  .stTextInput input, .stTextArea textarea {
    background: var(--bg-glass2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: var(--sans) !important;
  }
  .stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--purple) !important;
    box-shadow: 0 0 0 3px var(--purple-glow) !important;
  }

  /* ── Expander ── */
  [data-testid="stExpander"] {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden;
  }
  [data-testid="stExpander"] summary {
    font-family: var(--mono) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    padding: 0.75rem 1rem !important;
  }

  /* ── Sidebar label ── */
  .sidebar-section-label {
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin: 1.2rem 0 0.4rem;
  }

  /* ── Template buttons ── */
  .template-grid { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }

  /* ── History item ── */
  .history-item {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.82rem;
  }
  .history-prompt {
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.3rem;
    font-size: 0.85rem;
  }
  .history-meta {
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--text-dim);
    letter-spacing: 0.06em;
  }

  /* ── Spinner override ── */
  .stSpinner > div { border-top-color: var(--purple) !important; }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: var(--purple); }
</style>
""", unsafe_allow_html=True)


# ── Session state init ─────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "prompt_text" not in st.session_state:
    st.session_state.prompt_text = ""


# ── Prompt templates ───────────────────────────────────────────────────────────
TEMPLATES = {
    "⚡ Code Explain": "Explain the following concept with a clear, concise example in Python: {topic}. Walk me through the code line-by-line.",
    "✍️ Writing Help": "Help me write a compelling introduction paragraph for an essay about {topic}. Make it hook the reader immediately.",
    "📊 Analysis": "Analyze the key trends, opportunities, and risks related to {topic}. Structure your response with clear sections.",
    "🧠 Brainstorm": "Generate 10 creative and unconventional ideas related to {topic}. Push beyond the obvious. Be bold.",
    "🔬 Research": "Give me a deep-dive overview of {topic}, covering its history, current state, and future outlook. Cite key facts.",
}


# ── API call functions ─────────────────────────────────────────────────────────
def call_gemini(prompt: str, system_prompt: str, key: str, temp: float, max_tok: int) -> dict:
    start = time.time()
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=key)
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt.strip() else prompt

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                temperature=temp,
                max_output_tokens=max_tok,
            ),
        )
        elapsed = time.time() - start
        return {
            "ok": True,
            "text": response.text,
            "time": elapsed,
            "tokens_in": response.usage_metadata.prompt_token_count,
            "tokens_out": response.usage_metadata.candidates_token_count,
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "time": time.time() - start}


def call_llama(prompt: str, system_prompt: str, key: str, temp: float, max_tok: int) -> dict:
    start = time.time()
    try:
        from groq import Groq

        client = Groq(api_key=key)
        messages = []
        if system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            max_tokens=max_tok,
            temperature=temp,
            messages=messages,
        )
        elapsed = time.time() - start
        return {
            "ok": True,
            "text": response.choices[0].message.content,
            "time": elapsed,
            "tokens_in": response.usage.prompt_tokens,
            "tokens_out": response.usage.completion_tokens,
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "time": time.time() - start}


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:1.25rem;font-weight:800;
         background:linear-gradient(135deg,#fff,#8B5CF6);-webkit-background-clip:text;
         -webkit-text-fill-color:transparent;background-clip:text;margin-bottom:0.1rem;">
         🔍 BurnSmartAI
    </div>
    <div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#4A4A6A;
         letter-spacing:0.14em;text-transform:uppercase;margin-bottom:1.5rem;">
         Model Arena · v1.0
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">🔑 API Keys</div>', unsafe_allow_html=True)
    gemini_key = st.text_input("Gemini API Key", type="password", placeholder="AIza...", key="gemini_key")
    groq_key   = st.text_input("Groq API Key",   type="password", placeholder="gsk_...",  key="groq_key")

    st.markdown('<div class="sidebar-section-label">⚙️ Generation Settings</div>', unsafe_allow_html=True)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05, help="Higher = more creative")
    max_tokens  = st.slider("Max Tokens",  100, 4000, 1024, 50,  help="Maximum response length")

    st.markdown('<div class="sidebar-section-label">ℹ️ Get Free Keys</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:0.65rem;color:#4A4A6A;line-height:1.8;">
    🔵 <a href="https://aistudio.google.com/apikey" target="_blank"
         style="color:#4285F4;text-decoration:none;">Gemini → aistudio.google.com</a><br>
    🟠 <a href="https://console.groq.com/keys" target="_blank"
         style="color:#F97316;text-decoration:none;">Groq → console.groq.com</a>
    </div>
    """, unsafe_allow_html=True)


# ── Main area ──────────────────────────────────────────────────────────────────
st.markdown('<div class="burnsmart-title">🔍 BurnSmartAI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="burnsmart-sub">Simultaneous AI model comparison · Gemini vs Llama 4 Scout</div>',
    unsafe_allow_html=True,
)

# System prompt
with st.expander("🧬 System Prompt (optional)"):
    system_prompt = st.text_area(
        "System instructions",
        placeholder="You are a helpful, concise assistant. Answer clearly and thoroughly.",
        height=90,
        label_visibility="collapsed",
    )

# Prompt templates
with st.expander("⚡ Prompt Templates"):
    st.markdown(
        '<div style="font-family:\'Space Mono\',monospace;font-size:0.65rem;color:#4A4A6A;'
        'margin-bottom:0.6rem;">Click to populate prompt area</div>',
        unsafe_allow_html=True,
    )
    cols_t = st.columns(len(TEMPLATES))
    for i, (label, tpl) in enumerate(TEMPLATES.items()):
        with cols_t[i]:
            if st.button(label, use_container_width=True):
                st.session_state.prompt_text = tpl

# Prompt input
prompt = st.text_area(
    "Your Prompt",
    value=st.session_state.prompt_text,
    placeholder="Ask anything — compare how each model thinks, writes, and reasons...",
    height=130,
    label_visibility="collapsed",
    key="main_prompt",
)

compare_btn = st.button("⚡ Compare Models", type="primary", use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


# ── Results rendering helper ───────────────────────────────────────────────────
def render_response_col(result: dict | None, model_name: str, badge_class: str, dot_class: str, placeholder_msg: str):
    st.markdown(
        f'<div class="model-badge {badge_class}">'
        f'<span class="badge-dot {dot_class}"></span>{model_name}</div>',
        unsafe_allow_html=True,
    )
    if result is None:
        st.markdown(f'<div class="response-placeholder">{placeholder_msg}</div>', unsafe_allow_html=True)
    elif not result["ok"]:
        st.error(f"⚠️ {result['error']}")
    else:
        st.markdown(f'<div class="response-box">{result["text"]}</div>', unsafe_allow_html=True)
        words = len(result["text"].split())
        st.markdown(
            f'<div class="stats-row">'
            f'<span class="stat-chip">⏱ {result["time"]:.2f}s</span>'
            f'<span class="stat-chip">▲ {result["tokens_in"]} in</span>'
            f'<span class="stat-chip">▼ {result["tokens_out"]} out</span>'
            f'<span class="stat-chip">📝 {words} words</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ── Comparison logic ───────────────────────────────────────────────────────────
results_gemini = None
results_llama  = None

if compare_btn and prompt.strip():
    with st.spinner("Querying models in parallel…"):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
            fut_gemini = ex.submit(
                call_gemini, prompt, system_prompt if "system_prompt" in dir() else "",
                gemini_key, temperature, max_tokens
            ) if gemini_key else None

            fut_llama = ex.submit(
                call_llama, prompt, system_prompt if "system_prompt" in dir() else "",
                groq_key, temperature, max_tokens
            ) if groq_key else None

            results_gemini = fut_gemini.result() if fut_gemini else None
            results_llama  = fut_llama.result()  if fut_llama  else None

    # Save to history
    st.session_state.history.insert(0, {
        "ts": datetime.now().strftime("%H:%M:%S"),
        "prompt": prompt[:120] + ("…" if len(prompt) > 120 else ""),
        "gemini_ok": results_gemini["ok"] if results_gemini else False,
        "llama_ok":  results_llama["ok"]  if results_llama  else False,
        "gemini_time": results_gemini.get("time", 0) if results_gemini else 0,
        "llama_time":  results_llama.get("time", 0)  if results_llama  else 0,
    })

elif compare_btn:
    st.warning("Please enter a prompt before comparing.")


# ── Results columns ────────────────────────────────────────────────────────────
col_g, col_l = st.columns(2, gap="large")

with col_g:
    render_response_col(
        results_gemini, "Gemini 2.0 Flash", "badge-gemini", "dot-gemini",
        "🔵 Add Gemini API key to enable" if not gemini_key else "⏳ Awaiting comparison…",
    )

with col_l:
    render_response_col(
        results_llama, "Llama 4 Scout 17B", "badge-llama", "dot-llama",
        "🟠 Add Groq API key to enable" if not groq_key else "⏳ Awaiting comparison…",
    )


# ── Comparison metrics ─────────────────────────────────────────────────────────
if results_gemini and results_llama and results_gemini["ok"] and results_llama["ok"]:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:\'Space Mono\',monospace;font-size:0.65rem;color:#4A4A6A;'
        'letter-spacing:0.14em;text-transform:uppercase;margin-bottom:0.8rem;">📊 Comparison Metrics</div>',
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4, m5, m6 = st.columns(6)

    faster = "Gemini" if results_gemini["time"] < results_llama["time"] else "Llama 4"
    speed_delta = abs(results_gemini["time"] - results_llama["time"])

    with m1:
        st.metric("⚡ Gemini Speed", f'{results_gemini["time"]:.2f}s',
                  delta="faster" if faster == "Gemini" else f'+{speed_delta:.2f}s slower')
    with m2:
        st.metric("⚡ Llama Speed", f'{results_llama["time"]:.2f}s',
                  delta="faster" if faster == "Llama 4" else f'+{speed_delta:.2f}s slower')
    with m3:
        st.metric("🔵 Gemini Tokens Out", results_gemini["tokens_out"])
    with m4:
        st.metric("🟠 Llama Tokens Out", results_llama["tokens_out"])
    with m5:
        st.metric("🔵 Gemini Words", len(results_gemini["text"].split()))
    with m6:
        st.metric("🟠 Llama Words", len(results_llama["text"].split()))


# ── Session history ────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    with st.expander(f"🕒 Session History ({len(st.session_state.history)} comparisons)"):
        for item in st.session_state.history:
            g_badge = "✅" if item["gemini_ok"] else "❌"
            l_badge = "✅" if item["llama_ok"]  else "❌"
            st.markdown(
                f'<div class="history-item">'
                f'<div class="history-prompt">"{item["prompt"]}"</div>'
                f'<div class="history-meta">'
                f'🕐 {item["ts"]} &nbsp;|&nbsp; '
                f'Gemini {g_badge} {item["gemini_time"]:.2f}s &nbsp;|&nbsp; '
                f'Llama {l_badge} {item["llama_time"]:.2f}s'
                f'</div></div>',
                unsafe_allow_html=True,
            )
        if st.button("🗑 Clear History", key="clear_history"):
            st.session_state.history = []
            st.rerun()
