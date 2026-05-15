import imaplib
import email
from email.header import decode_header

from config.settings import get_mail163_credentials

# 允许 imaplib 使用 ID 命令
imaplib.Commands["ID"] = ("AUTH", "SELECTED")

IMAP_SERVER = "imap.163.com"


def decode_text(text):
    """
    解码邮件标题和发件人信息
    """
    if text is None:
        return ""

    decoded_parts = decode_header(text)
    result = ""

    for content, charset in decoded_parts:
        if isinstance(content, bytes):
            result += content.decode(charset or "utf-8", errors="ignore")
        else:
            result += content

    return result


def send_imap_id(mail):
    """
    向 163 邮箱服务器发送 IMAP ID。
    163 有时会把 Python imaplib 识别为不安全客户端，
    发送 ID 可以提高通过概率。
    """
    print("🪪 正在发送 IMAP ID 客户端信息...")

    try:
        status, data = mail._simple_command(
            "ID",
            '("name" "EmailAIAgent" "version" "1.0" "vendor" "Python" "support-email" "your_email@163.com")'
        )

        print("🪪 IMAP ID 状态:", status)
        print("🪪 IMAP ID 返回:", data)

    except Exception as e:
        print("⚠️ IMAP ID 发送失败，但继续尝试读取邮箱")
        print("错误信息:", e)


def read_163_emails(limit=5):
    """
    读取 163 邮箱最近邮件。
    需在环境变量或 .env 中配置 MAIL163_ACCOUNT、MAIL163_AUTH_CODE。
    """

    email_account, auth_code = get_mail163_credentials()
    if not email_account or not auth_code:
        raise RuntimeError(
            "未配置 163 邮箱：请设置环境变量 MAIL163_ACCOUNT 与 MAIL163_AUTH_CODE（或写入 .env）"
        )

    print("=" * 60)
    print("📨 开始读取 163 邮箱邮件")
    print("=" * 60)

    mail = None

    try:
        print("🔗 正在连接 IMAP 服务器...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        print("✅ IMAP 服务器连接成功")

        print("🔐 正在登录邮箱...")
        mail.login(email_account, auth_code)
        print("✅ 邮箱登录成功")

        send_imap_id(mail)

        print("📂 正在获取邮箱目录...")
        status, folders = mail.list()

        print("📂 list 状态:", status)
        print("📂 邮箱目录如下：")

        if folders:
            for folder in folders:
                print(folder)

        print("📂 正在进入收件箱 INBOX...")
        status, select_data = mail.select("INBOX", readonly=True)

        print("📂 select 状态:", status)
        print("📂 select 返回信息:", select_data)

        if status != "OK":
            raise Exception(f"无法进入 INBOX，服务器返回: {select_data}")

        print("✅ 已进入收件箱")

        print("🔍 正在搜索所有邮件...")
        status, data = mail.search(None, "ALL")

        print("🔍 search 状态:", status)
        print("🔍 search 返回:", data)

        if status != "OK":
            raise Exception(f"搜索邮件失败，服务器返回: {data}")

        email_ids = data[0].split()

        print(f"📧 共发现 {len(email_ids)} 封邮件")

        recent_ids = email_ids[-limit:]
        print(f"📥 准备读取最近 {len(recent_ids)} 封邮件")

        emails = []

        for index, email_id in enumerate(reversed(recent_ids), start=1):
            print("-" * 60)
            print(f"📨 正在读取第 {index} 封邮件，邮件ID: {email_id.decode()}")

            status, msg_data = mail.fetch(email_id, "(RFC822)")

            print("📥 fetch 状态:", status)

            if status != "OK":
                print("⚠️ 当前邮件读取失败，跳过")
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = decode_text(msg.get("Subject"))
            sender = decode_text(msg.get("From"))

            print("📌 邮件标题:", subject)
            print("👤 发件人:", sender)

            body = ""

            if msg.is_multipart():
                print("📦 检测到 multipart 邮件")

                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    print("📄 当前内容类型:", content_type)

                    if "attachment" in content_disposition:
                        continue

                    if content_type == "text/plain":
                        payload = part.get_payload(decode=True)

                        if payload:
                            body = payload.decode(
                                part.get_content_charset() or "utf-8",
                                errors="ignore"
                            )
                            print("✅ 成功读取 text/plain 正文")
                            break

                    elif content_type == "text/html" and not body:
                        payload = part.get_payload(decode=True)

                        if payload:
                            body = payload.decode(
                                part.get_content_charset() or "utf-8",
                                errors="ignore"
                            )
                            print("✅ 成功读取 text/html 正文")
            else:
                print("📄 普通单部分邮件")

                payload = msg.get_payload(decode=True)

                if payload:
                    body = payload.decode(
                        msg.get_content_charset() or "utf-8",
                        errors="ignore"
                    )
                    print("✅ 成功读取正文")

            emails.append({
                "message_id": email_id.decode(),
                "sender": sender,
                "subject": subject,
                "body": body
            })

            print("💾 邮件已加入结果列表")

        print("=" * 60)
        print(f"🎉 邮件读取完成，共读取 {len(emails)} 封邮件")
        print("=" * 60)

        return emails

    except Exception as e:
        print("=" * 60)
        print("❌ 邮件读取失败")
        print("错误信息:", e)
        print("=" * 60)

        return []

    finally:
        if mail is not None:
            try:
                print("🚪 正在退出邮箱登录...")
                mail.logout()
                print("✅ 已退出邮箱")
            except Exception:
                pass


if __name__ == "__main__":
    emails = read_163_emails(limit=5)

    print("\n")
    print("=" * 60)
    print("📋 最终邮件结果")
    print("=" * 60)

    for email_data in emails:
        print("📌 标题:", email_data["subject"])
        print("👤 发件人:", email_data["sender"])
        print("📝 正文预览:")
        print(email_data["body"][:300])
        print("-" * 60)