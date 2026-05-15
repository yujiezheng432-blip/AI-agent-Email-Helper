"""
邮件同步：从外部邮箱拉取并写入本地 SQLite。
处理流程（Agent）统一从数据库读取 status='raw' 的邮件。
"""

from database.email_repository import save_raw_email
from services.mail163_service import read_163_emails
from services.outlook_mail_service import fetch_recent_emails


def sync_from_163(limit: int = 30) -> int:
    emails = read_163_emails(limit=limit)
    for email_data in emails:
        save_raw_email(email_data)
    return len(emails)


def sync_from_outlook(limit: int = 30) -> int:
    emails = fetch_recent_emails(limit=limit)
    for email_data in emails:
        save_raw_email(email_data)
    return len(emails)
