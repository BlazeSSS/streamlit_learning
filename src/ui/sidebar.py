import streamlit as st

from src.util import interact_utils


async def create_sidebar():
    st.title("MCP 工具")
    # st.radio(
    #     "Transport",
    #     ["stdio", "sse", "streamable-http"],
    #     index=1,
    #     disabled=True,
    #     horizontal=True,
    # )

    # MCP 服务信息
    st.selectbox(
        "Transport",
        ["stdio", "sse", "streamable-http"],
        index=1,
        disabled=True,
        key="mcp_transport",
    )
    st.text_input("MCP Server URL", "http://127.0.0.1:8000/sse", key="mcp_url")

    agent = interact_utils.get_agent()

    # MCP 服务连接按钮
    if not st.session_state.mcp_connect:
        if st.button("Connect", use_container_width=True):
            is_connected = await agent.try_mcp_connect(st.session_state.mcp_url, st.session_state.mcp_transport)
            if is_connected:
                st.session_state.mcp_connect = True
                st.rerun()
            else:
                st.session_state.mcp_connect = False
                st.error('MCP connected Failed.')
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Reconnect", use_container_width=True):
                is_connected = await agent.try_mcp_connect(st.session_state.mcp_url, st.session_state.mcp_transport)
                if is_connected:
                    st.session_state.mcp_connect = True
                else:
                    st.session_state.mcp_connect = False
                    st.error('MCP connected Failed.')
        with col2:
            if st.button("Disconnect", use_container_width=True):
                st.session_state.mcp_connect = False
                agent.disconnect_mcp()
                st.rerun()

    # MCP 服务连接状态
    if st.session_state.mcp_connect:
        st.badge("Connected", icon=":material/check:", color="green")
    else:
        st.badge("Disconnected", icon=":material/close:", color="gray")

    # MCP 服务工具列表
    if st.button("Tools list", disabled=not st.session_state.mcp_connect, use_container_width=True):
        show_tools()

    # 清空上下文
    if st.button("Clear Context", use_container_width=True):
        st.session_state.chat_history = []


@st.dialog("Tools")
def show_tools():
    agent = interact_utils.get_agent()
    if not agent.tools:
        st.write("Tool is empty.")
    else:
        for tool in agent.tools:
            with st.expander(tool['function']['name']):
                st.markdown(tool['function']['description'])
