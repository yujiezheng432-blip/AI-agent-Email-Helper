# tools/save_result_tool.py

from database.email_repository import update_email_after_processing


def save_result(email, summary, analysis, draft_reply):
    """
    将 Agent 处理结果写回 SQLite，并把邮件标记为已处理。
    """

    result = {
        "id": email.get("id"),
        "message_id": email["message_id"],
        "sender": email["sender"],
        "subject": email["subject"],
        "summary": summary,
        "category": analysis["category"],
        "importance_score": analysis["importance_score"],
        "need_reply": analysis["need_reply"],
        "draft_reply": draft_reply,
    }

    if email.get("id") is not None:
        update_email_after_processing(
            email["id"],
            summary,
            analysis["category"],
            analysis["need_reply"],
            analysis["importance_score"],
            draft_reply,
        )

    print("=" * 60)
    print("邮件处理结果：")
    print(result)
    print("=" * 60)

    return result