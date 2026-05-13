# agents/email_agent.py

from tools.read_email_tool import read_recent_emails
from tools.summarize_email_tool import summarize_email
from tools.classify_email_tool import classify_email
from tools.generate_reply_tool import generate_reply
from tools.save_result_tool import save_result


class EmailAgent:
    """
    邮件助手 Agent。
    负责调度各个工具，完成完整邮件处理流程。
    """

    def __init__(self, email_limit=5):
        self.email_limit = email_limit

    def process_single_email(self, email):
        """
        处理单封邮件。
        """

        summary = summarize_email(email)
        analysis = classify_email(email)

        draft_reply = ""

        if analysis["need_reply"]:
            draft_reply = generate_reply(email)

        save_result(email, summary, analysis, draft_reply)

        return {
            "email": email,
            "summary": summary,
            "analysis": analysis,
            "draft_reply": draft_reply
        }

    def run(self):
        """
        执行 Agent 主流程。
        """

        emails = read_recent_emails(limit=self.email_limit)

        results = []

        for email in emails:
            result = self.process_single_email(email)
            results.append(result)

        return results