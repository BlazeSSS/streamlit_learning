import json

import streamlit as st
from streamlit_echarts import st_echarts

from src.util import interact_utils


async def create_chat_box():
    # 显示对话历史
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        if message['role'] == 'tool':
            with st.expander('Tool Result'):
                with st.chat_message(message['role']):
                    st.write(message['content'])
            # 渲染 echart 结果
            _rendering(message['content'])
        else:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    agent = interact_utils.get_agent()
    # 用户输入消息
    user_input = st.chat_input("Type a message...")
    if user_input:
        # 显示用户输入
        with st.chat_message("user"):
            st.write(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
        # 处理用户输入
        use_tools, res_stream = agent.process_query(user_input)

        # 显示AI响应
        with st.chat_message("assistant"):
            with st.empty():
                final_res = st.write_stream(res_stream)
                st.session_state.chat_history.append({"role": "assistant", "content": final_res})

        # 显示tool响应
        if use_tools:
            tool_name, tool_args = _get_tool_call(final_res)
            tool_result = await agent.call_tool(tool_name, tool_args)

            with st.expander("Tool Result"):
                with st.chat_message("tool"):
                    st.write(tool_result)
                    st.session_state.chat_history.append({"role": "tool", "content": tool_result})
            # 渲染 echart 结果
            _rendering(tool_result)


def _get_tool_call(tool_call):
    tool_call_str = tool_call.strip('</tool_call>')
    tool_call = json.loads(tool_call_str)
    tool_name = tool_call['name']
    tool_args = tool_call['arguments']
    return tool_name, tool_args


def _rendering(tool_result):
    result_json = json.loads(tool_result)
    if 'options' not in result_json:
        return
    options = result_json['options']
    st_echarts(options=options, height='500px')
