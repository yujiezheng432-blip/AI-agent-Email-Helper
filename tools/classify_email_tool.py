# tools/classify_email_tool.py

def classify_email(email):
    """
    判断邮件类别、重要程度、是否需要回复。
    """

    subject = email["subject"].lower()
    body = email["body"].lower()

    if "interview" in subject or "interview" in body:
        return {
            "category": "求职 / 面试",
            "importance_score": 9,
            "need_reply": True
        }

    if "sale" in subject or "discount" in body:
        return {
            "category": "广告 / 推广",
            "importance_score": 2,
            "need_reply": False
        }

    return {
        "category": "其他",
        "importance_score": 5,
        "need_reply": False
    }