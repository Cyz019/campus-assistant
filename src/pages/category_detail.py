import streamlit as st
import pandas as pd
from agent import agent_chat, get_history, clear_history, set_category, get_category

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="类别详情 - 校园小智",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# 移除导航文字 - 保留侧边栏
# ============================================================
st.components.v1.html("""
<script>
(function() {
    function removeNavTexts() {
        var walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: function(node) {
                    var text = node.textContent.trim();
                    if (text === 'app' || text === 'category detail' || 
                        text === 'categorydetail' || text === 'category_detail' ||
                        text === 'category' || text === 'detail') {
                        return NodeFilter.FILTER_ACCEPT;
                    }
                    return NodeFilter.FILTER_REJECT;
                }
            }
        );
        var nodesToRemove = [];
        var node;
        while (node = walker.nextNode()) {
            nodesToRemove.push(node);
        }
        for (var i = 0; i < nodesToRemove.length; i++) {
            var n = nodesToRemove[i];
            if (n.parentNode) {
                n.parentNode.removeChild(n);
            }
        }
        
        var allElements = document.querySelectorAll('*');
        for (var i = 0; i < allElements.length; i++) {
            var el = allElements[i];
            if (el.childNodes.length === 1 && el.childNodes[0].nodeType === 3) {
                var text = el.textContent.trim();
                if (text === 'app' || text === 'category detail' || 
                    text === 'categorydetail' || text === 'category_detail') {
                    el.remove();
                }
            }
        }
        
        var allDivs = document.querySelectorAll('div');
        for (var d = 0; d < allDivs.length; d++) {
            var div = allDivs[d];
            if (div.textContent && div.textContent.includes('/') && 
                div.textContent.includes('app')) {
                div.remove();
            }
        }
    }
    
    removeNavTexts();
    setTimeout(removeNavTexts, 100);
    setTimeout(removeNavTexts, 300);
    setTimeout(removeNavTexts, 500);
    setTimeout(removeNavTexts, 1000);
    
    var observer = new MutationObserver(function() {
        removeNavTexts();
    });
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        characterData: true
    });
})();
</script>
<style>
    /* 只隐藏面包屑导航，不隐藏侧边栏内容 */
    .stBreadcrumbs, .stBreadcrumbs *,
    .stPageTitle, .stPageTitle * {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
        position: absolute !important;
        top: -9999px !important;
        left: -9999px !important;
        opacity: 0 !important;
        pointer-events: none !important;
        margin: 0 !important;
        padding: 0 !important;
        border: 0 !important;
        min-height: 0 !important;
        max-height: 0 !important;
    }
</style>
""", height=0)

# ============================================================
# 初始化状态
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_question" not in st.session_state:
    st.session_state.selected_question = None
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []
if "detail_category" not in st.session_state:
    st.session_state.detail_category = None

# ============================================================
# 加载数据
# ============================================================
@st.cache_data
def load_campus_data():
    df = pd.read_csv('data/campus_data.csv')
    return df

df = load_campus_data()

