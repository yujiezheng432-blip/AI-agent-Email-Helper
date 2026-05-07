# tools/save_result_tool.py

def save_result(email, summary, analysis, draft_reply):
    """
    保存处理结果。
    目前先打印，后面再存入 SQLite。
    """

    result = {
        "message_id": email["message_id"],
        "sender": email["sender"],
        "subject": email["subject"],
        "summary": summary,
        "category": analysis["category"],
        "importance_score": analysis["importance_score"],
        "need_reply": analysis["need_reply"],
        "draft_reply": draft_reply
    }

    print("=" * 60)
    print("邮件处理结果：")
    print(result)
    print("=" * 60)

    return result