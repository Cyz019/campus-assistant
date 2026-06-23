import re
from tools import get_current_week, calculate_gpa
from rag_qa import rag_answer

# 对话记忆
conversation_history = []

def agent_chat(user_input):
    """智能体主函数：识别用户意图，调用对应工具或RAG问答"""
    conversation_history.append({"role": "user", "content": user_input})
    
    # ---- 意图识别 ----
    
    # 1. 校历查询
    if "周" in user_input and ("几" in user_input or "校历" in user_input):
        response = get_current_week()
    
    # 2. 绩点计算（必须有2个以上的数字）
    elif ("绩点" in user_input or "GPA" in user_input or "gpa" in user_input):
        scores = re.findall(r'\d+', user_input)
        if len(scores) >= 2:
            response = calculate_gpa(', '.join(scores))
        else:
            response = rag_answer(user_input, conversation_history)
    
    # 3. 打招呼
    elif user_input in ["你好", "您好", "hi", "hello", "在吗"]:
        response = "你好！我是校园生活百事通助手，可以帮你解答校园问题、查询校历、计算绩点。请问有什么可以帮你的？"
    
    # 4. 帮助指令
    elif user_input in ["帮助", "help", "功能"]:
        response = """📋 我能帮你做这些事：
1. 回答校园问题（请假、奖学金、报修等）
2. 查询当前校历周数（输入：现在第几周）
3. 计算绩点（输入：绩点计算 85,90,78）
4. 闲聊对话
试试问我一个问题吧！"""
    
    # 5. 默认走RAG问答（传入历史）
    else:
        response = rag_answer(user_input, conversation_history)
    
    conversation_history.append({"role": "assistant", "content": response})
    return response

def get_history():
    return conversation_history

def clear_history():
    conversation_history.clear()
    return "对话历史已清空"