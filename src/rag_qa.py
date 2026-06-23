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

def rag_answer(question, history=None):
    """RAG问答函数：检索 + 生成，支持对话历史"""
    # 1. 检索相关文档
    docs = vector_db.similarity_search(question, k=5)
    context = "\n\n".join([d.page_content for d in docs])
    
    # 2. 构建对话历史文本
    history_text = ""
    if history:
        # 只取最近4轮对话
        recent = history[-4:]
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent])
        history_text = f"【对话历史】\n{history_text}\n\n"
    
    # 3. 构建提示词（把历史拼进去）
    full_prompt = f"""{history_text}【校园规则】
{context}

【当前问题】
{question}

【回答要求】
1. 如果用户在对话历史中告诉过你他的名字或其他信息，请记住并使用
2. 只根据上面的规则回答校园问题
3. 如果规则里没有相关信息，说"我不确定，建议咨询辅导员"
4. 回答要简洁、友好

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