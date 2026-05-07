# tools/summarize_email_tool.py

def summarize_email(email):
    """
    根据邮件内容生成简单摘要。
    目前先不用 LLM，用规则模拟。
    """

    subject = email["subject"]
    body = email["body"]

    if "interview" in subject.lower() or "interview" in body.lower():
        return "这封邮件是关于面试邀请。"

    if "sale" in subject.lower() or "discount" in body.lower():
        return "这封邮件是广告促销信息。"

    return "这是一封普通邮件。"