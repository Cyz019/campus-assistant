import streamlit as st
import pandas as pd
from datetime import datetime
from agent import agent_chat, get_history, clear_history, set_category, get_category

# ============================================================
# 登录状态管理
# ============================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student_id" not in st.session_state:
    st.session_state.student_id = ""
if "saved_student_id" not in st.session_state:
    st.session_state.saved_student_id = ""
if "saved_password" not in st.session_state:
    st.session_state.saved_password = ""
if "detail_category" not in st.session_state:
    st.session_state.detail_category = None
if "selected_question" not in st.session_state:
    st.session_state.selected_question = None
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

# ============================================================
# 加载数据
# ============================================================
@st.cache_data
def load_campus_data():
    df = pd.read_csv('data/campus_data.csv')
    return df

df = load_campus_data()

# ============================================================
# 登录页面（未登录时显示）
# ============================================================
if not st.session_state.logged_in:
    st.set_page_config(
        page_title="校园小智 - 登录",
        page_icon="🎓",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    st.markdown("""
    <style>
        /* 隐藏侧边栏 */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        /* 隐藏右上角的菜单按钮 */
        button[kind="header"] {
            display: none !important;
        }
        /* 隐藏页面导航 */
        .stSidebarNav {
            display: none !important;
        }
        /* 隐藏顶部导航 */
        .stAppHeader {
            display: none !important;
        }
        header[data-testid="stHeader"] {
            display: none !important;
        }
        nav[data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        .stApp {
            background: linear-gradient(160deg, #1a2a4a 0%, #2a5a9a 50%, #3a7abd 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .stApp > div:first-child {
            background: transparent !important;
        }
        
        .login-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 75vh;
            padding: 20px;
        }
        .login-card {
            max-width: 420px;
            width: 100%;
            background: rgba(255, 255, 255, 0.10);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            padding: 36px 40px 30px 40px;
            border-radius: 28px;
            border: 1px solid rgba(255, 255, 255, 0.10);
            box-shadow: 0 30px 80px rgba(0,0,0,0.3);
            text-align: center;
            animation: fadeInUp 0.6s ease-out;
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .login-card .logo { font-size: 3.5rem; margin-bottom: 2px; display: block; }
        .login-card .title { font-size: 2rem; font-weight: 700; color: #fff; letter-spacing: 3px; }
        .login-card .title .gold { color: #FFD700; }
        .login-card .sub { font-size: 0.8rem; color: rgba(255,255,255,0.45); margin-top: 2px; margin-bottom: 20px; letter-spacing: 6px; }
        .login-card .divider {
            width: 50px; height: 2px;
            background: linear-gradient(90deg, transparent, #FFD700, transparent);
            margin: 0 auto 20px auto; border-radius: 10px;
        }
        .login-card .stTextInput {
            margin-top: -4px !important;
        }
        .login-card .stTextInput input {
            border-radius: 30px !important;
            border: 1px solid rgba(255, 255, 255, 0.10) !important;
            padding: 14px 20px !important;
            background: rgba(255, 255, 255, 0.05) !important;
            color: white !important;
            font-size: 15px !important;
            transition: all 0.3s ease !important;
        }
        .login-card .stTextInput input:focus {
            border-color: #FFD700 !important;
            background: rgba(255, 255, 255, 0.10) !important;
            box-shadow: 0 0 0 4px rgba(255, 215, 0, 0.06) !important;
        }
        .login-card .stTextInput input::placeholder {
            color: rgba(255, 255, 255, 0.3) !important;
        }
        .login-card .stTextInput label {
            color: rgba(255, 255, 255, 0.75) !important;
            font-size: 0.75rem !important;
            letter-spacing: 2px !important;
            text-transform: uppercase !important;
            margin-bottom: 2px !important;
            font-weight: 500 !important;
        }
        .login-card .stCheckbox label {
            color: rgba(255, 255, 255, 0.75) !important;
            font-size: 0.75rem !important;
            letter-spacing: 1px !important;
        }
        .login-card .stCheckbox label span {
            color: rgba(255, 255, 255, 0.75) !important;
        }
        .login-card .stCheckbox input[type="checkbox"] {
            accent-color: #FFD700 !important;
            width: 16px !important;
            height: 16px !important;
        }
        .checkbox-vertical {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2px;
            margin-top: 4px;
            margin-bottom: 10px;
        }
        .checkbox-vertical .stCheckbox {
            width: 100%;
            text-align: left;
            padding-left: 20px;
        }
        .login-card .stButton {
            display: flex;
            justify-content: center;
        }
        .login-card .stButton button {
            width: 70%;
            border-radius: 30px !important;
            padding: 14px !important;
            background: linear-gradient(135deg, #FFD700, #f5c800) !important;
            color: #0b1a33 !important;
            border: none !important;
            font-weight: 700 !important;
            font-size: 1.05rem !important;
            transition: all 0.3s ease !important;
            letter-spacing: 4px;
            margin-top: 2px;
            box-shadow: 0 4px 20px rgba(255, 215, 0, 0.15);
        }
        .login-card .stButton button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 12px 40px rgba(255, 215, 0, 0.30) !important;
        }
        .login-error {
            color: #ff6b6b;
            font-size: 0.8rem;
            margin-top: 10px;
            padding: 8px 16px;
            background: rgba(255, 80, 80, 0.06);
            border-radius: 30px;
            border: 1px solid rgba(255, 80, 80, 0.06);
        }
        .login-footer {
            text-align: center;
            margin-top: 24px;
            font-size: 0.65rem;
            color: rgba(255, 255, 255, 0.12);
            letter-spacing: 4px;
        }
        .stForm {
            margin-top: -8px !important;
        }
        .stForm > div {
            gap: 2px !important;
        }
        .feature-badge {
            display: inline-block;
            background: rgba(255, 215, 0, 0.06);
            border: 1px solid rgba(255, 215, 0, 0.04);
            padding: 2px 14px;
            border-radius: 30px;
            font-size: 0.6rem;
            color: rgba(255, 215, 0, 0.4);
            letter-spacing: 1px;
            margin: 2px;
        }
        .feature-row {
            margin-top: 16px;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 4px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-wrapper">
        <div class="login-card">
            <span class="logo">🎓</span>
            <div class="title">校园<span class="gold">小智</span></div>
            <div class="sub">✦ 你的校园生活助手 ✦</div>
            <div class="divider"></div>
            <div class="feature-row">
                <span class="feature-badge">📖 30+类问答</span>
                <span class="feature-badge">📅 校历查询</span>
                <span class="feature-badge">📊 绩点计算</span>
                <span class="feature-badge">💬 多轮对话</span>
            </div>
    """, unsafe_allow_html=True)

    with st.container():
        with st.form("login_form"):
            saved_id = st.session_state.get("saved_student_id", "")
            saved_pwd = st.session_state.get("saved_password", "")
            
            student_id = st.text_input("学号", placeholder="请输入你的学号", value=saved_id)
            password = st.text_input("密码", placeholder="请输入密码", type="password", value=saved_pwd)
            
            st.markdown('<div class="checkbox-vertical">', unsafe_allow_html=True)
            remember_id = st.checkbox("记住学号", value=bool(saved_id))
            remember_pwd = st.checkbox("记住密码", value=bool(saved_pwd))
            st.markdown('</div>', unsafe_allow_html=True)
            
            col_center1, col_center2, col_center3 = st.columns([1, 2, 1])
            with col_center2:
                submitted = st.form_submit_button("登 录", use_container_width=True)

            if submitted:
                if student_id and password:
                    if remember_id:
                        st.session_state.saved_student_id = student_id
                    else:
                        st.session_state.saved_student_id = ""
                    
                    if remember_pwd:
                        st.session_state.saved_password = password
                    else:
                        st.session_state.saved_password = ""
                    
                    st.session_state.logged_in = True
                    st.session_state.student_id = student_id
                    st.rerun()
                else:
                    st.markdown('<div class="login-error">⚠️ 请完整填写学号和密码</div>', unsafe_allow_html=True)

    st.markdown("""
        </div>
    </div>
    <div class="login-footer">✦ 校园小智 · 安徽交通职业技术学院 ✦</div>
    """, unsafe_allow_html=True)
    st.stop()


# ============================================================
# 主界面（已登录）
# ============================================================
st.set_page_config(
    page_title="校园小智",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 移除导航文字 - 保留侧边栏
# ============================================================
st.components.v1.html("""
<script>
(function() {
    function removeNavTexts() {
        // 1. 移除所有包含 "app" 和 "category" 的文本节点
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
        
        // 2. 移除包含这些文字的父元素（如果父元素只有这些文字）
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
        
        // 3. 移除面包屑导航（但保留侧边栏）
        var allDivs = document.querySelectorAll('div');
        for (var d = 0; d < allDivs.length; d++) {
            var div = allDivs[d];
            if (div.textContent && div.textContent.includes('/') && 
                div.textContent.includes('app')) {
                div.remove();
            }
        }
    }
    
    // 立即执行
    removeNavTexts();
    // 多次延迟执行确保动态加载完成
    setTimeout(removeNavTexts, 100);
    setTimeout(removeNavTexts, 300);
    setTimeout(removeNavTexts, 500);
    setTimeout(removeNavTexts, 1000);
    
    // 监听页面变化
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
    /* 只隐藏面包屑导航，不隐藏侧边栏 */
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
    
    /* 保留侧边栏 */
    section[data-testid="stSidebar"] {
        display: flex !important;
        visibility: visible !important;
        height: auto !important;
        width: auto !important;
        overflow: visible !important;
        position: relative !important;
        top: auto !important;
        left: auto !important;
        opacity: 1 !important;
        pointer-events: auto !important;
    }
</style>
""", height=0)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(160deg, #eef0f5 0%, #e2e6ef 50%, #d5dce8 100%);
    }
    
    /* ===== 侧边栏样式 - 深蓝色渐变 ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1a33 0%, #1a3a6b 45%, #1e4d8a 100%) !important;
        border-right: 1px solid rgba(255, 215, 0, 0.08);
    }
    
    section[data-testid="stSidebar"] * {
        color: rgba(255, 255, 255, 0.85) !important;
    }
    
    .sidebar-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #FFD700 !important;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: 2px;
        text-transform: uppercase;
        opacity: 0.85;
    }
    .sidebar-title .icon {
        font-size: 1rem;
    }
    .sidebar-sub {
        color: rgba(255, 255, 255, 0.3) !important;
        font-size: 0.7rem;
        margin-bottom: 14px;
        letter-spacing: 1.5px;
    }
    .current-category-card {
        background: rgba(255, 215, 0, 0.06);
        border: 1px solid rgba(255, 215, 0, 0.08);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .current-category-card .label {
        font-size: 0.7rem;
        color: rgba(255, 255, 255, 0.4);
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .current-category-card .value {
        font-size: 0.9rem;
        color: #FFD700;
        font-weight: 600;
        letter-spacing: 1px;
    }
    .current-category-card .value.all {
        color: rgba(255, 255, 255, 0.5);
        font-weight: 400;
    }
    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        padding: 10px 12px;
        text-align: center;
    }
    .stat-card .number {
        font-size: 1.4rem;
        font-weight: 700;
        color: #FFD700;
        line-height: 1.2;
    }
    .stat-card .desc {
        font-size: 0.6rem;
        color: rgba(255, 255, 255, 0.4);
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 2px;
    }
    section[data-testid="stSidebar"] .stButton button {
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        background: rgba(255, 255, 255, 0.04) !important;
        color: rgba(255, 255, 255, 0.8) !important;
        padding: 8px 12px !important;
        font-size: 12px !important;
        backdrop-filter: blur(5px);
        box-shadow: none !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255, 215, 0, 0.08) !important;
        border-color: rgba(255, 215, 0, 0.15) !important;
        color: #FFD700 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
    }
    section[data-testid="stSidebar"] hr {
        margin: 14px 0 !important;
        border-color: rgba(255, 255, 255, 0.04) !important;
    }
    .sidebar-footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.06) !important;
        font-size: 10px;
        letter-spacing: 3px;
        margin-top: 6px;
        padding-top: 12px;
        border-top: 1px solid rgba(255, 255, 255, 0.02);
    }
    .reset-btn .stButton button {
        background: rgba(100, 180, 255, 0.04) !important;
        border-color: rgba(100, 180, 255, 0.06) !important;
        color: rgba(100, 180, 255, 0.5) !important;
    }
    .reset-btn .stButton button:hover {
        background: rgba(100, 180, 255, 0.08) !important;
        color: #64b4ff !important;
    }
    .clear-btn .stButton button {
        background: rgba(255, 80, 80, 0.04) !important;
        border-color: rgba(255, 80, 80, 0.06) !important;
        color: rgba(255, 150, 150, 0.5) !important;
    }
    .clear-btn .stButton button:hover {
        background: rgba(255, 80, 80, 0.08) !important;
        color: #ff6b6b !important;
    }
    .logout-btn .stButton button {
        background: rgba(255, 80, 80, 0.04) !important;
        border-color: rgba(255, 80, 80, 0.06) !important;
        color: rgba(255, 150, 150, 0.4) !important;
    }
    .logout-btn .stButton button:hover {
        background: rgba(255, 80, 80, 0.08) !important;
        color: #ff6b6b !important;
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
    .category-hint {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.04), rgba(255, 215, 0, 0.01));
        border-left: 3px solid #FFD700;
        padding: 12px 18px;
        border-radius: 12px;
        margin-bottom: 18px;
        font-size: 14px;
        color: #1a2a4a;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 215, 0, 0.06);
    }
    .category-hint strong {
        color: #1a3a6b;
    }
    .user-info {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.5);
        text-align: right;
        margin-top: -10px;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }
    ::-webkit-scrollbar {
        width: 4px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.02);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(26, 58, 107, 0.15);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(26, 58, 107, 0.25);
    }

    .main-header {
        text-align: center;
        padding: 2.2rem 0 1.8rem 0;
        background: linear-gradient(135deg, #0b1a33 0%, #1a3a6b 45%, #1e4d8a 100%);
        border-radius: 18px;
        color: white;
        margin-bottom: 1.8rem;
        box-shadow: 0 12px 40px rgba(10, 30, 70, 0.35);
        border: 1px solid rgba(255, 215, 0, 0.08);
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: -60%;
        right: -20%;
        width: 60%;
        height: 200%;
        background: radial-gradient(ellipse, rgba(255, 215, 0, 0.04) 0%, transparent 70%);
        pointer-events: none;
    }
    .main-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, #FFD700, #FFD700, transparent);
        opacity: 0.3;
    }
    .main-header h1 {
        font-size: 2.8rem;
        margin: 0;
        font-weight: 700;
        letter-spacing: 4px;
        position: relative;
    }
    .main-header h1 .gold {
        color: #FFD700;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.15);
    }
    .main-header .sub {
        font-size: 1rem;
        opacity: 0.6;
        margin: 8px 0 0 0;
        letter-spacing: 8px;
        font-weight: 300;
        position: relative;
    }
    .main-header .badge-row {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-top: 14px;
        flex-wrap: wrap;
        position: relative;
    }
    .main-header .badge-item {
        background: rgba(255, 215, 0, 0.06);
        border: 1px solid rgba(255, 215, 0, 0.08);
        padding: 4px 18px;
        border-radius: 30px;
        font-size: 0.75rem;
        color: rgba(255, 215, 0, 0.6);
        letter-spacing: 1px;
    }

    .func-card {
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 14px;
        padding: 14px 18px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 2px 12px rgba(0,0,0,0.02);
        margin-bottom: 12px;
        height: 100%;
    }
    .func-card .func-title {
        font-size: 0.7rem;
        color: #5a6a8a;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .func-card .func-content {
        font-size: 0.9rem;
        color: #1a2a4a;
    }
    .func-card .stButton button {
        padding: 4px 16px !important;
        font-size: 0.75rem !important;
        border-radius: 20px !important;
        background: linear-gradient(135deg, #1a3a6b, #2a5a9a) !important;
        color: white !important;
        border: none !important;
    }
    .func-card .stTextInput input {
        padding: 4px 12px !important;
        font-size: 0.85rem !important;
        border-radius: 20px !important;
    }
    .func-row {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 14px;
        margin-bottom: 14px;
    }
    @media (max-width: 768px) {
        .func-row {
            grid-template-columns: 1fr;
        }
    }

    .calendar-table {
        width: 100%;
        font-size: 0.75rem;
        border-collapse: collapse;
    }
    .calendar-table th {
        background: linear-gradient(135deg, #1a3a6b, #2a5a9a);
        color: white;
        padding: 5px 6px;
        text-align: center;
        font-weight: 500;
        letter-spacing: 1px;
    }
    .calendar-table td {
        padding: 4px 6px;
        text-align: center;
        border-bottom: 1px solid rgba(0,0,0,0.04);
    }
    .calendar-table tr:nth-child(even) {
        background: rgba(255,255,255,0.3);
    }
    .calendar-table .current-week {
        background: rgba(255, 215, 0, 0.12) !important;
        border-left: 3px solid #FFD700;
        font-weight: 600;
    }
    .calendar-table .current-week td {
        color: #1a3a6b;
    }
    .week-status {
        text-align: center;
        margin-top: 8px;
        font-size: 0.9rem;
        font-weight: 500;
        color: #1a3a6b;
        padding: 6px;
        background: rgba(255, 215, 0, 0.06);
        border-radius: 10px;
        border: 1px solid rgba(255, 215, 0, 0.06);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎓 校园<span class="gold">小智</span></h1>
    <div class="sub">✦ 你的校园生活助手 · 随时为你解答 ✦</div>
    <div class="badge-row">
        <span class="badge-item">✦ 30+ 类校园问题</span>
        <span class="badge-item">✦ 智能问答</span>
        <span class="badge-item">✦ 多轮对话</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="user-info">👤 欢迎，{st.session_state.student_id}</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "show_history" not in st.session_state:
    st.session_state.show_history = False
if "gpa_result" not in st.session_state:
    st.session_state.gpa_result = ""

# ============================================================
# 工具函数
# ============================================================
def get_calendar_data():
    calendar_data = {
        "周次": list(range(1, 21)),
        "日期": [
            "3/2-3/8", "3/9-3/15", "3/16-3/22", "3/23-3/29", "3/30-4/5",
            "4/6-4/12", "4/13-4/19", "4/20-4/26", "4/27-5/3", "5/4-5/10",
            "5/11-5/17", "5/18-5/24", "5/25-5/31", "6/1-6/7", "6/8-6/14",
            "6/15-6/21", "6/22-6/28", "6/29-7/5", "7/6-7/12", "7/13-7/17"
        ],
        "事项": [
            "开学报到", "正式上课", "", "", "清明节",
            "", "", "", "期中教学检查", "期中教学检查",
            "", "", "", "", "",
            "端午节", "", "", "期末教学检查", "期末考试"
        ]
    }
    return calendar_data

def get_current_week_info():
    today = datetime.now()
    semester_start = datetime(2026, 3, 2)
    summer_start = datetime(2026, 7, 18)
    days_diff = (today - semester_start).days
    
    if days_diff < 0:
        return {"week": 0, "status": "未开始", "msg": "🎓 2026年春季学期尚未开始，3月2日开学报到"}
    if today >= summer_start:
        return {"week": 0, "status": "暑假", "msg": "🌞 已进入暑假（7月18日-8月31日），新学期再会！"}
    week_num = days_diff // 7 + 1
    if week_num > 20:
        return {"week": 20, "status": "已结束", "msg": "📅 本学期已结束（共20周）"}
    return {"week": week_num, "status": f"第{week_num}周", "msg": f"📅 当前是2025-2026学年第二学期第 {week_num} 周"}

def calc_gpa(scores_str):
    try:
        scores = [float(x.strip()) for x in scores_str.split(',') if x.strip()]
        total = 0
        for s in scores:
            if s >= 90:
                total += 4.0
            elif s >= 80:
                total += 3.0
            elif s >= 70:
                total += 2.0
            elif s >= 60:
                total += 1.0
            else:
                total += 0
        gpa = total / len(scores)
        return f"✅ 您的平均绩点是：{gpa:.2f}"
    except:
        return "❌ 格式错误，请用逗号分隔，如：85,90,78"

# ============================================================
# 顶部功能栏
# ============================================================
st.markdown('<div class="func-row">', unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <div class="func-card">
        <div class="func-title">📅 校历查询</div>
        <div class="func-content">
    """, unsafe_allow_html=True)
    
    cal_data = get_calendar_data()
    current_week_info = get_current_week_info()
    current_week = current_week_info["week"]
    
    df_cal = pd.DataFrame({
        "周次": cal_data["周次"],
        "日期": cal_data["日期"],
        "事项": cal_data["事项"]
    })
    
    def highlight_current_week(row):
        if row.name + 1 == current_week and current_week > 0:
            return ['background-color: rgba(255, 215, 0, 0.15); font-weight: bold; color: #1a3a6b;'] * len(row)
        return [''] * len(row)
    
    styled_df = df_cal.style.apply(highlight_current_week, axis=1)
    styled_df = styled_df.set_properties(**{
        'text-align': 'center',
        'font-size': '12px',
        'padding': '4px 6px'
    })
    styled_df = styled_df.set_table_styles([
        {'selector': 'thead tr th', 'props': [
            ('background', 'linear-gradient(135deg, #1a3a6b, #2a5a9a)'),
            ('color', 'white'),
            ('font-size', '12px'),
            ('padding', '6px 8px'),
            ('text-align', 'center'),
            ('font-weight', '500'),
            ('letter-spacing', '1px')
        ]},
        {'selector': 'tbody tr:nth-child(even)', 'props': [
            ('background', 'rgba(255,255,255,0.3)')
        ]},
        {'selector': '', 'props': [
            ('border-collapse', 'collapse'),
            ('width', '100%'),
            ('font-size', '12px')
        ]}
    ])
    
    st.dataframe(styled_df, use_container_width=True, height=350)
    status_msg = current_week_info["msg"]
    st.markdown(f'<div class="week-status">{status_msg}</div>', unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <div class="func-card">
        <div class="func-title">📊 绩点计算</div>
        <div class="func-content">
    """, unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns([3, 1])
    with col_g1:
        gpa_input = st.text_input("", placeholder="输入成绩，如：85,90,78", key="gpa_input_widget", label_visibility="collapsed")
    with col_g2:
        if st.button("计算", key="gpa_calc_btn"):
            if gpa_input:
                st.session_state.gpa_result = calc_gpa(gpa_input)
            else:
                st.session_state.gpa_result = "⚠️ 请先输入成绩"
    
    if st.session_state.gpa_result:
        st.markdown(f"<p style='font-size:0.9rem;color:#1a3a6b;font-weight:500;'>{st.session_state.gpa_result}</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='font-size:0.75rem;color:#8a9bb5;'>输入各科成绩，用逗号分隔</p>", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <div class="func-card">
        <div class="func-title">💬 历史对话</div>
        <div class="func-content">
    """, unsafe_allow_html=True)
    
    if st.button("📖 查看历史对话", key="show_history_btn", use_container_width=True):
        st.session_state.show_history = not st.session_state.show_history
    
    if st.session_state.show_history:
        history = get_history()
        if history:
            st.markdown(f"<p style='font-size:0.75rem;color:#5a6a8a;'>共 {len(history)} 条记录</p>", unsafe_allow_html=True)
            for msg in history[-10:]:
                role_icon = "👤" if msg["role"] == "user" else "🤖"
                content = msg['content']
                if len(content) > 60:
                    content = content[:60] + "..."
                st.markdown(f"<p style='font-size:0.75rem;margin:2px 0;color:#3a4a6a;'>{role_icon} {content}</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='font-size:0.8rem;color:#8a9bb5;'>暂无对话记录</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='font-size:0.75rem;color:#8a9bb5;'>点击按钮查看历史对话</p>", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# 侧边栏
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title"><span class="icon">📊</span> 智能助手</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="number">30+</div>
            <div class="desc">问题类别</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="number">160</div>
            <div class="desc">知识条目</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    current_cat = get_category()
    if current_cat:
        st.markdown(f"""
        <div class="current-category-card">
            <span class="label">📌 当前类别</span>
            <span class="value">{current_cat}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="current-category-card">
            <span class="label">📌 当前类别</span>
            <span class="value all">全部（未限制）</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    if st.button("🔄 取消限制", use_container_width=True):
        set_category(None)
        st.session_state.selected_category = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="sidebar-title"><span class="icon">📋</span> 选择类别</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">点击后，跳转到该类别的详情页面</div>', unsafe_allow_html=True)

    categories = {
        "📝 请假": "请假", "💰 奖学金": "奖学金", "🔧 报修": "报修", "💳 一卡通": "一卡通",
        "📚 选课": "选课", "🌐 校园网络": "校园网络", "📦 快递服务": "快递服务", "📖 图书馆": "图书馆",
        "🏥 校医院": "校医院", "💊 医疗报销": "医疗报销", "🛡️ 校园安全": "校园安全", "🎭 社团活动": "社团活动",
        "🏠 宿舍管理": "宿舍管理", "🍽️ 食堂就餐": "食堂就餐", "🏟️ 体育场馆": "体育场馆",
        "🧠 心理咨询": "心理咨询", "💼 就业指导": "就业指导", "🪪 学生证": "学生证",
        "📁 档案管理": "档案管理", "📊 成绩查询": "成绩查询", "🔄 转专业": "转专业",
        "📖 辅修": "辅修", "🎓 考研": "考研", "🌍 出国交换": "出国交换",
        "💼 实习实训": "实习实训", "📝 毕业答辩": "毕业答辩", "🎓 学位授予": "学位授予",
        "💰 学费缴纳": "学费缴纳", "🏦 助学贷款": "助学贷款", "💪 勤工助学": "勤工助学",
        "🤝 困难补助": "困难补助", "🎖️ 征兵入伍": "征兵入伍", "🤗 志愿服务": "志愿服务",
        "🌱 社会实践": "社会实践"
    }

    cols = st.columns(2)
    for i, (label, category) in enumerate(categories.items()):
        col = cols[i % 2]
        if col.button(label, use_container_width=True, key=f"cat_{i}"):
            st.session_state.detail_category = category
            st.session_state.selected_question = None
            st.session_state.qa_history = []
            st.switch_page("pages/category_detail.py")

    st.divider()

    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.messages = []
        st.session_state.selected_category = None
        st.session_state.show_history = False
        clear_history()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("🚪 退出登录", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.student_id = ""
        st.session_state.messages = []
        st.session_state.selected_category = None
        clear_history()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-footer">✦ 校园小智 ✦</div>', unsafe_allow_html=True)

# ============================================================
# 聊天界面
# ============================================================
with st.container():
    if st.session_state.selected_category:
        st.markdown(f"""
        <div class="category-hint">
            📌 当前类别：<strong>{st.session_state.selected_category}</strong>
            ｜请在下方输入具体问题
        </div>
        """, unsafe_allow_html=True)

    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div style="text-align:center;padding:30px 20px;flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;">
            <div style="font-size:2.5rem;margin-bottom:4px;">🎓</div>
            <div style="font-size:1rem;font-weight:600;color:#1a2a4a;">开始提问吧</div>
            <div style="font-size:0.8rem;color:#7a8aaa;margin-top:2px;">左侧选择类别，下方输入问题</div>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("💬 输入你的校园问题...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("✦ 思考中..."):
                response = agent_chat(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        st.rerun()