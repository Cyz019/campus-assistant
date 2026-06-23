from datetime import datetime

def get_current_week():
    """
    获取当前是第几周
    根据2025-2026学年第二学期校历：
    - 2026年3月2日开始上课（第1周）
    - 2026年7月18日开始暑假
    """
    today = datetime.now()
    
    # 校历开始日期：2026年3月2日（第1周周一）
    semester_start = datetime(2026, 3, 2)
    
    # 暑假开始日期：2026年7月18日
    summer_start = datetime(2026, 7, 18)
    
    # 计算当前是第几周（从3月2日开始算）
    days_diff = (today - semester_start).days
    
    # 还没开学
    if days_diff < 0:
        return "🎓 2026年春季学期尚未开始，3月2日开学报到"
    
    # 放暑假了
    if today >= summer_start:
        return "🌞 已进入暑假（7月18日-8月31日），新学期再会！"
    
    # 计算周数（第1周从3月2日开始）
    week_num = days_diff // 7 + 1
    
    # 校历共20周（3月2日 ~ 7月17日）
    if week_num > 20:
        return f"📅 本学期已结束（共20周），请关注下学期安排"
    
    # 根据不同周数显示不同信息
    extra_info = ""
    if week_num <= 2:
        extra_info = "（期初教学检查）"
    elif 9 <= week_num <= 10:
        extra_info = "（期中教学检查）"
    elif week_num >= 19:
        extra_info = "（期末教学检查、期末考试）"
    
    return f"📅 当前是2025-2026学年第二学期第 {week_num} 周 {extra_info}"

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