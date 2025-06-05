import streamlit as st


def get_session_value(key):
    return st.session_state.get(key)


def set_session_value(key, value):
    st.session_state[key] = value
