import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("🚀 开始构建向量库...")

# 加载CSV数据
df = pd.read_csv('data/campus_data.csv')
print(f"📂 已加载 {len(df)} 条数据")

# 使用免费本地嵌入模型
print("📥 正在加载嵌入模型...")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh")

# 准备文本和元数据
texts = df['answer'].tolist()
metadatas = df[['id', 'category', 'question']].to_dict('records')

print(f"📝 准备向量化 {len(texts)} 条记录...")

# 创建向量库并持久化（新版本语法）
vector_db = Chroma.from_texts(
    texts=texts,
    embedding=embeddings,
    metadatas=metadatas,  # 注意这里是 metadatas（复数）
    persist_directory='./vector_db'
)

print(f"✅ 已存入 {len(texts)} 条记录到向量库！")
print("📁 向量库保存在 ./vector_db 目录")