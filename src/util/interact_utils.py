import streamlit as st

from src.agent.agent import Agent


def get_session_value(key):
    return st.session_state.get(key)


def set_session_value(key, value):
    st.session_state[key] = value

def init_session_state():
    if "mcp_connect" not in st.session_state:
        st.session_state.mcp_connect = False

@st.cache_resource
def get_agent():
    return Agent('Simple Agent', 'desc')