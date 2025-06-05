import asyncio
import streamlit as st
from src.ui import sidebar, chat_box
import time

async def mian():
    st.set_page_config(
        page_title="Agent With MCP",
        page_icon=":rocket:",
        layout="wide",
    )
    # 初始化 MCP 状态

    # 对话框
    chat_box.create_chat_box()
    # st.header("MCP 工具列表")
    # st.write("这里是 MCP 工具列表")
    # 加载 CSS
    with open("src/ui/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    #  侧边栏
    with st.sidebar:
        sidebar.create_sidebar()
    # MCP 工具列表
    # with st.spinner("Wait for it...", show_time=True):
    #     time.sleep(5)


if __name__ == "__main__":
    asyncio.run(mian())
