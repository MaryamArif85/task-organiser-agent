import streamlit as st
from graph import graph as graph_app
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Task Organiser Agent", page_icon="✅", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0A0A0A; color: white; }
    h1 { font-size: 4rem !important; font-weight: 900 !important; line-height: 1; }
    .top-label { color:#FF1E1E; letter-spacing:3px; font-size:18px !important; font-weight:800; }
    .card {
        background-color: #141414;
        border-top: 2.5px solid #FF1E1E;
        padding: 22px;
        min-height: 170px;
    }
    .card-num { color: #FF1E1E; font-size: 32px; font-weight: 900; }
    .card-title { font-weight: 800; font-size: 15px; margin-top: 8px; color: white; }
    .card-desc { color: #D1D5DB; font-size: 14px; margin-top: 10px; line-height:1.4; }
    textarea { background-color: #141414 !important; color: white !important; border: 1.5px solid #555 !important; font-size: 16px !important; }
    .stButton>button { font-size: 15px !important; font-weight: 600; }
    [data-baseweb="tab"] { font-size: 15px !important; }
</style>
""", unsafe_allow_html=True)

def set_example(text):
    st.session_state.user_text = text
def clear_text():
    st.session_state.user_text = ""

if "user_text" not in st.session_state:
    st.session_state.user_text = ""

# --- FIXED HEADER ---
st.markdown('<p class="top-label">TASK ORGANISER AGENT</p>', unsafe_allow_html=True)
st.markdown('<h1>3-STEP<br>TASK<br>ORGANISER <span style="color:#FF1E1E;">AGENT</span></h1>', unsafe_allow_html=True)
st.markdown('<hr style="border: 1px solid #FF1E1E; margin-top:20px;">', unsafe_allow_html=True)

c_a, c_b = st.columns([2,1])
with c_a:
    st.markdown('**📅 TODAY BUILT WITH LANG GRAPH | 🚀 STREAMLIT + GEMINI 3.6 FLASH**')
with c_b:
    st.markdown('<p style="text-align:right; font-size:15px; font-weight:700;">LEARN. <span style="color:#FF1E1E;">ORGANISE.</span> EXECUTE.</p>', unsafe_allow_html=True)

# --- Cards ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="card"><div class="card-num">01</div><div class="card-title">EXAMPLE 1 — DAILY TASKS</div><div class="card-desc">Buy groceries today, finish assignment tomorrow, and plan vacation next month.</div></div>', unsafe_allow_html=True)
    st.button("Load Example 1", on_click=set_example, args=("Buy groceries today, finish assignment tomorrow, and plan vacation next month.",), use_container_width=True)
with col2:
    st.markdown('<div class="card"><div class="card-num">02</div><div class="card-title">EXAMPLE 2 — WEEKLY PLAN</div><div class="card-desc">Pay electricity bill asap, prepare for exam this week, call mom next week</div></div>', unsafe_allow_html=True)
    st.button("Load Example 2", on_click=set_example, args=("Pay electricity bill asap, prepare for exam this week, call mom next week",), use_container_width=True)
with col3:
    st.markdown('<div class="card"><div class="card-num">03</div><div class="card-title">EXAMPLE 3 — URGENT TASKS</div><div class="card-desc">Submit report today, schedule meeting tomorrow, with high and medium priorities.</div></div>', unsafe_allow_html=True)
    st.button("Load Example 3", on_click=set_example, args=("Submit report today, schedule meeting tomorrow",), use_container_width=True)

st.markdown("### ENTER YOUR TASKS:")
user_input = st.text_area("Enter your tasks:", key="user_text", label_visibility="collapsed", height=130, placeholder="e.g., Buy groceries today...")

c_run, c_clear = st.columns([3,1])
with c_run:
    run = st.button("🚀 ORGANISE TASKS", type="primary", use_container_width=True)
with c_clear:
    st.button("🗑️ CLEAR", on_click=clear_text, use_container_width=True)

if run:
    if not user_input.strip():
        st.warning("Please enter some tasks!")
    else:
        with st.spinner("Agent is thinking..."):
            result = graph_app.invoke({"user_input": user_input, "extracted_tasks": [], "prioritized_tasks": [], "formatted_output": ""})
            st.markdown('<hr style="border-color:#FF1E1E;">', unsafe_allow_html=True)
            t1, t2, t3 = st.tabs(["01 EXTRACTED", "02 PRIORITIZED", "03 FINAL"])
            with t1: st.json(result["extracted_tasks"])
            with t2:
                for t in result["prioritized_tasks"]:
                    p = t.get('priority','Medium')
                    icon = "🔴" if p=="High" else "🟡" if p=="Medium" else "🟢"
                    st.markdown(f"### {icon} [{p}] {t.get('task')}")
            with t3: st.code(result["formatted_output"], language="text")