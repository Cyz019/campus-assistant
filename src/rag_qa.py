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
    
    # 2. 构建提示词
    prompt = RAG_PROMPT.format(context=context, question=question)
    
    # 3. 构建消息列表（包含历史对话）
    messages = []
    
    # 如果有历史对话，加入上下文（最多保留最近4轮）
    if history:
        for msg in history[-4:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
    
    # 添加当前问题
    messages.append({"role": "user", "content": prompt})
    
    # 4. 调用大模型生成回答
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ 调用大模型失败：{e}"