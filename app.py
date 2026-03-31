import streamlit as st
import time
import threading
from datetime import datetime

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BurnSmartAI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Global ── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  .stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #12101e 50%, #0d1117 100%);
    color: #e2e8f0;
  }

  /* ── Hide default Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: rgba(17, 15, 30, 0.95) !important;
    border-right: 1px solid rgba(139, 92, 246, 0.2);
    backdrop-filter: blur(20px);
  }

  [data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem;
  }

  /* ── Main container ── */
  .main .block-container {
    padding: 2rem 2.5rem;
    max-width: 1400px;
  }

  /* ── Title ── */
  .burn-title {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #8B5CF6 0%, #a78bfa 50%, #22D3EE 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
    line-height: 1.1;
  }

  .burn-subtitle {
    color: #94a3b8;
    font-size: 1rem;
    font-weight: 400;
    margin-top: 0.25rem;
    letter-spacing: 0.01em;
  }

  /* ── Model badge headers ── */
  .model-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    margin-bottom: 12px;
  }

  .badge-gemini {
    background: rgba(66, 133, 244, 0.15);
    border: 1px solid rgba(66, 133, 244, 0.4);
    color: #60a5fa;
  }

  .badge-llama {
    background: rgba(34, 211, 238, 0.12);
    border: 1px solid rgba(34, 211, 238, 0.35);
    color: #22D3EE;
  }

  /* ── Response boxes ── */
  .response-box {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.25rem 1.4rem;
    min-height: 220px;
    line-height: 1.7;
    font-size: 0.93rem;
    color: #cbd5e1;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
    white-space: pre-wrap;
    word-break: break-word;
    transition: border-color 0.3s ease;
  }

  .response-box:hover {
    border-color: rgba(139, 92, 246, 0.25);
  }

  .response-box.gemini-box {
    border-top: 2px solid rgba(66, 133, 244, 0.5);
  }

  .response-box.llama-box {
    border-top: 2px solid rgba(34, 211, 238, 0.5);
  }

  .response-box.placeholder-box {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #475569;
    font-style: italic;
    font-size: 0.88rem;
    border-style: dashed;
  }

  /* ── Stats caption ── */
  .stats-caption {
    display: flex;
    gap: 16px;
    margin-top: 10px;
    padding: 8px 12px;
    background: rgba(0,0,0,0.2);
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.05);
    font-size: 0.78rem;
    color: #64748b;
  }

  .stats-item {
    display: flex;
    align-items: center;
    gap: 5px;
  }

  .stats-icon { font-size: 0.85rem; }

  /* ── Compare button ── */
  .stButton > button {
    background: linear-gradient(135deg, #7c3aed, #8B5CF6, #6d28d9) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.35) !important;
    width: 100% !important;
  }

  .stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5) !important;
  }

  .stButton > button:active {
    transform: translateY(0px) !important;
  }

  /* ── Template buttons ── */
  .template-btn > button {
    background: rgba(139, 92, 246, 0.08) !important;
    border: 1px solid rgba(139, 92, 246, 0.25) !important;
    color: #a78bfa !important;
    border-radius: 8px !important;
    font-size: 0.8rem !important;
    padding: 0.35rem 0.8rem !important;
    font-weight: 500 !important;
    width: auto !important;
    box-shadow: none !important;
  }

  .template-btn > button:hover {
    background: rgba(139, 92, 246, 0.18) !important;
    border-color: rgba(139, 92, 246, 0.5) !important;
    transform: none !important;
    box-shadow: none !important;
  }

  /* ── Inputs ── */
  .stTextArea > div > div > textarea {
    background: rgba(15, 13, 27, 0.8) !important;
    border: 1px solid rgba(139, 92, 246, 0.25) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-size: 0.93rem !important;
    transition: border-color 0.2s ease !important;
  }

  .stTextArea > div > div > textarea:focus {
    border-color: rgba(139, 92, 246, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
  }

  .stTextInput > div > div > input {
    background: rgba(15, 13, 27, 0.8) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
  }

  /* ── Sliders ── */
  .stSlider > div > div > div {
    color: #8B5CF6 !important;
  }

  /* ── Expanders ── */
  .streamlit-expanderHeader {
    background: rgba(139, 92, 246, 0.06) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(139, 92, 246, 0.15) !important;
    color: #a78bfa !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
  }

  /* ── Metric cards ── */
  [data-testid="stMetric"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    backdrop-filter: blur(10px);
  }

  [data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.78rem !important; }
  [data-testid="stMetricValue"] { color: #e2e8f0 !important; font-size: 1.5rem !important; font-weight: 600 !important; }

  /* ── Divider ── */
  .custom-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.07);
    margin: 1.5rem 0;
  }

  /* ── Section labels ── */
  .section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.5rem;
  }

  /* ── History entry ── */
  .history-entry {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.82rem;
    color: #94a3b8;
  }

  .history-timestamp {
    font-size: 0.72rem;
    color: #475569;
    margin-bottom: 4px;
  }

  /* ── Error box ── */
  .error-box {
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 10px;
    padding: 1rem;
    color: #fca5a5;
    font-size: 0.88rem;
  }

  /* ── Sidebar key label ── */
  .key-label {
    font-size: 0.78rem;
    color: #64748b;
    margin-bottom: 2px;
  }

  .sidebar-section-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4B5563;
    margin: 1.2rem 0 0.6rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
  }
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "prompt_text" not in st.session_state:
    st.session_state.prompt_text = ""


