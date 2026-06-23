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

def rag_answer(question):
    """RAG问答函数：检索 + 生成"""
    docs = vector_db.similarity_search(question, k=5)
    context = "\n\n".join([d.page_content for d in docs])
    prompt = RAG_PROMPT.format(context=context, question=question)
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ 调用大模型失败：{e}"