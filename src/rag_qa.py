import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from prompt_templates import RAG_PROMPT

load_dotenv()

print("🤖 初始化RAG问答系统...")

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh")
vector_db = Chroma(persist_directory='./vector_db', embedding_function=embeddings)

def rag_answer(question, history=None, category=None):
    """
    RAG问答函数：检索 + 生成，支持对话历史和类别过滤
    
    参数:
        question: 用户问题
        history: 对话历史列表，格式为 [{"role": "user/assistant", "content": "..."}]
        category: 可选，指定类别后只检索该类别的内容
    """
    # 1. 检索相关文档
    if category:
        # 按类别过滤检索
        results = vector_db.similarity_search(question, k=5, filter={"category": category})
    else:
        # 检索所有类别
        results = vector_db.similarity_search(question, k=5)
    
    docs = results
    context = "\n\n".join([d.page_content for d in docs])
    
    # 2. 构建对话历史文本
    history_text = ""
    if history:
        recent = history[-4:]  # 只取最近4轮
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent])
        history_text = f"【对话历史】\n{history_text}\n\n"
    
    # 3. 构建提示词
    full_prompt = f"""{history_text}【校园规则】
{context}

【当前问题】
{question}

【回答要求】
1. 如果用户告诉过你名字等信息，请记住并使用
2. 只根据上面的规则回答
3. 如果规则里没有相关信息，请用亲切友好的语气回复，示例：
   "亲爱的同学，这个问题暂时不在当前类别的资料中哦～建议你点击左侧对应的分类按钮，或直接联系辅导员获取准确信息～"
4. 回答要简洁、友好，语气像学长学姐一样亲切

【回答】
"""
    
    # 4. 调用大模型生成回答
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ 调用大模型失败：{e}"