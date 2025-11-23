import streamlit as st
import requests
import uuid

# Configuration
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Interview Practice Partner", page_icon="🤖")

st.title("🤖 Interview Practice Partner")
st.markdown("Select a role and start your mock interview!")

# Session State Initialization
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "interview_active" not in st.session_state:
    st.session_state.interview_active = False

# Sidebar - Configuration
with st.sidebar:
    st.header("Setup")
    role = st.selectbox("Choose Role", ["Software Engineer", "Product Manager", "Data Scientist", "Sales Associate", "Customer Support"])
    experience = st.selectbox("Experience Level", ["Junior", "Mid-Level", "Senior"])
    
    if st.button("Start New Interview"):
        try:
            response = requests.post(f"{BACKEND_URL}/start_session", json={"role": role, "experience_level": experience})
            if response.status_code == 200:
                data = response.json()
                st.session_state.session_id = data["session_id"]
                st.session_state.messages = [{"role": "assistant", "content": data["initial_message"]}]
                st.session_state.interview_active = True
                st.rerun()
            else:
                st.error("Failed to start session. Is backend running?")
        except Exception as e:
            st.error(f"Connection error: {e}")

# Main Chat Interface
if st.session_state.interview_active:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    # Chat input (Text)
    if prompt := st.chat_input("Type your answer..."):
        # ... (Text logic remains same) ...
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            with st.spinner("Interviewer is thinking..."):
                response = requests.post(
                    f"{BACKEND_URL}/chat", 
                    json={"session_id": st.session_state.session_id, "user_message": prompt}
                )
                if response.status_code == 200:
                    data = response.json()
                    agent_msg = data["agent_message"]
                    st.session_state.messages.append({"role": "assistant", "content": agent_msg})
                    with st.chat_message("assistant"):
                        st.markdown(agent_msg)
                    if data["is_interview_over"]:
                        st.session_state.interview_active = False
                        st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

    # --- Audio Input ---
    st.markdown("---")
    
    # Read the HTML component
    import os
    with open("frontend/vad_component.html", "r") as f:
        vad_html = f.read()
        
    # Inject into Streamlit
    st.components.v1.html(vad_html, height=300)
    
    st.info("ℹ️ **Live Mode**: Click 'Start Interview'. The app will listen. When you stop talking for 2 seconds, it will automatically reply.")

else:
    if st.session_state.session_id:
        st.info("Interview finished. Check back for feedback (Coming Soon).")
    else:
        st.info("👈 Please select a role and click 'Start New Interview' to begin.")