# ============================================================
# CSS 样式
# ============================================================
st.markdown("""
<style>
    /* ===== 隐藏侧边栏 ===== */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    .stApp {
        background: linear-gradient(160deg, #eef0f5 0%, #e2e6ef 50%, #d5dce8 100%);
    }
    
    .detail-header {
        text-align: center;
        padding: 1.8rem 0 1.2rem 0;
        background: linear-gradient(135deg, #0b1a33 0%, #1a3a6b 45%, #1e4d8a 100%);
        border-radius: 18px;
        color: white;
        margin-bottom: 1.8rem;
        box-shadow: 0 12px 40px rgba(10, 30, 70, 0.35);
        border: 1px solid rgba(255, 215, 0, 0.08);
        position: relative;
        overflow: hidden;
    }
    .detail-header::before {
        content: '';
        position: absolute;
        top: -60%;
        right: -20%;
        width: 60%;
        height: 200%;
        background: radial-gradient(ellipse, rgba(255, 215, 0, 0.04) 0%, transparent 70%);
        pointer-events: none;
    }
    .detail-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, #FFD700, #FFD700, transparent);
        opacity: 0.3;
    }
    .detail-header h1 {
        font-size: 2.4rem;
        margin: 0;
        font-weight: 700;
        letter-spacing: 4px;
        position: relative;
    }
    .detail-header h1 .gold {
        color: #FFD700;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.15);
    }
    .detail-header .sub {
        font-size: 0.9rem;
        opacity: 0.5;
        margin: 6px 0 0 0;
        letter-spacing: 6px;
        font-weight: 300;
        position: relative;
    }
    .detail-header .category-badge {
        display: inline-block;
        background: rgba(255, 215, 0, 0.12);
        border: 1px solid rgba(255, 215, 0, 0.15);
        padding: 6px 24px;
        border-radius: 30px;
        font-size: 0.85rem;
        color: #FFD700;
        letter-spacing: 2px;
        margin-top: 12px;
        position: relative;
    }
    
    .question-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-bottom: 20px;
    }
    @media (max-width: 768px) {
        .question-grid {
            grid-template-columns: 1fr;
        }
    }
    
    .qa-container {
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 14px;
        padding: 20px 24px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 2px 12px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }
    .qa-container .qa-question {
        font-size: 1.05rem;
        font-weight: 600;
        color: #1a3a6b;
        margin-bottom: 12px;
        padding-bottom: 12px;
        border-bottom: 2px solid rgba(255, 215, 0, 0.15);
    }
    .qa-container .qa-answer {
        font-size: 0.95rem;
        color: #2a3a5a;
        line-height: 1.8;
    }
    
    .stChatInput input {
        border-radius: 30px !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        padding: 14px 24px !important;
        font-size: 15px !important;
        background: rgba(255, 255, 255, 0.5) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        color: #1a2a4a !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04) !important;
        transition: all 0.3s ease !important;
    }
    .stChatInput input::placeholder {
        color: #8a9bb5 !important;
    }
    .stChatInput input:focus {
        border-color: #FFD700 !important;
        background: rgba(255, 255, 255, 0.7) !important;
        box-shadow: 0 0 0 4px rgba(255, 215, 0, 0.06), 0 4px 20px rgba(0,0,0,0.06) !important;
    }
    .stChatMessage {
        border-radius: 14px !important;
        padding: 14px 20px !important;
        margin-bottom: 12px !important;
        border: none !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.03) !important;
    }
    .stChatMessage.user {
        background: linear-gradient(135deg, #1a3a6b, #2a5a9a) !important;
        color: white !important;
    }
    .stChatMessage.user .stMarkdown {
        color: white !important;
    }
    .stChatMessage.assistant {
        background: rgba(255, 255, 255, 0.5) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .user-info {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.5);
        text-align: right;
        margin-top: -10px;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }
    
    .empty-state {
        text-align: center;
        padding: 40px 20px;
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .empty-state .icon {
        font-size: 3rem;
        margin-bottom: 8px;
    }
    .empty-state .title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a2a4a;
    }
    .empty-state .sub {
        font-size: 0.85rem;
        color: #7a8aaa;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 获取当前类别
# ============================================================
category = st.session_state.detail_category or "社团活动"

# 获取该类别下的问答数据
category_qa = df[df['category'] == category]

# ============================================================
# 页面头部
# ============================================================
col_back, col_title = st.columns([1, 5])
with col_back:
    if st.button("← 返回首页", key="back_home", use_container_width=True):
        st.session_state.detail_category = None
        st.session_state.selected_question = None
        st.session_state.messages = []
        st.switch_page("app.py")

with col_title:
    st.markdown(f"""
    <div class="detail-header" style="margin-top:0;">
        <h1>📋 类别<span class="gold">详情</span></h1>
        <div class="sub">✦ 校园小智 · 智能问答 ✦</div>
        <div class="category-badge">📌 {category}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="user-info">👤 欢迎，{st.session_state.student_id}</div>', unsafe_allow_html=True)

# ============================================================
# 显示该类别下的所有问答
# ============================================================
if not category_qa.empty:
    st.markdown(f"<p style='font-size:0.9rem;color:#5a6a8a;margin-bottom:14px;'>共 <strong>{len(category_qa)}</strong> 条问答</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="question-grid">', unsafe_allow_html=True)
    
    for idx, row in category_qa.iterrows():
        question = row['question']
        answer = row['answer']
        
        if st.button(
            f"💬 {question}",
            key=f"q_{idx}",
            use_container_width=True,
            help="点击查看答案"
        ):
            st.session_state.selected_question = question
            st.session_state.qa_history.append({
                "question": question,
                "answer": answer
            })
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.selected_question:
        selected_row = category_qa[category_qa['question'] == st.session_state.selected_question]
        if not selected_row.empty:
            answer = selected_row.iloc[0]['answer']
            
            st.markdown(f"""
            <div class="qa-container">
                <div class="qa-question">❓ {st.session_state.selected_question}</div>
                <div class="qa-answer">{answer}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="margin-top:-10px;margin-bottom:16px;font-size:0.8rem;color:#8a9bb5;">
                💡 如有疑问，可以在下方继续追问
            </div>
            """, unsafe_allow_html=True)
    
    prompt = st.chat_input("💬 输入你的问题...")
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("✦ 思考中..."):
                context = ""
                if st.session_state.selected_question:
                    context = f"用户刚才查看了问题：{st.session_state.selected_question}，现在追问："
                response = agent_chat(f"{context}{prompt}")
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.rerun()
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

else:
    st.markdown("""
    <div class="empty-state">
        <div class="icon">📭</div>
        <div class="title">该类别暂无问答</div>
        <div class="sub">请返回首页选择其他类别</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 底部操作栏
# ============================================================
st.divider()

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    if st.button("🏠 返回首页", use_container_width=True):
        st.session_state.detail_category = None
        st.session_state.selected_question = None
        st.session_state.messages = []
        st.switch_page("app.py")

with col2:
    if st.button("🔄 刷新列表", use_container_width=True):
        st.rerun()

with col3:
    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.messages = []
        st.session_state.selected_question = None
        st.rerun()

with col4:
    if st.button("🚪 退出登录", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.student_id = ""
        st.session_state.messages = []
        st.session_state.detail_category = None
        st.session_state.selected_question = None
        clear_history()
        st.switch_page("app.py")

# ============================================================
# 页脚
# ============================================================
st.markdown("""
<div style="text-align:center;padding:20px 0 10px 0;font-size:0.7rem;color:#8a9bb5;letter-spacing:3px;">
    ✦ 校园小智 · 安徽交通职业技术学院 ✦
</div>
""", unsafe_allow_html=True)