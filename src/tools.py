from datetime import datetime

def get_current_week():
    """获取当前是第几周（校历），假设9月1日是第1周"""
    today = datetime.now()
    start = datetime(2025, 9, 1)
    week_num = (today - start).days // 7 + 1
    
    # 如果还没开学，显示第1周
    if week_num < 1:
        week_num = 1
    # 如果超过20周，显示已结束
    if week_num > 20:
        return "本学年校历已结束，请关注新学期安排"
    
    return f"现在是第{week_num}周"

def calculate_gpa(scores_str):
    """计算绩点，输入格式：'85,90,78'"""
    try:
        scores = [int(x.strip()) for x in scores_str.split(',')]
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
        return f"您的平均绩点是：{gpa:.2f}"
    except Exception as e:
        return f"❌ 输入格式错误，请用逗号分隔分数，例如：85,90,78"