# ─── API Helpers ──────────────────────────────────────────────────────────────
def call_gemini(key: str, prompt: str, system_prompt: str, temp: float, max_tok: int) -> dict:
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=key)
        full_prompt = f"{system_prompt}\n\n{prompt}".strip() if system_prompt else prompt

        t0 = time.time()
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                temperature=temp,
                max_output_tokens=max_tok,
            ),
        )
        elapsed = time.time() - t0

        text = response.text
        tokens_in = response.usage_metadata.prompt_token_count
        tokens_out = response.usage_metadata.candidates_token_count

        return {"ok": True, "text": text, "tokens_in": tokens_in, "tokens_out": tokens_out, "elapsed": elapsed}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def call_llama(key: str, prompt: str, system_prompt: str, temp: float, max_tok: int) -> dict:
    try:
        from groq import Groq

        client = Groq(api_key=key)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        t0 = time.time()
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            max_tokens=max_tok,
            temperature=temp,
            messages=messages,
        )
        elapsed = time.time() - t0

        text = response.choices[0].message.content
        tokens_in = response.usage.prompt_tokens
        tokens_out = response.usage.completion_tokens

        return {"ok": True, "text": text, "tokens_in": tokens_in, "tokens_out": tokens_out, "elapsed": elapsed}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def run_parallel(gemini_key, groq_key, prompt, system_prompt, temp, max_tok):
    results = {"gemini": None, "llama": None}

    def run_g():
        results["gemini"] = call_gemini(gemini_key, prompt, system_prompt, temp, max_tok)

    def run_l():
        results["llama"] = call_llama(groq_key, prompt, system_prompt, temp, max_tok)

    threads = []
    if gemini_key:
        t = threading.Thread(target=run_g)
        threads.append(t)
        t.start()
    else:
        results["gemini"] = None

    if groq_key:
        t = threading.Thread(target=run_l)
        threads.append(t)
        t.start()
    else:
        results["llama"] = None

    for t in threads:
        t.join()

    return results


