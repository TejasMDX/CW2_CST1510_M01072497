import streamlit as st
from google import genai
from app.data.incidents import get_all_incidents
from app.data.tickets import get_all_tickets
from app.data.datasets import get_all_metadata
from app.data.db import connect_database

#if not st.session_state.logged_in:
    #st.error("You must be logged in to view this page")
    #if st.button("Go to login"):
        #st.switch_page("Home.py")
    #st.stop()
    

# Initialize Gemini client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

conn = connect_database()
incidents = get_all_incidents(conn)
tickets = get_all_tickets(conn)
datasets = get_all_metadata(conn)

if 'incidents_messages' not in st.session_state: 
    st.session_state.incidents_messages = []

    all_incidents = incidents.to_string()

    text = f"""You are given the table of all incidents: {all_incidents} \n
            You are a cybersecurity expert assistant.
            - Analyze incidents and threats
            - Provide technical guidance
            - Explain attack vectors & mitigations
            - Use standard terminology (MITRE, CVE)
            - Prioritize actionable recommendations \n
            Tone: Professional, technical and human like\n
            Format: Clear steps
            """
    st.session_state.incidents_messages.append({"role": "model", "parts":[{"text":text}]})
    
    st.session_state.incidents_messages.append({"role": "model", "parts":[{"text":"I am your cybersecurity expert assistant."}]})

if 'tickets_messages' not in st.session_state:
    st.session_state.tickets_messages = []

    all_tickets  = tickets.to_string()

    text = f""" You are given the table of all tickets: {all_tickets} \n
            You are an IT Operations expert assistant.
            - Ticket triage & prioritization
            - Troubleshooting guidance
            - System optimization tips
            - Infrastructure best practices
            - Provide practical, actionable solutions
            Tone: Professional, technical and human like\n
            Format: Clear steps
            """
    
    st.session_state.tickets_messages.append({"role": "model", "parts":[{"text":text}]})

    st.session_state.tickets_messages.append({"role": "model", "parts":[{"text":"I am your IT Operations expert assistant."}]})

if 'datasets_messages' not in st.session_state:
    st.session_state.datasets_messages = []

    all_datasets = datasets.to_string()

    text = f""" You are given the table of all datasets: {all_datasets} \n
            You are a Data Science expert assistant.
            - Dataset analysis & insights
            - Visualization recommendations
            - Statistical methods guidance
            - Machine learning technique suggestions
            - Explain concepts clearly and practically

            Tone: Professional, clear, and human-like
            Format: Clear steps
        """
    
    st.session_state.datasets_messages.append({"role": "model", "parts":[{"text":text}]})

    st.session_state.datasets_messages.append({"role": "model", "parts":[{"text":"I am your Data Science expert assistant."}]})


if "ai_index" not in st.session_state: st.session_state.ai_index = None

messages = [st.session_state.incidents_messages,st.session_state.tickets_messages,st.session_state.datasets_messages]

titles = ["Cyber Incidents Assistant","IT Tickets Assistant","Datasets Metadata Assistant"]

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

       

if st.session_state.ai_index is not None:
    st.title(titles[st.session_state.ai_index])

    prompt	= st.chat_input("Say something...")

    for message	in messages[st.session_state.ai_index][1:]:
        #ui_role = "assistant" if message["role"] == "model" else "user"
        with st.chat_message(message["role"]):
            st.markdown(message["parts"][0]["text"])

    if prompt:

        with st.chat_message("user"):
            st.markdown(prompt)

            messages[st.session_state.ai_index].append({"role":"user","parts":[{"text":prompt}]})

        response = client.models.generate_content_stream(
            model = "gemini-2.5-flash",
            contents = messages[st.session_state.ai_index],
        )
        
        full_reply = ""
        for chunk in response:
            full_reply += chunk.text
        
        with st.chat_message("model"):
            st.markdown(full_reply)
        messages[st.session_state.ai_index].append({"role":"model","parts":[{"text":full_reply}]})

