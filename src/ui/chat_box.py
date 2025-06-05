import streamlit as st

from src.agent import agent

def create_chat_box():
    # 显示对话历史
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # 用户输入消息
    user_input = st.chat_input("Type a message...")
    if user_input:
        # 显示用户输入
        with st.chat_message("user"):
            st.write(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
        # 处理用户输入
        agent.process_query(user_input)

        # 显示AI响应
        with st.chat_message("assistant"):
            st.write("Assistant's response")
            st.session_state.chat_history.append({"role": "assistant", "content": "Assistant's response"})

        # 显示tool响应
        with st.chat_message("tool"):
            st.write("tool's response")
            st.session_state.chat_history.append({"role": "tool", "content": "tool's response"})