# ─── Prompt Templates ─────────────────────────────────────────────────────────
TEMPLATES = {
    "⚡ Code Explainer": "Explain this code snippet step by step, including what it does, why it works, and any potential improvements:\n\n```python\ndef fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n```",
    "✍️ Writing Help": "Help me improve this paragraph for clarity, conciseness, and impact. Explain what you changed and why:\n\n'The thing that we need to do is to make sure that all of the different parts of the project are working together in a way that is good and efficient for everyone involved in the process.'",
    "📊 Analysis": "Analyze the pros and cons of remote work vs. in-office work in 2025. Consider productivity, culture, mental health, and business outcomes. Provide a balanced, evidence-based assessment.",
    "💡 Brainstorm": "Give me 10 creative, unconventional business ideas that combine AI with sustainability. For each idea, include the core concept, target market, and one key challenge to solve.",
    "🔬 Research": "Summarize the current state of quantum computing in 2025: key breakthroughs, major players, practical applications that exist today, and realistic timelines for widespread adoption.",
}


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="burn-title" style="font-size:1.5rem;">🔍 BurnSmartAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="burn-subtitle" style="font-size:0.78rem; margin-bottom:0.5rem;">Model Comparison Engine</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">🔑 API Keys</div>', unsafe_allow_html=True)

    gemini_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIza...",
        help="Get free key at aistudio.google.com",
    )
    groq_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get free key at console.groq.com — covers Llama 4 Scout",
    )

    st.markdown('<div class="sidebar-section-title">⚙️ Generation Settings</div>', unsafe_allow_html=True)

    temperature = st.slider(
        "Temperature",
        min_value=0.0, max_value=1.0,
        value=0.7, step=0.05,
        help="Higher = more creative, Lower = more deterministic",
    )
    max_tokens = st.slider(
        "Max Tokens",
        min_value=100, max_value=4000,
        value=1024, step=100,
        help="Maximum tokens per model response",
    )

    st.markdown('<div class="sidebar-section-title">ℹ️ About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.75rem; color:#475569; line-height:1.6;">
    Compare <strong style="color:#60a5fa;">Gemini 2.5 Flash</strong> vs 
    <strong style="color:#22D3EE;">Llama 4 Scout 17B</strong> side-by-side.<br><br>
    Both APIs have generous free tiers — no credit card needed.
    </div>
    """, unsafe_allow_html=True)


# ─── Main Area ────────────────────────────────────────────────────────────────
st.markdown('<div class="burn-title">🔍 BurnSmartAI</div>', unsafe_allow_html=True)
st.markdown('<div class="burn-subtitle">Compare AI model responses side-by-side — speed, quality, and token efficiency at a glance.</div>', unsafe_allow_html=True)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# System prompt
with st.expander("🛠️ System Prompt (optional)"):
    system_prompt = st.text_area(
        "System instructions",
        placeholder="e.g. You are a concise technical expert. Always use bullet points. Avoid repetition.",
        height=90,
        label_visibility="collapsed",
    )

# Prompt templates
with st.expander("📋 Prompt Templates — click to load"):
    cols = st.columns(len(TEMPLATES))
    for i, (label, tmpl) in enumerate(TEMPLATES.items()):
        with cols[i]:
            st.markdown('<div class="template-btn">', unsafe_allow_html=True)
            if st.button(label, key=f"tmpl_{i}"):
                st.session_state.prompt_text = tmpl
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# Main prompt
prompt = st.text_area(
    "Your Prompt",
    value=st.session_state.prompt_text,
    placeholder="Ask anything… compare how Gemini and Llama respond to the same question.",
    height=140,
    label_visibility="collapsed",
)

# Compare button
compare_clicked = st.button("⚡ Compare Models", type="primary")

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


# ─── Results ──────────────────────────────────────────────────────────────────
if compare_clicked:
    if not prompt.strip():
        st.warning("Please enter a prompt before comparing.")
    elif not gemini_key and not groq_key:
        st.error("Please add at least one API key in the sidebar to run a comparison.")
    else:
        with st.spinner("🚀 Querying models in parallel…"):
            sp = system_prompt if "system_prompt" in dir() else ""
            results = run_parallel(gemini_key, groq_key, prompt.strip(), sp, temperature, max_tokens)

        # Save to history
        st.session_state.history.insert(0, {
            "timestamp": datetime.now().strftime("%H:%M:%S · %b %d"),
            "prompt": prompt.strip()[:120] + ("…" if len(prompt.strip()) > 120 else ""),
            "gemini_ok": results["gemini"] is not None and results["gemini"].get("ok"),
            "llama_ok": results["llama"] is not None and results["llama"].get("ok"),
        })

        # ── Column layout ──────────────────────────────────────────────────────
        col1, col2 = st.columns(2)

        # Helper
        def render_column(col, result, provider, badge_class, color_hex, box_class, icon):
            with col:
                st.markdown(f'<div class="model-badge {badge_class}">{icon} {provider}</div>', unsafe_allow_html=True)

                if result is None:
                    st.markdown(f'<div class="response-box placeholder-box">Add {provider.split(" ")[0]} key to enable</div>', unsafe_allow_html=True)
                elif not result["ok"]:
                    st.markdown(f'<div class="error-box">❌ <strong>Error:</strong> {result["error"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="response-box {box_class}">{result["text"]}</div>', unsafe_allow_html=True)
                    words = len(result["text"].split())
                    st.markdown(f"""
                    <div class="stats-caption">
                      <span class="stats-item"><span class="stats-icon">⏱</span> {result['elapsed']:.2f}s</span>
                      <span class="stats-item"><span class="stats-icon">📥</span> {result['tokens_in']:,} in</span>
                      <span class="stats-item"><span class="stats-icon">📤</span> {result['tokens_out']:,} out</span>
                      <span class="stats-item"><span class="stats-icon">📝</span> {words:,} words</span>
                    </div>
                    """, unsafe_allow_html=True)

        render_column(col1, results["gemini"], "Gemini 2.5 Flash", "badge-gemini", "#4285F4", "gemini-box", "✦")
        render_column(col2, results["llama"],  "Llama 4 Scout 17B", "badge-llama",  "#22D3EE", "llama-box",  "◈")

        # ── Comparison Metrics ─────────────────────────────────────────────────
        g = results.get("gemini")
        l = results.get("llama")

        if g and g.get("ok") and l and l.get("ok"):
            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">📊 Head-to-Head Metrics</div>', unsafe_allow_html=True)

            m1, m2, m3, m4 = st.columns(4)

            faster = "Gemini" if g["elapsed"] < l["elapsed"] else "Llama 4"
            speed_delta = abs(g["elapsed"] - l["elapsed"])

            g_words = len(g["text"].split())
            l_words = len(l["text"].split())
            more_words = "Gemini" if g_words > l_words else "Llama 4"

            m1.metric("⏱ Gemini Speed", f"{g['elapsed']:.2f}s", delta=f"{'faster' if g['elapsed'] < l['elapsed'] else 'slower'} by {speed_delta:.2f}s")
            m2.metric("⏱ Llama 4 Speed", f"{l['elapsed']:.2f}s", delta=f"{'faster' if l['elapsed'] < g['elapsed'] else 'slower'} by {speed_delta:.2f}s")
            m3.metric("📤 Output Tokens", f"{g['tokens_out']:,} G  ·  {l['tokens_out']:,} L", delta=f"Δ {abs(g['tokens_out']-l['tokens_out'])}")
            m4.metric("📝 Word Count", f"{g_words:,} G  ·  {l_words:,} L", delta=f"{more_words} wrote more")

        elif (g and g.get("ok")) or (l and l.get("ok")):
            # Only one model responded
            active = g if (g and g.get("ok")) else l
            label = "Gemini" if active is g else "Llama 4 Scout"
            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            m1.metric("⏱ Response Time", f"{active['elapsed']:.2f}s")
            m2.metric("📥 Input Tokens", f"{active['tokens_in']:,}")
            m3.metric("📤 Output Tokens", f"{active['tokens_out']:,}")

else:
    # Placeholder state — show what the columns will look like
    if not compare_clicked:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="model-badge badge-gemini">✦ Gemini 2.5 Flash</div>', unsafe_allow_html=True)
            st.markdown('<div class="response-box placeholder-box">Response will appear here after comparing…</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="model-badge badge-llama">◈ Llama 4 Scout 17B</div>', unsafe_allow_html=True)
            st.markdown('<div class="response-box placeholder-box">Response will appear here after comparing…</div>', unsafe_allow_html=True)


# ─── Session History ──────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    with st.expander(f"🕐 Session History ({len(st.session_state.history)} comparisons)"):
        for entry in st.session_state.history[:20]:
            g_icon = "✅" if entry.get("gemini_ok") else ("⚠️" if not entry.get("gemini_ok") else "⬜")
            l_icon = "✅" if entry.get("llama_ok") else ("⚠️" if not entry.get("llama_ok") else "⬜")
            st.markdown(f"""
            <div class="history-entry">
              <div class="history-timestamp">🕐 {entry['timestamp']} · Gemini {g_icon} · Llama 4 {l_icon}</div>
              <div>{entry['prompt']}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑 Clear History", key="clear_hist"):
            st.session_state.history = []
            st.rerun()
