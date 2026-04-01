"""
╔══════════════════════════════════════════════════════════════╗
║           Deep Dive Research Engine — app.py                 ║
║   Dual-AI: Gemini (Research) × Llama 4 Scout (Analysis)     ║
║   Cross-verified insights → structured markdown document     ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
from datetime import datetime
import time

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be the very first Streamlit call)
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Deep Dive Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",   # sidebar starts minimised
)


# ──────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ──────────────────────────────────────────────────────────────────────────────
def inject_css() -> None:
    st.markdown(
        """
        <style>
        /* ── Base ── */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0d0b1e 0%, #1a1535 50%, #0f1729 100%);
            min-height: 100vh;
        }
        [data-testid="stHeader"] { background: transparent; }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background: rgba(15, 12, 35, 0.97) !important;
            border-right: 1px solid rgba(102, 126, 234, 0.2);
        }

        /* ── Typography ── */
        .main-title {
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(120deg, #667eea, #a78bfa, #f093fb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            line-height: 1.15;
            margin-bottom: 0.3rem;
        }
        .main-subtitle {
            text-align: center;
            color: #9ca3af;
            font-size: 1.05rem;
            margin-bottom: 0.5rem;
        }

        /* ── Cards ── */
        .glass-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            margin: 0.8rem 0;
            backdrop-filter: blur(12px);
        }

        /* ── Divider ── */
        .glow-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(102,126,234,0.6), transparent);
            margin: 1.6rem 0;
        }

        /* ── Verification card ── */
        .verify-card {
            background: rgba(102,126,234,0.07);
            border: 1px solid rgba(102,126,234,0.25);
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            margin: 0.8rem 0;
        }

        /* ── Status pills ── */
        .pill-confirmed {
            background: rgba(16,185,129,0.18);
            color: #34d399;
            border: 1px solid rgba(16,185,129,0.35);
            padding: 0.2rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .pill-refined {
            background: rgba(245,158,11,0.18);
            color: #fbbf24;
            border: 1px solid rgba(245,158,11,0.35);
            padding: 0.2rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .pill-contradicted {
            background: rgba(239,68,68,0.18);
            color: #f87171;
            border: 1px solid rgba(239,68,68,0.35);
            padding: 0.2rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .pill-unknown {
            background: rgba(156,163,175,0.18);
            color: #9ca3af;
            border: 1px solid rgba(156,163,175,0.35);
            padding: 0.2rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        /* ── Model badges ── */
        .badge-gemini {
            background: linear-gradient(135deg,#4285f4,#34a853);
            color:#fff;
            padding: 0.15rem 0.55rem;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 700;
        }
        .badge-llama {
            background: linear-gradient(135deg,#f7931e,#8b5cf6);
            color:#fff;
            padding: 0.15rem 0.55rem;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 700;
        }

        /* ── Buttons ── */
        .stButton > button {
            background: linear-gradient(135deg,#667eea,#764ba2) !important;
            color: #fff !important;
            border: none !important;
            border-radius: 9px !important;
            font-weight: 700 !important;
            transition: transform .2s, box-shadow .2s !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(102,126,234,0.45) !important;
        }
        .stButton > button:disabled {
            opacity: 0.45 !important;
            cursor: not-allowed !important;
        }

        /* ── Download button ── */
        .stDownloadButton > button {
            background: linear-gradient(135deg,#10b981,#059669) !important;
            color: #fff !important;
            border: none !important;
            border-radius: 9px !important;
            font-weight: 700 !important;
        }

        /* ── Metrics ── */
        [data-testid="stMetric"] {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 10px;
            padding: 0.8rem 1rem;
        }

        /* ── Tabs ── */
        [data-testid="stTabs"] button {
            font-weight: 600;
        }

        /* ── Expander ── */
        [data-testid="stExpander"] > div:first-child {
            background: rgba(255,255,255,0.04);
            border-radius: 8px;
        }

        /* ── Branding hide ── */
        #MainMenu, footer { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────────────────────────────────────
# SESSION STATE INITIALISATION
# ──────────────────────────────────────────────────────────────────────────────
def init_session_state() -> None:
    defaults = {
        "gemini_output": None,
        "llama_output": None,
        "verification": None,
        "final_doc": None,
        "current_topic": "",
        "research_complete": False,
        "sidebar_open": False,   # tracks sidebar toggle
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
def render_sidebar() -> tuple[str, str]:
    """Render sidebar controls; return (gemini_key, groq_key)."""
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        st.markdown("---")

        # ── API Keys ──────────────────────────────────────────────────────────
        st.markdown("### 🔑 API Keys")
        gemini_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="AIza...",
            help="Get yours → https://aistudio.google.com/app/apikey",
            key="sb_gemini_key",
        )
        groq_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Get yours → https://console.groq.com/keys",
            key="sb_groq_key",
        )

        # ── Live status ───────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 📡 Connection Status")
        c1, c2 = st.columns(2)
        c1.success("✅ Gemini") if gemini_key else c1.error("❌ Gemini")
        c2.success("✅ Groq")   if groq_key   else c2.error("❌ Groq")

        # ── Model info ────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 🤖 Models")
        st.markdown(
            """
| Role | Model | Provider |
|------|-------|----------|
| Research | Gemini 2.0 Flash | Google |
| Analysis | Llama 4 Scout 17B | Groq |
"""
        )

        # ── Tips ──────────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 💡 Good Topics")
        st.info(
            "• AI / ML frameworks\n"
            "• Cloud architectures\n"
            "• Programming paradigms\n"
            "• Distributed systems\n"
            "• Emerging technologies"
        )

        # ── Reset ─────────────────────────────────────────────────────────────
        st.markdown("---")
        if st.button("🗑️ Clear All Results", use_container_width=True):
            for k in ["gemini_output", "llama_output", "verification", "final_doc",
                      "research_complete", "current_topic"]:
                st.session_state[k] = False if k == "research_complete" else None
            st.session_state["current_topic"] = ""
            st.rerun()

    return gemini_key or "", groq_key or ""


# ──────────────────────────────────────────────────────────────────────────────
# AI FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────────

def run_gemini_research(topic: str, api_key: str) -> str:
    """
    Call Gemini 2.0 Flash to produce structured factual research.
    Returns markdown-formatted text or an error string starting with '❌'.
    """
    try:
        from google import genai  # pip install google-genai

        client = genai.Client(api_key=api_key)
        prompt = f"""
You are a world-class research assistant. Produce a thorough, factual deep-dive on the topic below.

**Topic:** {topic}

Structure your response with EXACTLY these sections:

### Gemini Research Output

**Definition & Overview:**
Precise, clear definition and a 2-3 paragraph high-level overview.

**Key Concepts (5-7):**
Number and explain each concept concisely.

**Industry Trends (2025–2026):**
Recent developments, data points, adoption statistics, and forward outlook.

**Technical Details:**
Mechanisms, architecture specifics, implementation considerations.

**Real-World Applications:**
At least 5 concrete use-cases with named companies or products where possible.

**Source-Style References:**
List 8+ authoritative sources: arXiv papers, official docs, industry reports, GitHub repos.

Be factual. Cite specific numbers and dates where available. Avoid vague generalisations.
"""
        response = client.models.generate_content(
            model="gemini-2.0-flash",   # adjust if you have access to a newer preview
            contents=prompt,
        )
        return response.text

    except ImportError:
        return "❌ Package missing: run `pip install google-genai`"
    except Exception as exc:
        return f"❌ Gemini API error: {exc}"


def run_llama_analysis(topic: str, api_key: str, gemini_context: str = "") -> str:
    """
    Call Llama 4 Scout 17B via Groq for deep reasoning and critical analysis.
    Returns markdown-formatted text or an error string starting with '❌'.
    """
    try:
        from groq import Groq  # pip install groq

        client = Groq(api_key=api_key)

        context_block = (
            f"\n\n**Prior research context (Gemini):**\n{gemini_context[:2500]}...\n"
            f"Build upon this with deeper, independent analysis.\n"
            if gemini_context else ""
        )

        prompt = f"""
You are an expert technical analyst and deep-reasoning engine.

**Topic:** {topic}
{context_block}

Provide your analysis with EXACTLY these sections:

### Llama Analysis Output

**Deep Reasoning & Architecture:**
Explain the underlying principles, design philosophy, and *why* things work the way they do—not just *what* they are.

**Technical Trade-offs:**
Detailed pros/cons table-style breakdown; situational analysis of when each trade-off matters.

**Critical Analysis:**
What is commonly misunderstood, oversimplified, or hype vs. reality?

**Comparative Analysis:**
How does this compare to leading alternatives? When is each the right choice?

**Edge Cases & Failure Modes:**
What breaks down at scale, under adversarial conditions, or in edge scenarios?

**Future Directions & Open Problems:**
Where is research/engineering heading? What remains unsolved?

Go deep. Be analytical. Challenge assumptions where warranted.
"""
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert technical analyst specialising in deep reasoning, "
                        "architecture critique, and critical analysis of complex systems."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.7,
            max_tokens=4096,
        )
        return completion.choices[0].message.content

    except ImportError:
        return "❌ Package missing: run `pip install groq`"
    except Exception as exc:
        return f"❌ Groq API error: {exc}"


def cross_verify_claim(gemini_output: str, topic: str, groq_key: str) -> dict:
    """
    1. Extract one key claim from Gemini's output.
    2. Have Llama verify / refine / contradict it.
    Returns a dict with keys: claim, result, explanation, confidence, nuance.
    """
    try:
        from groq import Groq

        client = Groq(api_key=groq_key)

        # ── Step 1: extract claim ─────────────────────────────────────────────
        extract_resp = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": (
                        f'From this research about "{topic}", extract ONE specific, '
                        f"verifiable, non-trivial factual claim.\n\n"
                        f"{gemini_output[:3000]}\n\n"
                        "Return ONLY the claim as a single sentence. No preamble."
                    ),
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.25,
            max_tokens=200,
        )
        claim = extract_resp.choices[0].message.content.strip().strip('"')

        # ── Step 2: verify claim ──────────────────────────────────────────────
        verify_resp = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""
Carefully evaluate this claim about "{topic}":

Claim: "{claim}"

Respond in this exact format (one item per line):
VERIFICATION_RESULT: <Confirmed | Refined | Contradicted>
EXPLANATION: <2-3 sentences>
CONFIDENCE_LEVEL: <High | Medium | Low>
NUANCE: <One sentence caveat or additional context>
""",
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.25,
            max_tokens=512,
        )
        raw = verify_resp.choices[0].message.content.strip()

        # ── Parse structured response ─────────────────────────────────────────
        parsed = {"result": "Unknown", "explanation": raw, "confidence": "Medium", "nuance": ""}
        for line in raw.splitlines():
            if line.startswith("VERIFICATION_RESULT:"):
                parsed["result"] = line.split(":", 1)[1].strip()
            elif line.startswith("EXPLANATION:"):
                parsed["explanation"] = line.split(":", 1)[1].strip()
            elif line.startswith("CONFIDENCE_LEVEL:"):
                parsed["confidence"] = line.split(":", 1)[1].strip()
            elif line.startswith("NUANCE:"):
                parsed["nuance"] = line.split(":", 1)[1].strip()

        return {"claim": claim, **parsed, "raw": raw}

    except Exception as exc:
        return {
            "claim": "Claim extraction failed",
            "result": "Error",
            "explanation": str(exc),
            "confidence": "N/A",
            "nuance": "",
            "raw": "",
        }


def generate_final_document(
    topic: str,
    gemini_output: str,
    llama_output: str,
    verification: dict,
    groq_key: str,
) -> str:
    """
    Use Llama to synthesise both model outputs into a fully structured
    'Deep Dive' markdown document with debrief section.
    Falls back to a template-assembled version on error.
    """
    try:
        from groq import Groq

        client = Groq(api_key=groq_key)
        today = datetime.now().strftime("%B %d, %Y")

        prompt = f"""
You are a world-class technical writer. Synthesise the research and analysis below
into a polished, comprehensive "Deep Dive" document in clean Markdown.

**Topic:** {topic}
**Date:** {today}

--- GEMINI RESEARCH ---
{gemini_output[:3000]}

--- LLAMA ANALYSIS ---
{llama_output[:3000]}

--- VERIFIED INSIGHT ---
Claim: {verification.get('claim','N/A')}
Result: {verification.get('result','N/A')}
Explanation: {verification.get('explanation','N/A')}
Confidence: {verification.get('confidence','N/A')}

Generate the document using EXACTLY this structure (keep all section numbers):

# Deep Dive: {topic}
*Generated: {today} | Powered by Gemini 2.0 Flash × Llama 4 Scout 17B*

---

## 1. Overview
[3-4 well-crafted paragraphs — clear, accurate, engaging]

## 2. Key Concepts
[7 concepts, each with a short but substantive explanation]

## 3. How It Works (Technical Breakdown)
[Detailed; use sub-headings where appropriate]

## 4. Practical Use Cases
[6+ real-world applications with context and named examples]

## 5. Trade-offs / Limitations

### ✅ Strengths
[Bulleted list]

### ⚠️ Limitations
[Bulleted list]

### 🚫 When NOT to Use It
[3+ concrete scenarios]

## 6. Tools & Ecosystem (2026)
[Libraries, platforms, cloud services, community resources]

## 7. Verified Insight
- **Claim:** {verification.get('claim','N/A')}
- **Verification Result:** {verification.get('result','N/A')}
- **Explanation:** {verification.get('explanation','N/A')}
- **Confidence Level:** {verification.get('confidence','N/A')}

## 8. Practical Takeaways
[6 actionable bullet points a practitioner should remember]

## 9. Sources Referenced
[12+ diverse sources: papers, docs, tools, blogs, companies]

---

## 🧾 Research Debrief

**Why Gemini was valuable:**
[Specific contribution — 2-3 sentences]

**Why Llama was valuable:**
[Specific contribution — 2-3 sentences]

**Areas of model disagreement:**
[Any divergence in perspective or emphasis]

**Hardest aspect of this topic to understand:**
[Honest assessment]

**Reusability of this research approach:**
[Yes/No + reasoning]

**What a deeper analysis would add:**
[3 concrete improvements]

---
*Deep Dive Research Engine | Dual-AI Cross-Verified*
"""

        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a world-class technical writer. Produce comprehensive, "
                        "accurate, well-structured Markdown documents with no filler."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.55,
            max_tokens=8192,
        )
        return completion.choices[0].message.content

    except Exception as exc:
        # ── Graceful fallback: assemble from raw outputs ───────────────────────
        today = datetime.now().strftime("%B %d, %Y")
        return f"""# Deep Dive: {topic}
*Generated: {today} | Powered by Gemini 2.0 Flash × Llama 4 Scout 17B*

---

## Gemini Research Output
{gemini_output}

---

## Llama Analysis Output
{llama_output}

---

## 7. Verified Insight
- **Claim:** {verification.get('claim','N/A')}
- **Verification Result:** {verification.get('result','N/A')}
- **Explanation:** {verification.get('explanation','N/A')}
- **Confidence Level:** {verification.get('confidence','N/A')}

---

> ⚠️ Final document synthesis encountered an error: `{exc}`.
> Raw model outputs are shown above. Please retry or download as-is.
"""


# ──────────────────────────────────────────────────────────────────────────────
# HELPER: verification pill HTML
# ──────────────────────────────────────────────────────────────────────────────
def _pill(result: str) -> str:
    r = result.lower()
    if "confirmed" in r:
        return f'<span class="pill-confirmed">✅ {result}</span>'
    if "refined" in r:
        return f'<span class="pill-refined">🔄 {result}</span>'
    if "contradicted" in r:
        return f'<span class="pill-contradicted">❌ {result}</span>'
    return f'<span class="pill-unknown">ℹ️ {result}</span>'


# ──────────────────────────────────────────────────────────────────────────────
# MAIN APPLICATION
# ──────────────────────────────────────────────────────────────────────────────
def main() -> None:
    inject_css()
    init_session_state()

    # ── Sidebar ──────────────────────────────────────────────────────────────
    gemini_key, groq_key = render_sidebar()

    # ── Hero Header ──────────────────────────────────────────────────────────
    st.markdown('<div class="main-title">🔬 Deep Dive Research</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">'
        '<span class="badge-gemini">Gemini 2.0 Flash</span> &nbsp;×&nbsp; '
        '<span class="badge-llama">Llama 4 Scout 17B</span> &nbsp;|&nbsp; '
        'Cross-Verified AI Research Engine'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    # ── Topic Input ───────────────────────────────────────────────────────────
    col_topic, col_suggest = st.columns([3, 2])

    with col_topic:
        manual_topic = st.text_input(
            "🎯 Research Topic",
            placeholder="e.g. Retrieval-Augmented Generation, Kubernetes, Zero-Knowledge Proofs…",
            help="Enter any technical topic for a comprehensive deep dive.",
        )

    SUGGESTED = [
        "— Pick a suggestion —",
        "Retrieval-Augmented Generation (RAG)",
        "Kubernetes & Container Orchestration",
        "Transformer Architecture",
        "Edge Computing & IoT",
        "Zero-Knowledge Proofs",
        "Rust Programming Language",
        "WebAssembly (WASM)",
        "Apache Kafka",
        "GraphQL vs REST",
        "Federated Learning",
        "LLM Fine-tuning (LoRA / QLoRA)",
        "Microservices vs Monolith",
        "DevSecOps Practices",
        "Quantum Machine Learning",
    ]
    with col_suggest:
        pick = st.selectbox("💡 Or pick a suggested topic", SUGGESTED)

    # Resolve final topic
    topic = (pick if pick != SUGGESTED[0] else manual_topic).strip()

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    # ── Action Buttons ────────────────────────────────────────────────────────
    b1, b2, b3 = st.columns([5, 5, 2])
    with b1:
        btn_research = st.button("🚀 Run Research", use_container_width=True)
    with b2:
        btn_generate = st.button(
            "📄 Generate Final Document",
            disabled=not st.session_state.research_complete,
            use_container_width=True,
        )
    with b3:
        btn_reset = st.button("🔄 Reset", use_container_width=True)

    if btn_reset:
        for k in ["gemini_output", "llama_output", "verification", "final_doc", "current_topic"]:
            st.session_state[k] = None
        st.session_state["research_complete"] = False
        st.rerun()

    # ─────────────────────────────────────────────────────────────────────────
    # RUN RESEARCH PIPELINE
    # ─────────────────────────────────────────────────────────────────────────
    if btn_research:
        # Validation
        if not topic:
            st.error("⚠️ Please enter or select a research topic.")
            return
        if not gemini_key:
            st.error("⚠️ Gemini API key is missing — open the sidebar (← arrow) to add it.")
            return
        if not groq_key:
            st.error("⚠️ Groq API key is missing — open the sidebar (← arrow) to add it.")
            return

        st.session_state.current_topic = topic
        st.session_state.research_complete = False

        st.markdown("### 🔄 Research Pipeline")
        progress = st.progress(0)
        status   = st.empty()

        # ── Step 1: Gemini ────────────────────────────────────────────────────
        status.markdown("**Step 1 / 3** &nbsp;🧠 Gemini conducting research…")
        progress.progress(8)
        with st.spinner("Gemini is researching…"):
            g_out = run_gemini_research(topic, gemini_key)
        st.session_state.gemini_output = g_out
        progress.progress(38)

        if g_out.startswith("❌"):
            st.error(g_out)
            return
        st.success("✅ Step 1 complete — Gemini research done.")

        # ── Step 2: Llama ─────────────────────────────────────────────────────
        status.markdown("**Step 2 / 3** &nbsp;🦙 Llama performing deep analysis…")
        progress.progress(45)
        with st.spinner("Llama is analysing…"):
            l_out = run_llama_analysis(topic, groq_key, g_out)
        st.session_state.llama_output = l_out
        progress.progress(75)

        if l_out.startswith("❌"):
            st.error(l_out)
            return
        st.success("✅ Step 2 complete — Llama analysis done.")

        # ── Step 3: Cross-Verify ──────────────────────────────────────────────
        status.markdown("**Step 3 / 3** &nbsp;🔍 Cross-verifying insights…")
        progress.progress(82)
        with st.spinner("Verifying claims…"):
            verif = cross_verify_claim(g_out, topic, groq_key)
        st.session_state.verification = verif
        progress.progress(100)
        status.markdown(
            "✅ **All steps complete!** "
            "Click **Generate Final Document** to produce your Deep Dive."
        )
        st.session_state.research_complete = True
        st.balloons()

    # ─────────────────────────────────────────────────────────────────────────
    # DISPLAY RESEARCH OUTPUTS
    # ─────────────────────────────────────────────────────────────────────────
    if st.session_state.gemini_output or st.session_state.llama_output:
        st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            f"## 📊 Research Results &nbsp;·&nbsp; "
            f"*{st.session_state.current_topic}*"
        )

        tab_g, tab_l, tab_v = st.tabs(
            ["🟦 Gemini Research", "🟠 Llama Analysis", "🔍 Cross-Verification"]
        )

        with tab_g:
            if st.session_state.gemini_output:
                with st.expander("View Gemini Research Output", expanded=True):
                    st.markdown(st.session_state.gemini_output)

        with tab_l:
            if st.session_state.llama_output:
                with st.expander("View Llama Analysis Output", expanded=True):
                    st.markdown(st.session_state.llama_output)

        with tab_v:
            v = st.session_state.verification
            if v:
                st.markdown(
                    f"""
                    <div class="verify-card">
                        <h3>🔍 Cross-Verification Result</h3>
                        <p><strong>Extracted Claim:</strong><br>
                        <em>"{v.get('claim','N/A')}"</em></p>
                        <br>
                        <p><strong>Verification Status:</strong> &nbsp;
                        {_pill(v.get('result','Unknown'))}</p>
                        <br>
                        <p><strong>Explanation:</strong><br>
                        {v.get('explanation','N/A')}</p>
                        <br>
                        <p><strong>Confidence Level:</strong> &nbsp;
                        <code>{v.get('confidence','N/A')}</code></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if v.get("nuance"):
                    st.info(f"📝 **Additional Nuance:** {v['nuance']}")

    # ─────────────────────────────────────────────────────────────────────────
    # GENERATE FINAL DOCUMENT
    # ─────────────────────────────────────────────────────────────────────────
    if btn_generate and st.session_state.research_complete:
        with st.spinner("📝 Synthesising your Deep Dive document…"):
            doc = generate_final_document(
                st.session_state.current_topic,
                st.session_state.gemini_output,
                st.session_state.llama_output,
                st.session_state.verification,
                groq_key,
            )
        st.session_state.final_doc = doc

    # ─────────────────────────────────────────────────────────────────────────
    # DISPLAY FINAL DOCUMENT
    # ─────────────────────────────────────────────────────────────────────────
    if st.session_state.final_doc:
        st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
        st.markdown("## 📄 Final Deep Dive Document")

        # Metadata row
        m1, m2, m3, m4 = st.columns(4)
        topic_label = st.session_state.current_topic
        if len(topic_label) > 28:
            topic_label = topic_label[:25] + "…"
        word_count = len(st.session_state.final_doc.split())
        char_count = len(st.session_state.final_doc)
        m1.metric("📌 Topic",      topic_label)
        m2.metric("📝 Words",      f"~{word_count:,}")
        m3.metric("📐 Characters", f"~{char_count:,}")
        m4.metric("🤖 Models",     "Gemini + Llama 4")

        # Preview
        with st.expander("📖 Preview Document", expanded=True):
            st.markdown(st.session_state.final_doc)

        # Downloads
        st.markdown("### 💾 Download")
        safe_name = (
            st.session_state.current_topic.lower()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("/", "_")[:35]
        )
        date_str   = datetime.now().strftime("%Y%m%d")
        md_name    = f"deep_dive_{safe_name}_{date_str}.md"
        txt_name   = md_name.replace(".md", ".txt")

        d1, d2 = st.columns(2)
        with d1:
            st.download_button(
                label="⬇️ Download Markdown (.md)",
                data=st.session_state.final_doc,
                file_name=md_name,
                mime="text/markdown",
                use_container_width=True,
            )
        with d2:
            st.download_button(
                label="⬇️ Download Plain Text (.txt)",
                data=st.session_state.final_doc,
                file_name=txt_name,
                mime="text/plain",
                use_container_width=True,
            )

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align:center;color:#6b7280;font-size:0.82rem;padding:0.8rem 0;">
            🔬 <strong>Deep Dive Research Engine</strong> &nbsp;|&nbsp;
            Powered by <strong>Gemini 2.0 Flash</strong> × <strong>Llama 4 Scout 17B via Groq</strong>
            &nbsp;|&nbsp; Dual-AI Cross-Verified Insights
        </div>
        """,
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
