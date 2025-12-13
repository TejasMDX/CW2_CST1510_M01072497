import streamlit as st
from app.data.incidents import get_all_incidents
from app.data.tickets import get_all_tickets
from app.data.datasets import get_all_metadata
from app.data.db import connect_database
from services.ai_assistant import AIAssistant

#check if user is logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]

# Load data from database
conn = connect_database()
incidents = get_all_incidents(conn)
tickets = get_all_tickets(conn)
datasets = get_all_metadata(conn)

# Initialize AI assistants if not already done
if "assistants" not in st.session_state:
    st.session_state.assistants = {}
    # Cybersecurity assistant
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
    # IT Operations assistant
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
    # Data Science assistant
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

# Initialize chat history for each assistant
if "chat_ui" not in st.session_state:
    st.session_state.chat_ui = {
        0: [],
        1: [],
        2: []
    }
# Assistant titles
titles = [
    "🤖 Cyber Incidents Assistant",
    "🤖 IT Tickets Assistant",
    "🤖 Datasets Metadata Assistant"
]
# Track which AI assistant is active
if "ai_index" not in st.session_state:
    st.session_state.ai_index = None

# AI assistant selection buttons
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

# Require an assistant to be selected
if st.session_state.ai_index is None:
    st.info("Choose one AI assistant")
    st.stop()

# Chat UI
assistant = st.session_state.assistants[st.session_state.ai_index]
ui_messages = st.session_state.chat_ui[st.session_state.ai_index]

st.title(titles[st.session_state.ai_index])

# Display previous messages
for msg in ui_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# User input
prompt = st.chat_input("Say something...")

if prompt:
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    ui_messages.append({"role": "user", "text": prompt})
    # Send to AI assistant and get response
    response = assistant.send_message(prompt)

    # Show AI response
    with st.chat_message("model"):
        st.markdown(response)

    ui_messages.append({"role": "model", "text": response})
