from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("🔍 开始测试检索功能...")

# 加载向量库
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh")
vector_db = Chroma(persist_directory='./vector_db', embedding_function=embeddings)

def search_knowledge(query):
    """检索知识库，返回最相关的3条结果"""
    results = vector_db.similarity_search(query, k=3)
    print(f"\n🔍 搜索: {query}")
    print("-" * 50)
    for i, r in enumerate(results, 1):
        print(f"📌 结果 {i}: {r.metadata}")
        print(f"📄 内容: {r.page_content}\n")
    return results

# 测试十个不同类别的问题
if __name__ == "__main__":
    search_knowledge("我发烧了怎么办？")           # 请假类
    search_knowledge("奖学金要多少绩点？")         # 奖学金类
    search_knowledge("宿舍灯坏了找谁？")           # 报修类
    search_knowledge("一卡通丢了怎么办？")         # 一卡通类
    search_knowledge("选错了课能退吗？")           # 选课类
    search_knowledge("校园网怎么连接？")           # 校园网络类
    search_knowledge("快递到哪里取？")             # 快递服务类
    search_knowledge("图书馆开放时间是什么？")     # 图书馆类
    search_knowledge("校外看病能报销吗？")         # 医疗报销类
    search_knowledge("校园报警电话是多少？")       # 校园安全类