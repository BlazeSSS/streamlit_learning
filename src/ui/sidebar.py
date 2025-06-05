import streamlit as st
import time

from src.util import interact_utils


def create_sidebar():
    st.title("MCP 工具")
    # st.radio(
    #     "Transport",
    #     ["stdio", "sse", "streamable-http"],
    #     index=1,
    #     disabled=True,
    #     horizontal=True,
    # )
    st.selectbox(
        "Transport",
        ["stdio", "sse", "streamable-http"],
        index=1,
        disabled=True,
        key="mcp_transport",
    )
    st.text_input("MCP Server URL", "http://127.0.0.1:8000/sse", key="mcp_url")

    if "mcp_connect" not in st.session_state:
        st.session_state.mcp_connect = False

    if st.button("Connect", use_container_width=True):
        st.session_state.mcp_connect = True

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Reconnect", use_container_width=True):
            st.session_state.mcp_connect = True
    with col2:
        if st.button("Disconnect", use_container_width=True):
            st.session_state.mcp_connect = False

    if st.session_state.mcp_connect:
        st.badge("Connected", icon=":material/check:", color="green")
    else:
        st.badge("Disconnected", icon=":material/close:", color="gray")

    if st.button(
        "Tools list",
        disabled=not st.session_state.mcp_connect,
        use_container_width=True,
    ):
        show_tools()
    st.button("Clear Context", use_container_width=True)


@st.dialog("Tools")
def show_tools():
    with st.expander("fucntion 1"):
        st.write("Description of function 1")
    with st.expander("fucntion 1"):
        st.write("Description of function 1")
