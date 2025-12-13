import streamlit as st
from app.data.incidents import get_all_incidents
from app.data.tickets import get_all_tickets
from app.data.datasets import get_all_metadata
from app.data.db import connect_database
from services.ai_assistant import AIAssistant

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]

conn = connect_database()
incidents = get_all_incidents(conn)
tickets = get_all_tickets(conn)
datasets = get_all_metadata(conn)

if "assistants" not in st.session_state:
    st.session_state.assistants = {}

    st.session_state.assistants[0] = AIAssistant(
        api_key=api_key,
        system_prompt=f"""
You are given the table of all incidents:
{incidents.to_string()}

You are a cybersecurity expert assistant.
- Analyze incidents and threats
- Provide technical guidance
- Explain attack vectors & mitigations
- Use standard terminology (MITRE, CVE)
- Prioritize actionable recommendations

Tone: Professional, technical, human-like
Format: Clear steps
"""
    )

    st.session_state.assistants[1] = AIAssistant(
        api_key=api_key,
        system_prompt=f"""
You are given the table of all tickets:
{tickets.to_string()}

You are an IT Operations expert assistant.
- Ticket triage & prioritization
- Troubleshooting guidance
- System optimization tips
- Infrastructure best practices

Tone: Professional, technical, human-like
Format: Clear steps
"""
    )

    st.session_state.assistants[2] = AIAssistant(
        api_key=api_key,
        system_prompt=f"""
You are given the table of all datasets:
{datasets.to_string()}

You are a Data Science expert assistant.
- Dataset analysis & insights
- Visualization recommendations
- Statistical methods guidance
- Machine learning technique suggestions

Tone: Professional, clear, human-like
Format: Clear steps
"""
    )


if "chat_ui" not in st.session_state:
    st.session_state.chat_ui = {
        0: [],
        1: [],
        2: []
    }

titles = [
    "🤖 Cyber Incidents Assistant",
    "🤖 IT Tickets Assistant",
    "🤖 Datasets Metadata Assistant"
]

if "ai_index" not in st.session_state:
    st.session_state.ai_index = None

col1, col2, col3 = st.columns(3)
if col1.button("Cyber Incidents Assistant"):
    st.session_state.ai_index = 0
    st.rerun()

if col2.button("IT Tickets Assistant"):
    st.session_state.ai_index = 1
    st.rerun()

if col3.button("Datasets Metadata Assistant"):
    st.session_state.ai_index = 2
    st.rerun()

if st.session_state.ai_index is None:
    st.info("Choose one AI assistant")
    st.stop()


assistant = st.session_state.assistants[st.session_state.ai_index]
ui_messages = st.session_state.chat_ui[st.session_state.ai_index]

st.title(titles[st.session_state.ai_index])

for msg in ui_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

prompt = st.chat_input("Say something...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    ui_messages.append({"role": "user", "text": prompt})

    response = assistant.send_message(prompt)

    with st.chat_message("model"):
        st.markdown(response)

    ui_messages.append({"role": "model", "text": response})
