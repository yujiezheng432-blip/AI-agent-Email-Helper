# tools/generate_reply_tool.py

def generate_reply(email):
    """
    根据邮件内容生成回复草稿。
    目前先用模板模拟。
    """

    subject = email["subject"].lower()
    body = email["body"].lower()

    if "interview" in subject or "interview" in body:
        return (
            "Dear Sir or Madam,\n\n"
            "Thank you for your email and the interview invitation. "
            "I would be happy to attend the interview next Monday.\n\n"
            "Best regards,\n"
            "Yujie"
        )

    return ""