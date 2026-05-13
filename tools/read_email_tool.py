# tools/read_email_tool.py

from services.outlook_mail_service import fetch_recent_emails


def read_recent_emails(limit=10):
    """
    Tool: 读取最近 Outlook 邮件。
    """

    return fetch_recent_emails(limit=limit)