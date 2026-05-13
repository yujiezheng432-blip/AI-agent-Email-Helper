# main.py

from tools.read_email_tool import read_recent_emails


def main():
    emails = read_recent_emails(limit=5)

    for email in emails:
        print("邮件ID:", email["message_id"])
        print("发件人:", email["sender_name"], email["sender_email"])
        print("标题:", email["subject"])
        print("时间:", email["received_time"])
        print("预览:", email["body_preview"])
        print("-" * 80)


if __name__ == "__main__":
    main()
