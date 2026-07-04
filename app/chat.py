import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from agent.orchestrator import ask_agent

st.set_page_config(
    page_title="DataMind — Chat",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 DataMind — Ask Your Data")
st.markdown("*Type any business question and get instant AI-powered insights*")
st.divider()

# Suggested questions
st.markdown("**Suggested questions:**")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Which region is underperforming?"):
        st.session_state.question = "Which region is underperforming and why?"
with col2:
    if st.button("What should I restock urgently?"):
        st.session_state.question = "What products should I restock urgently?"
with col3:
    if st.button("Who are my top customers?"):
        st.session_state.question = "Who are my top customers by revenue?"

st.divider()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "question" not in st.session_state:
    st.session_state.question = ""

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("Ask anything about your business data...")

# Handle suggested question buttons
if st.session_state.question:
    question = st.session_state.question
    st.session_state.question = ""

if question:
    # Show user message
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("DataMind is analysing your data..."):
            response = ask_agent(question)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})