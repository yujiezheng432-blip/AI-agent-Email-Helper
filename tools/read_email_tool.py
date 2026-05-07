# tools/read_email_tool.py

def read_recent_emails(limit=5):
    """
    模拟读取最近邮件。
    当前阶段先不接入 Outlook，
    使用假数据练习 Agent 工作流。
    """

    emails = [
        {
            "message_id": "email_001",
            "sender": "hr@company.com",
            "subject": "面试邀请",
            "body": "你好 Yujie，我们想邀请你参加下周一的面试。",
            "receiving_time": "2026-05-07 10:00"
        },
        {
            "message_id": "email_002",
            "sender": "shop@example.com",
            "subject": "今日促销活动",
            "body": "今天所有商品限时折扣，立即购买！",
            "receiving_time": "2026-05-07 11:00"
        }
    ]

    return emails[:limit]