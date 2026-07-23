import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
from agent.orchestrator import ask_agent

def show():
    st.title("💬 DataMind — Ask Your Data")
    st.markdown("*Type any business question and get instant AI-powered insights*")
    st.divider()

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

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "question" not in st.session_state:
        st.session_state.question = ""

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask anything about your business data...")

    if st.session_state.question:
        question = st.session_state.question
        st.session_state.question = ""

    if question:
        with st.chat_message("user"):
            st.markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("assistant"):
            with st.spinner("DataMind is analysing your data..."):
                response = ask_agent(question)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
