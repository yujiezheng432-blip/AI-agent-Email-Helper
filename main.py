
# main.py

from tools.read_email_tool import read_recent_emails
from tools.summarize_email_tool import summarize_email
from tools.classify_email_tool import classify_email
from tools.generate_reply_tool import generate_reply
from tools.save_result_tool import save_result


def run_agent():
    """
    邮件助手 Agent 主流程。
    """

    emails = read_recent_emails(limit=5)

    for email in emails:
        summary = summarize_email(email)

        analysis = classify_email(email)

        draft_reply = ""

        if analysis["need_reply"]:
            draft_reply = generate_reply(email)

        save_result(email, summary, analysis, draft_reply)


if __name__ == "__main__":
    run_agent()