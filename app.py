import streamlit as st
from graph import build_graph

# --- 1. MUST BE FIRST LINE - centered = responsive ---
st.set_page_config(page_title="TASK ORGANISER AGENT", page_icon="✅", layout="centered")

# --- 2. YOUR EXACT COLOUR SCHEME + RESPONSIVE ---
st.markdown("""
<style>
.stApp { background-color: #0A0A0A; color: #FFFFFF; }
.block-container {
    max-width: 900px !important;
    padding-left: 20px !important;
    padding-right: 20px !important;
    padding-top: 30px !important;
}
h1, h2, h3, p, label { color: #FFFFFF !important; }
div[data-testid="stTextArea"] textarea {
    background-color: #1A1A1A !important;
    color: #FFFFFF !important;
    border: 1px solid #333 !important;
    border-radius: 6px !important;
}
button[kind="primary"] {
    background-color: #FF1E1E !important;
    color: white !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    border: none !important;
}
button[kind="primary"]:hover {
    background-color: #e01818 !important;
}
.stTabs [data-baseweb="tab"] { color: #888; }
.stTabs [aria-selected="true"] { color: #FF1E1E !important; }
hr { border-color: #FF1E1E !important; }
.card {
    border: 1px solid #222; 
    padding: 14px; 
    background: #111; 
    border-radius: 8px;
    height: 125px;
    transition: border-color 0.2s;
}
.card:hover {
    border-color: #FF1E1E;
}
.card-num { color: #FF1E1E; font-weight: 700; font-size: 11px; letter-spacing: 1px; }
.card-title { font-size: 11px; font-weight: 700; margin: 6px 0; color: #fff; }
.card-desc { font-size: 10px; color: #888; line-height: 1.4; }
@media (max-width: 768px) {
    h1 { font-size: 24px !important; }
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p style="color:#FF1E1E; font-size:10px; letter-spacing:2px; font-weight:700;">TASK ORGANISER AGENT</p>', unsafe_allow_html=True)
st.markdown('<h1 style="line-height:1.1;">3-STEP<br>TASK<br>ORGANISER <span style="color:#FF1E1E;">AGENT</span></h1>', unsafe_allow_html=True)
st.markdown('<hr style="border:1px solid #FF1E1E;">', unsafe_allow_html=True)

col_top1, col_top2 = st.columns([3,1])
with col_top1:
    st.markdown('<p style="font-size:9px; color:#888;">■ BUILT WITH LANGGRAPH | STREAMLIT + GEMINI 2.0 FLASH</p>', unsafe_allow_html=True)
with col_top2:
    st.markdown('<p style="text-align:right; font-size:9px; font-weight:700;">LEARN. <span style="color:#FF1E1E;">ORGANISE.</span> EXECUTE.</p>', unsafe_allow_html=True)

# --- SESSION STATE + HELPERS ---
if "user_text" not in st.session_state:
    st.session_state.user_text = "submit assignment tomorrow 5pm, buy milk egg, pay bills next week"

def set_example(text):
    st.session_state.user_text = text

def clear_text():
    st.session_state.user_text = ""

# --- CARDS - CLICKABLE EXAMPLES ---
st.markdown("<p style='font-size:11px; color:#888; margin-bottom:10px;'>CHOOSE A QUICK EXAMPLE OR TYPE YOUR OWN:</p>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="card"><div class="card-num">01</div><div class="card-title">DAILY TASKS</div><div class="card-desc">Buy groceries today, finish assignment tomorrow, plan vacation.</div></div>', unsafe_allow_html=True)
    st.button("Load Example 1", key="ex1", on_click=set_example, args=("Buy groceries today, finish assignment tomorrow, and plan vacation next month.",), use_container_width=True)
with c2:
    st.markdown('<div class="card"><div class="card-num">02</div><div class="card-title">WEEKLY PLAN</div><div class="card-desc">Pay electricity bill asap, prepare for exam, call mom next week.</div></div>', unsafe_allow_html=True)
    st.button("Load Example 2", key="ex2", on_click=set_example, args=("Pay electricity bill asap, prepare for exam this week, call mom next week",), use_container_width=True)
with c3:
    st.markdown('<div class="card"><div class="card-num">03</div><div class="card-title">URGENT TASKS</div><div class="card-desc">Submit report today, schedule meeting, buy milk and egg.</div></div>', unsafe_allow_html=True)
    st.button("Load Example 3", key="ex3", on_click=set_example, args=("Submit report today, schedule meeting tomorrow, buy milk and egg",), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### ENTER YOUR TASKS:")
user_input = st.text_area("Enter your tasks:", key="user_text", label_visibility="collapsed", height=120, placeholder="e.g., Buy groceries today...")

c_run, c_clear = st.columns([3,1])
with c_run:
    run = st.button("🚀 ORGANISE TASKS", type="primary", use_container_width=True)
with c_clear:
    st.button("🗑️ CLEAR", on_click=clear_text, use_container_width=True)

# --- EXECUTION & USER-FRIENDLY OUTPUT ---
if run:
    if not user_input.strip():
        st.warning("Please enter some tasks!")
    else:
        with st.spinner("Agent is analyzing and sorting your tasks..."):
            graph = build_graph()
            result = graph.invoke({"user_input": user_input, "extracted_tasks": [], "prioritized_tasks": [], "formatted_output": ""})
        
        st.markdown('<hr style="border-color:#FF1E1E; margin-top:35px; margin-bottom:25px;">', unsafe_allow_html=True)
        
        # Section Header with Summary Metrics
        prioritized = result.get('prioritized_tasks', [])
        high_count = sum(1 for item in prioritized if "high" in item.get('priority', '').lower())
        med_count = sum(1 for item in prioritized if "medium" in item.get('priority', '').lower())
        low_count = sum(1 for item in prioritized if "low" in item.get('priority', '').lower())

        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h3 style="margin:0; font-size:18px;">✨ Your Organized Action Plan</h3>
            <span style="font-size:11px; color:#888; background:#161616; padding:4px 10px; border-radius:12px; border:1px solid #333;">
                Total Tasks: <b>{len(prioritized)}</b> | High Priority: <span style="color:#FF1E1E;">{high_count}</span>
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Render tasks cleanly sorted or grouped
        for idx, item in enumerate(prioritized):
            task = item.get('task', '')
            prio = item.get('priority', 'Low').lower()
            
            # Styling based on priority
            if "high" in prio:
                col = "#FF1E1E"
                lbl = "HIGH PRIORITY"
            elif "low" in prio:
                col = "#10B981"
                lbl = "LOW PRIORITY"
            else:
                col = "#F59E0B"
                lbl = "MEDIUM PRIORITY"

            st.markdown(f"""
            <div style="border-left: 4px solid {col}; background: #141414; padding: 12px 16px; margin-bottom: 10px; border-radius: 0 6px 6px 0; display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center;">
                    <span style="background: {col}; color: white; font-size: 8px; font-weight: 800; padding: 3px 8px; border-radius: 12px; letter-spacing: 0.5px;">{lbl}</span>
                    <span style="margin-left: 14px; color: white; font-size: 13px; font-weight: 500;">{task}</span>
                </div>
                <span style="color: #555; font-size: 11px;">#{idx+1}</span>
            </div>
            """, unsafe_allow_html=True)

        # Clean, collapsible Developer/Teacher view instead of confusing tabs
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🛠️ Developer / Evaluator Mode (LangGraph Pipeline Steps)"):
            st.markdown("<p style='font-size:11px; color:#888;'>Under the hood view showing how the agent processed the state across nodes:</p>", unsafe_allow_html=True)
            t1, t2, t3 = st.tabs(["01 Extracted State", "02 Prioritized State", "03 Final Text Output"])
            with t1: 
                st.json(result["extracted_tasks"])
            with t2: 
                st.json(result["prioritized_tasks"])
            with t3: 
                st.code(result["formatted_output"], language="text")

