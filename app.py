import asyncio

import streamlit as st
from dotenv import load_dotenv

from src.ui import sidebar, chat_box
from src.util import interact_utils

load_dotenv()


async def mian():
    st.set_page_config(
        page_title="Agent With MCP",
        page_icon=":rocket:",
        layout="wide",
    )

    # 初始化 MCP 状态
    interact_utils.init_session_state()
    # 加载 CSS
    with open("src/ui/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    #  侧边栏
    with st.sidebar:
        await sidebar.create_sidebar()
    # 对话框
    await chat_box.create_chat_box()


if __name__ == "__main__":
    asyncio.run(mian())
