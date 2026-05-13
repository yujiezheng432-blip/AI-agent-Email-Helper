from services.mail163_service import read_163_emails
from database.db import init_db
from database.email_repository import save_raw_email


def main():
    init_db()

    emails = read_163_emails(limit=5)

    for email_data in emails:
        save_raw_email(email_data)
        print("已保存邮件:", email_data["subject"])


if __name__ == "__main__":
    main()