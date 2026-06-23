import streamlit as st
from agent import agent_chat, get_history, clear_history

# 页面配置
st.set_page_config(
    page_title="校园百事通",
    page_icon="🏫",
    layout="centered"
)

# 标题
st.title("🏫 校园生活百事通助手")
st.caption("帮你解答请假、奖学金、报修等校园生活问题")

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 侧边栏 - 功能按钮
with st.sidebar:
    st.header("📋 功能说明")
    st.markdown("""
    **我能帮你：**
    - 📝 回答校园问题（请假、奖学金、报修等）
    - 📅 查询当前校历周数
    - 📊 计算绩点（输入：85,90,78）
    - 💬 多轮对话记忆
    """)
    
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("Made with ❤️ 校园百事通")

# 输入框
if prompt := st.chat_input("问点校园问题..."):
    # 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 调用智能体
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = agent_chat(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})