import html as html_lib
import json
import textwrap

import requests
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Research Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# HELPERS
# ============================================================

def html(content: str) -> None:
    st.html(textwrap.dedent(content))


def safe(value) -> str:
    return html_lib.escape(str(value or ""))


def safe_float(value, default=0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default=0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def parse_report(result: dict) -> dict:
    report = result.get("final_report", result.get("report", {}))

    if isinstance(report, dict):
        return report

    if isinstance(report, str):
        try:
            parsed = json.loads(report)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
        return {"executive_summary": report}

    return {}


def reset_to_home() -> None:
    st.session_state.question = ""
    st.session_state.research_result = None
    st.session_state.page = "home"


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
<style>
/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 8% 10%,
            rgba(247,143,163,0.11),
            transparent 22%
        ),
        radial-gradient(
            circle at 92% 25%,
            rgba(255,183,197,0.06),
            transparent 20%
        ),
        #071014 !important;
    color:#f8f6f4 !important;
}

.block-container {
    max-width:1450px !important;
    padding-top:1rem !important;
    padding-bottom:2.5rem !important;
}

#MainMenu,
footer {
    visibility:hidden !important;
}

header {
    background:transparent !important;
}

html {
    scroll-behavior:smooth;
}

[id] {
    scroll-margin-top:25px;
}


/* ============================================================
   NAVIGATION
   These are normal HTML anchors.
   They scroll instantly and do NOT trigger Streamlit reruns.
   ============================================================ */

.top-nav {
    width:100%;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:8px 5px 18px;
    border-bottom:1px solid rgba(255,255,255,0.07);
}

.brand {
    display:flex;
    align-items:center;
    gap:12px;
}

