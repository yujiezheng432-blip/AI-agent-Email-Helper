# tools/read_email_tool.py

from database.email_repository import get_unprocessed_emails, row_to_agent_email


def read_recent_emails(limit=10):
    """
    Tool: 从本地数据库读取待处理邮件（status='raw'）。
    邮件需先通过同步命令写入库（163 或 Outlook）。
    """

    rows = get_unprocessed_emails(limit=limit)
    return [row_to_agent_email(row) for row in rows]