.brand-symbol {
    width:40px;
    height:40px;
    border-radius:11px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:21px;
    font-weight:800;
    background:linear-gradient(135deg,#ffb1bf,#f47f9a);
    color:#171014;
    box-shadow:0 0 22px rgba(247,143,163,0.20);
    flex-shrink:0;
}

.brand-name {
    font-size:16px;
    font-weight:800;
    line-height:1.1;
    color:#f7f3f1;
}

.brand-subtitle {
    font-size:10px;
    color:#8e9a9d;
    margin-top:4px;
}

.nav-links {
    display:flex;
    gap:27px;
    align-items:center;
    font-size:12px;
}

.nav-link {
    color:#b5c0c3 !important;
    text-decoration:none !important;
    cursor:pointer;
    white-space:nowrap;
    transition:color 0.15s ease;
}

.nav-link:hover {
    color:#ff9fb1 !important;
}

.nav-active {
    color:#ff9fb1 !important;
    font-weight:700;
}

.signin-link {
    display:inline-flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(135deg,#ff9daf,#f1849b);
    color:#171014 !important;
    border-radius:9px;
    padding:11px 19px;
    font-weight:800;
    text-decoration:none !important;
}

.signin-link:hover {
    color:#171014 !important;
    box-shadow:0 8px 22px rgba(255,143,163,0.20);
}

.settings-link {
    font-size:16px;
}


/* ============================================================
   HOME
   ============================================================ */

.hero {
    text-align:center;
    padding:58px 20px 30px;
}

.hero-badge {
    display:inline-block;
    padding:8px 16px;
    border-radius:999px;
    border:1px solid rgba(255,159,177,0.38);
    background:rgba(255,159,177,0.05);
    color:#ffafbd;
    font-size:11px;
    font-weight:700;
    letter-spacing:0.7px;
    margin-bottom:20px;
}

.hero-title {
    max-width:900px;
    margin:auto;
    font-size:50px;
    line-height:1.08;
    font-weight:850;
    letter-spacing:-2px;
}

.pink-text {
    background:linear-gradient(
        90deg,
        #ffb3c1,
        #f58ba2,
        #ffc1cb
    );
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero-description {
    max-width:760px;
    margin:20px auto 0;
    color:#aab5b8;
    font-size:15px;
    line-height:1.7;
}

.feature-strip {
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:12px;
    margin:22px auto 28px;
    max-width:1050px;
}

.mini-feature {
    text-align:center;
    padding:12px;
    color:#aeb9bc;
    font-size:11px;
    border-radius:12px;
    background:rgba(255,255,255,0.022);
    border:1px solid rgba(255,255,255,0.065);
}

.mini-icon {
    font-size:19px;
    color:#ff9fb1;
    margin-bottom:5px;
}

.mini-title {
    color:#f5f1ef;
    font-weight:700;
    margin-bottom:3px;
}

.research-card {
    max-width:1100px;
    margin:18px auto 0;
    padding:24px;
    border-radius:17px;
    background:linear-gradient(
        145deg,
        rgba(24,35,39,0.92),
        rgba(10,20,24,0.92)
    );
    border:1px solid rgba(255,159,177,0.27);
}

.research-title {
    font-size:18px;
    font-weight:750;
    margin-bottom:12px;
}

.examples-label {
    max-width:1100px;
    margin:12px auto 7px;
    color:#a9b5b8;
    font-size:12px;
    font-weight:700;
}


/* ============================================================
   INPUT
   ============================================================ */

.stTextArea textarea {
    background:#0b1519 !important;
    color:#f1f3f2 !important;
    border:1px solid #44555b !important;
    border-radius:11px !important;
    font-size:14px !important;
    caret-color:#ff9fb1 !important;
}

.stTextArea textarea:focus {
    border-color:#ff9fb1 !important;
    box-shadow:0 0 0 1px rgba(255,159,177,0.22) !important;
}

.stTextArea textarea::placeholder {
    color:#858f93 !important;
    opacity:1 !important;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    min-height:44px !important;
    border-radius:10px !important;
    border:1px solid rgba(255,159,177,0.45) !important;
    background:linear-gradient(135deg,#ff9daf,#f1849b) !important;
    color:#1b1014 !important;
    font-weight:800 !important;
    transition:transform 0.15s ease, box-shadow 0.15s ease !important;
}

.stButton > button:hover {
    transform:translateY(-1px) !important;
    box-shadow:0 8px 22px rgba(255,143,163,0.18) !important;
}

div[data-testid="stDownloadButton"] button,
div[data-testid="stDownloadButton"] > button {
    width:100% !important;
    min-height:44px !important;
    border-radius:10px !important;
    border:1px solid rgba(255,159,177,0.45) !important;
    background:linear-gradient(135deg,#ff9daf,#f1849b) !important;
    color:#1b1014 !important;
    font-weight:800 !important;
    opacity:1 !important;
}

div[data-testid="stDownloadButton"] button:hover {
    box-shadow:0 8px 22px rgba(255,143,163,0.18) !important;
}

div[data-testid="stDownloadButton"] button p,
div[data-testid="stDownloadButton"] button span {
    color:#1b1014 !important;
    font-weight:800 !important;
}


/* ============================================================
   GENERAL CARDS
   ============================================================ */

.section-heading {
    font-size:24px;
    font-weight:800;
    margin-top:42px;
    margin-bottom:7px;
}

.section-description {
    color:#89979b;
    font-size:13px;
    margin-bottom:18px;
}

.feature-card,
.content-card,
.company-card,
.sidebar-card,
.metric-card,
.agent-box,
.research-progress-card {
    background:rgba(17,29,33,0.82);
    border:1px solid rgba(255,255,255,0.075);
}

.feature-card {
    min-height:145px;
    padding:21px;
    border-radius:15px;
    margin-bottom:12px;
}

.feature-card:hover {
    border-color:rgba(255,159,177,0.28);
}

.feature-icon {
    width:43px;
    height:43px;
    border-radius:12px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:rgba(255,143,163,0.11);
    color:#ff9fb1;
    font-size:21px;
    margin-bottom:12px;
}

.feature-title,
.content-card-title {
    color:#f6f2ef;
    font-weight:800;
}

.feature-title {
    font-size:14px;
    margin-bottom:6px;
}

.feature-description,
.content-text {
    color:#a9b4b6;
    line-height:1.6;
}

.feature-description {
    font-size:12px;
}

.content-card {
    border-radius:15px;
    padding:20px;
    margin-bottom:12px;
}

.content-card-title {
    font-size:15px;
    margin-bottom:10px;
}

.content-text {
    font-size:12px;
}

.info-section {
    margin-top:45px;
    padding:25px;
    border-radius:15px;
    background:rgba(17,29,33,0.58);
    border:1px solid rgba(255,255,255,0.065);
}

.info-title {
    font-size:20px;
    font-weight:800;
    margin-bottom:8px;
}

.info-text {
    color:#aab5b8;
    font-size:13px;
    line-height:1.7;
}


/* ============================================================
   RESEARCHING
   ============================================================ */

.results-header {
    margin-top:28px;
    margin-bottom:18px;
}

.results-title {
    font-size:30px;
    font-weight:850;
    margin-bottom:6px;
}

.results-subtitle {
    color:#8f9ca0;
    font-size:12px;
    line-height:1.65;
}

.question-box {
    background:rgba(255,159,177,0.045);
    border:1px solid rgba(255,159,177,0.16);
    border-radius:12px;
    padding:15px;
    color:#c6ced0;
    font-size:13px;
    margin-bottom:18px;
}

.research-progress-card {
    border-radius:17px;
    padding:22px;
    margin-top:18px;
}

.agent-box {
    min-height:125px;
    padding:17px;
    border-radius:14px;
    text-align:center;
}

.agent-icon {
    font-size:25px;
    color:#ff9fb1;
    margin-bottom:7px;
}

.agent-title {
    font-weight:750;
    font-size:13px;
    margin-bottom:5px;
}

.agent-description {
    color:#89979b;
    font-size:11px;
    line-height:1.5;
}


/* ============================================================
   RESULTS
   ============================================================ */

.metric-card {
    border-radius:14px;
    padding:18px;
    min-height:112px;
}

.metric-label {
    color:#94a1a4;
    font-size:11px;
    margin-bottom:9px;
}

.metric-value {
    font-size:27px;
    font-weight:850;
    color:#f7f4f2;
}

.metric-highlight {
    color:#ff9fb1;
    font-size:11px;
    margin-top:4px;
}

.company-card {
    border-radius:13px;
    padding:17px;
    margin-bottom:12px;
    min-height:150px;
}

.company-name {
    font-size:15px;
    font-weight:800;
    color:#f8f5f2;
}

.company-score {
    font-size:24px;
    font-weight:850;
    color:#ff9fb1;
    text-align:right;
}

.company-meta {
    color:#8f9ca0;
    font-size:11px;
    margin-top:4px;
}

.score-bar {
    height:6px;
    border-radius:999px;
    background:#263337;
    overflow:hidden;
    margin-top:11px;
}

.score-fill {
    height:100%;
    border-radius:999px;
    background:linear-gradient(90deg,#f47f9a,#ffb2bf);
}

.validation-pass,
.validation-warning {
    border-radius:10px;
    padding:12px;
    font-size:12px;
}

.validation-pass {
    border:1px solid rgba(115,220,174,0.25);
    background:rgba(70,180,130,0.07);
    color:#87dcb4;
}

.validation-warning {
    border:1px solid rgba(255,190,100,0.25);
    background:rgba(255,190,100,0.06);
    color:#ffc77d;
}

.insight-number {
    display:inline-flex;
    width:23px;
    height:23px;
    border-radius:50%;
    align-items:center;
    justify-content:center;
    background:rgba(255,159,177,0.13);
    color:#ff9fb1;
    font-size:11px;
    font-weight:800;
    margin-right:7px;
}

@media (max-width:900px) {
    .nav-links {
        gap:13px;
    }

    .hero-title {
        font-size:38px;
    }

    .feature-strip {
        grid-template-columns:repeat(2,1fr);
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "question" not in st.session_state:
    st.session_state.question = ""

if "research_result" not in st.session_state:
    st.session_state.research_result = None


# ============================================================
# NAVIGATION
# ============================================================

def show_nav(active: str = "Home") -> None:
    # These are anchors, not Streamlit buttons.
    # Clicking them therefore scrolls instantly without
    # sending another request to the FastAPI backend.
    html(
        f"""
        <div class="top-nav" id="top">

            <div class="brand">
                <div class="brand-symbol">✦</div>

                <div>
                    <div class="brand-name">Research Intelligence</div>
                    <div class="brand-subtitle">
                        Agentic AI Research Platform
                    </div>
                </div>
            </div>

            <div class="nav-links">

                <a
                    class="nav-link {'nav-active' if active == 'Home' else ''}"
                    href="#home"
                >Home</a>

                <a
                    class="nav-link {'nav-active' if active == 'Examples' else ''}"
                    href="#examples"
                >Examples</a>

                <a
                    class="nav-link {'nav-active' if active == 'How it works' else ''}"
                    href="#how-it-works"
                >How it works</a>

                <a
                    class="nav-link {'nav-active' if active == 'About' else ''}"
                    href="#about"
                >About</a>

                <a
                    class="nav-link settings-link"
                    href="#settings"
                    title="Settings"
                    aria-label="Settings"
                >⚙</a>

                <a
                    class="signin-link"
                    href="#sign-in"
                >Sign in</a>

            </div>
        </div>
        """
    )


# ============================================================
# HOME
# ============================================================

def show_home() -> None:
    show_nav("Home")

    html(
        """
        <div id="home"></div>

        <div class="hero">

            <div class="hero-badge">
                ✦ &nbsp; MULTI-AGENT AI RESEARCH
            </div>

            <div class="hero-title">
                Turn complex questions into
                <span class="pink-text">
                    trusted, evidence-backed insights
                </span>
            </div>

            <div class="hero-description">
                Get comprehensive research with real sources,
                data, comparisons and analysis using multiple
                AI agents working together.
            </div>

        </div>

        <div class="feature-strip">

            <div class="mini-feature">
                <div class="mini-icon">◉</div>
                <div class="mini-title">Multi-Agent Research</div>
                Plan, Search, Analyze
            </div>

            <div class="mini-feature">
                <div class="mini-icon">⌕</div>
                <div class="mini-title">Real-time Web Search</div>
                Latest information
            </div>

            <div class="mini-feature">
                <div class="mini-icon">✓</div>
                <div class="mini-title">Source Verification</div>
                Credible & traceable
            </div>

            <div class="mini-feature">
                <div class="mini-icon">▤</div>
                <div class="mini-title">Structured Reports</div>
                Clear & understandable
            </div>

        </div>

        <div id="examples"></div>

        <div class="research-card">
            <div class="research-title">
                What would you like to research today?
            </div>
        </div>
        """
    )

    question = st.text_area(
        "Research question",
        value=st.session_state.question,
        height=120,
        placeholder=(
            "Example: Analyze the Indian AI startup market "
            "and identify the most promising companies."
        ),
        label_visibility="collapsed",
        key="research_question_input",
    )

    st.session_state.question = question

    if st.button(
        "Analyze Research  →",
        type="primary",
        key="analyze_research",
    ):
        if not question.strip():
            st.warning("Please enter a research question first.")
        else:
            st.session_state.page = "researching"
            st.rerun()

    html(
        """
        <div class="examples-label">
            Try an example:
        </div>
        """
    )

    examples = [
        "Future of electric vehicles in India",
        "Compare top LLM models in 2025",
        "Latest trends in global AI investment",
    ]

    example_columns = st.columns(3)

    for index, example in enumerate(examples):
        with example_columns[index]:
            if st.button(
                example,
                key=f"example_{index}",
                use_container_width=True,
            ):
                st.session_state.question = example
                st.session_state.research_result = None
                st.rerun()

    html('<div id="how-it-works"></div>')

    html(
        """
        <div class="section-heading">
            What the platform does
        </div>

        <div class="section-description">
            Multiple specialized components work together instead
            of relying on a single AI response.
        </div>
        """
    )

    features = [
        (
            "◉",
            "Intelligent Planning",
            "Breaks a research question into focused topics, companies and search queries.",
        ),
        (
            "⌕",
            "Evidence Retrieval",
            "Combines web research with semantic retrieval from the persistent knowledge base.",
        ),
        (
            "✓",
            "Source Verification",
            "Checks available evidence before it is used in the final research output.",
        ),
        (
            "ϟ",
            "Parallel Research",
            "Runs independent research tasks without unnecessary sequential work.",
        ),
        (
            "▤",
            "RAG Knowledge Base",
            "Stores research documents and embeddings using PostgreSQL and pgvector.",
        ),
        (
            "▥",
            "Explainable Scoring",
            "Connects company scores to available evidence instead of unsupported claims.",
        ),
    ]

    for start in range(0, len(features), 3):
        row = st.columns(3)

        for column, feature in zip(
            row,
            features[start:start + 3],
        ):
            icon, title, description = feature

            with column:
                html(
                    f"""
                    <div class="feature-card">

                        <div class="feature-icon">
                            {safe(icon)}
                        </div>

                        <div class="feature-title">
                            {safe(title)}
                        </div>

                        <div class="feature-description">
                            {safe(description)}
                        </div>

                    </div>
                    """
                )

    html(
        """
        <div id="about" class="info-section">

            <div class="info-title">
                About
            </div>

            <div class="info-text">
                Research Intelligence is a multi-agent research
                platform that plans research, gathers evidence,
                verifies sources, retrieves knowledge from a RAG
                database, scores companies and validates the
                generated report.
            </div>

        </div>

        <div id="settings" class="info-section">

            <div class="info-title">
                Settings
            </div>

            <div class="info-text">
                The current application uses the local Qwen model
                for generation and the configured research services
                for retrieval. Application controls can be added
                here without changing the research pipeline.
            </div>

        </div>

        <div id="sign-in" class="info-section">

            <div class="info-title">
                Sign in
            </div>

            <div class="info-text">
                Authentication is not enabled in the current
                fresher-friendly version of the platform.
            </div>

        </div>
        """
    )


# ============================================================
# RESEARCHING
# ============================================================

def show_researching() -> None:
    # The navigation remains visible, but it contains only
    # page anchors. No accidental backend request is created.
    show_nav("Home")

    html(
        """
        <div class="results-header">

            <div class="results-title">
                Researching your question...
            </div>

            <div class="results-subtitle">
                AI agents are working together to find,
                verify and analyze relevant information.
            </div>

        </div>
        """
    )

    html(
        f"""
        <div class="question-box">
            <strong>Your Question</strong>
            <br><br>
            {safe(st.session_state.question)}
        </div>

        <div class="research-progress-card">
            <div class="content-card-title">
                Research Pipeline
            </div>
            <div class="content-text">
                The local Qwen model and research services are
                processing the request. This can take a few minutes.
            </div>
        </div>
        """
    )

    progress = st.progress(8)
    status = st.empty()

    agent_columns = st.columns(4)

    agents = [
        ("◎", "Planner", "Creates the research strategy."),
        ("⌕", "Web Research", "Collects relevant evidence."),
        ("✓", "Verifier", "Checks available sources."),
        ("▤", "Writer", "Creates the final report."),
    ]

    for column, agent in zip(agent_columns, agents):
        icon, title, description = agent

        with column:
            html(
                f"""
                <div class="agent-box">

                    <div class="agent-icon">
                        {safe(icon)}
                    </div>

                    <div class="agent-title">
                        {safe(title)}
                    </div>

                    <div class="agent-description">
                        {safe(description)}
                    </div>

                </div>
                """
            )

    status.markdown("**Running the research pipeline...**")

    try:
        response = requests.post(
            "http://127.0.0.1:8000/research",
            json={
                "question": st.session_state.question
            },
            timeout=900,
        )

        response.raise_for_status()

        st.session_state.research_result = response.json()
        progress.progress(100)
        status.markdown(
            "**Research complete. Preparing results...**"
        )

        st.session_state.page = "results"
        st.rerun()

    except requests.exceptions.ConnectionError:
        st.error(
            "FastAPI is not running. Start it with: "
            "uvicorn app.api:app --reload"
        )

        if st.button(
            "← Back to Home",
            key="research_connection_back",
        ):
            reset_to_home()
            st.rerun()

    except requests.exceptions.Timeout:
        st.error(
            "The research request timed out."
        )

        if st.button(
            "← Back to Home",
            key="research_timeout_back",
        ):
            reset_to_home()
            st.rerun()

    except requests.exceptions.HTTPError:
        try:
            detail = response.json()
        except Exception:
            detail = response.text

        st.error(
            f"Research API error:\n\n{detail}"
        )

        if st.button(
            "← Back to Home",
            key="research_http_back",
        ):
            reset_to_home()
            st.rerun()

    except Exception as error:
        st.error(
            f"Research request failed: {error}"
        )

        if st.button(
            "← Back to Home",
            key="research_error_back",
        ):
            reset_to_home()
            st.rerun()


# ============================================================
# RESULTS
# ============================================================

def show_results() -> None:
    result = st.session_state.research_result

    if not result:
        reset_to_home()
        st.rerun()

    report = parse_report(result)

    validation = report.get(
        "validation",
        result.get("validation", {}),
    )

    if not isinstance(validation, dict):
        validation = {}

    confidence = safe_float(
        result.get("confidence_score", 0)
    )

    latency = safe_float(
        result.get("total_latency_seconds", 0)
    )

    total_tokens = safe_int(
        result.get("total_tokens", 0)
    )

    # API now returns ONLY genuinely verified sources
    # in this field.
    verified_sources = result.get(
        "verified_sources",
        [],
    )

    if isinstance(verified_sources, list):
        verified_source_count = len(
            verified_sources
        )
    else:
        verified_source_count = safe_int(
            result.get("verified_source_count", 0)
        )

    demo_source_count = safe_int(
        result.get("demo_source_count", 0)
    )

    unverified_source_count = safe_int(
        result.get("unverified_source_count", 0)
    )

    title = report.get(
        "title",
        "Research Analysis",
    )

    question = result.get(
        "question",
        st.session_state.question,
    )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    html(
        f"""
        <div class="top-nav" id="results-top">

            <div class="brand">

                <div class="brand-symbol">
                    ✦
                </div>

                <div>
                    <div class="brand-name">
                        Research Intelligence
                    </div>

                    <div class="brand-subtitle">
                        Agentic AI Research Platform
                    </div>
                </div>

            </div>

            <div class="nav-links">
                <a
                    class="nav-link"
                    href="#results-top"
                >
                    Results
                </a>
            </div>

        </div>

        <div class="results-header">

            <div class="results-title">
                {safe(title)}
            </div>

            <div class="results-subtitle">
                Evidence-backed analysis generated by the
                Agentic Research Intelligence Platform.
                <br>
                <span style="color:#b3bec1;">
                    {safe(question)}
                </span>
            </div>

        </div>
        """
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    metric_columns = st.columns(4)

    metrics = [
        (
            "Confidence Score",
            f"{confidence:.0%}",
            "Evidence-based confidence",
        ),
        (
            "Verified Sources",
            str(verified_source_count),
            "Independently verified web sources",
        ),
        (
            "Total Latency",
            f"{latency:.1f}s",
            "End-to-end processing",
        ),
        (
            "LLM Tokens",
            f"{total_tokens:,}",
            "Local Qwen processing",
        ),
    ]

    for column, metric in zip(
        metric_columns,
        metrics,
    ):
        label, value, description = metric

        with column:
            html(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        {safe(label)}
                    </div>

                    <div class="metric-value">
                        {safe(value)}
                    </div>

                    <div class="metric-highlight">
                        {safe(description)}
                    </div>

                </div>
                """
            )

    # --------------------------------------------------------
    # SUMMARY + VALIDATION
    # --------------------------------------------------------

    top_left, top_right = st.columns(
        [2.1, 1]
    )

    with top_left:
        summary = report.get(
            "executive_summary",
            "No executive summary available.",
        )

        html(
            f"""
            <div class="content-card">

                <div class="content-card-title">
                    ▤ &nbsp; Executive Summary
                </div>

                <div class="content-text">
                    {safe(summary)}
                </div>

            </div>
            """
        )

    with top_right:
        validation_status = str(
            validation.get(
                "status",
                "unknown",
            )
        ).lower()

        if validation_status == "passed":
            html(
                """
                <div class="sidebar-card">

                    <div class="content-card-title">
                        ✓ &nbsp; Validation
                    </div>

                    <div class="validation-pass">
                        Report passed the final validation stage.
                    </div>

                </div>
                """
            )
        else:
            html(
                """
                <div class="sidebar-card">

                    <div class="content-card-title">
                        ! &nbsp; Validation
                    </div>

                    <div class="validation-warning">
                        Additional validation may be required
                        for this report.
                    </div>

                </div>
                """
            )

    # --------------------------------------------------------
    # MARKET + INSIGHTS
    # --------------------------------------------------------

    market_overview = report.get(
        "market_overview",
        "",
    )

    insights = report.get(
        "key_insights",
        report.get("insights", []),
    )

    if isinstance(insights, str):
        insights = (
            [insights]
            if insights.strip()
            else []
        )

    if not isinstance(insights, list):
        insights = []

    market_left, insight_right = st.columns(
        [2.1, 1]
    )

    with market_left:
        if market_overview:
            html(
                f"""
                <div class="content-card">

                    <div class="content-card-title">
                        ▥ &nbsp; Market Overview
                    </div>

                    <div class="content-text">
                        {safe(market_overview)}
                    </div>

                </div>
                """
            )

    with insight_right:
        html(
            """
            <div class="sidebar-card">

                <div class="content-card-title">
                    ✦ &nbsp; Key Insights
                </div>
            """
        )

        if insights:
            for index, insight in enumerate(
                insights,
                start=1,
            ):
                html(
                    f"""
                    <div style="
                        margin-bottom:10px;
                        color:#a9b4b6;
                        font-size:12px;
                        line-height:1.5;
                    ">

                        <span class="insight-number">
                            {index}
                        </span>

                        {safe(insight)}

                    </div>
                    """
                )
        else:
            fallback = []

            if confidence == 0:
                fallback.append(
                    "No independently verified web evidence "
                    "was available for this analysis."
                )

            if demo_source_count:
                fallback.append(
                    f"{demo_source_count} demo/fallback "
                    "sources were available to the pipeline."
                )

            if fallback:
                for index, insight in enumerate(
                    fallback,
                    start=1,
                ):
                    html(
                        f"""
                        <div style="
                            margin-bottom:10px;
                            color:#a9b4b6;
                            font-size:12px;
                            line-height:1.5;
                        ">
                            <span class="insight-number">
                                {index}
                            </span>
                            {safe(insight)}
                        </div>
                        """
                    )
            else:
                html(
                    """
                    <div class="content-text">
                        Key insights will appear here when
                        the report provides them.
                    </div>
                    """
                )

        html("</div>")

    # --------------------------------------------------------
    # COMPANIES
    # Two columns reduce the page height substantially.
    # --------------------------------------------------------

    companies = report.get(
        "companies",
        [],
    )

    if not isinstance(companies, list):
        companies = []

    html(
        """
        <div class="section-heading">
            Top Companies Identified
        </div>

        <div class="section-description">
            Scores shown below come from the research pipeline
            and available evidence.
        </div>
        """
    )

    company_columns = st.columns(2)

    for index, company in enumerate(
        companies,
        start=1,
    ):
        if not isinstance(company, dict):
            continue

        name = company.get(
            "company_name",
            company.get(
                "company",
                "Unknown Company",
            ),
        )

        score = safe_float(
            company.get(
                "overall_score",
                0,
            )
        )

        explanation = company.get(
            "evidence_summary",
            company.get(
                "explanation",
                company.get(
                    "reasoning",
                    company.get(
                        "summary",
                        company.get(
                            "reason",
                            "",
                        ),
                    ),
                ),
            ),
        )

        evidence_count = company.get(
            "evidence_count"
        )

        if evidence_count is None:
            evidence_label = (
                "Evidence-adjusted scoring"
            )
        else:
            evidence_label = (
                f"Evidence items: "
                f"{safe_int(evidence_count)}"
            )

        percentage = min(
            max(score / 10 * 100, 0),
            100,
        )

        with company_columns[
            (index - 1) % 2
        ]:
            html(
                f"""
                <div class="company-card">

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                        gap:15px;
                    ">

                        <div>
                            <div class="company-name">
                                {index}. {safe(name)}
                            </div>

                            <div class="company-meta">
                                {safe(evidence_label)}
                            </div>
                        </div>

                        <div class="company-score">
                            {score:.2f}
                        </div>

                    </div>

                    <div class="score-bar">
                        <div
                            class="score-fill"
                            style="
                                width:{percentage:.2f}%;
                            "
                        ></div>
                    </div>

                    <div
                        class="content-text"
                        style="margin-top:10px;"
                    >
                        {safe(explanation)}
                    </div>

                </div>
                """
            )

    # --------------------------------------------------------
    # METHODOLOGY + LIMITATIONS
    # --------------------------------------------------------

    methodology = report.get(
        "methodology",
        "",
    )

    limitations = report.get(
        "limitations",
        [],
    )

    if isinstance(limitations, str):
        limitations = (
            [limitations]
            if limitations.strip()
            else []
        )

    if not isinstance(limitations, list):
        limitations = (
            [limitations]
            if limitations
            else []
        )

    method_left, limitation_right = st.columns(2)

    with method_left:
        if methodology:
            html(
                f"""
                <div class="sidebar-card">

                    <div class="content-card-title">
                        ⚙ &nbsp; Methodology
                    </div>

                    <div class="content-text">
                        {safe(methodology)}
                    </div>

                </div>
                """
            )

    with limitation_right:
        limitation_items = list(limitations)

        if confidence == 0:
            confidence_limit = (
                "No genuinely verified web evidence "
                "was available."
            )

            if confidence_limit not in limitation_items:
                limitation_items.insert(
                    0,
                    confidence_limit,
                )

        if demo_source_count:
            demo_limit = (
                "Demo/fallback evidence is not "
                "independent verification."
            )

            if demo_limit not in limitation_items:
                limitation_items.append(
                    demo_limit
                )

        if unverified_source_count:
            unverified_limit = (
                f"{unverified_source_count} web sources "
                "were not independently verified."
            )

            if unverified_limit not in limitation_items:
                limitation_items.append(
                    unverified_limit
                )

        if limitation_items:
            limitation_html = "".join(
                f"""
                <div style="
                    margin-bottom:8px;
                ">
                    • {safe(item)}
                </div>
                """
                for item in limitation_items
            )

            html(
                f"""
                <div class="sidebar-card">

                    <div class="content-card-title">
                        ! &nbsp; Limitations
                    </div>

                    <div class="content-text">
                        {limitation_html}
                    </div>

                </div>
                """
            )

    # --------------------------------------------------------
    # SOURCE BREAKDOWN
    # --------------------------------------------------------

    if demo_source_count or unverified_source_count:
        html(
            f"""
            <div class="content-text"
                 style="
                    margin-top:4px;
                    margin-bottom:8px;
                 ">
                Source breakdown:
                {verified_source_count} verified,
                {unverified_source_count} unverified,
                {demo_source_count} demo/fallback.
            </div>
            """
        )

    # --------------------------------------------------------
    # ACTIONS
    # --------------------------------------------------------

    action_left, action_right = st.columns(2)

    with action_left:
        if st.button(
            "← New Research",
            use_container_width=True,
            key="results_new_research",
        ):
            reset_to_home()
            st.rerun()

    with action_right:
        report_json = json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
        )

        st.download_button(
            "Download Research Report",
            data=report_json,
            file_name="research_report.json",
            mime="application/json",
            use_container_width=True,
            key="download_research_report",
        )


# ============================================================
# ROUTER
# ============================================================

if st.session_state.page == "home":
    show_home()

elif st.session_state.page == "researching":
    show_researching()

elif st.session_state.page == "results":
    show_results()

else:
    reset_to_home()
    st.rerun()
