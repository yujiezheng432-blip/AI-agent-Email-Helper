# tools/email_listener_163.py
# 轮询：周期性从 163 同步到数据库，再运行 Agent 处理未处理邮件。

import time

from dotenv import load_dotenv

from agents.email_agent import EmailAgent
from database.db import init_db
from services.sync_service import sync_from_163


def start_163_email_listener(interval=60, sync_limit=20, process_limit=10):
    """
    每隔 interval 秒执行一次：同步 163 -> 本地库 -> 处理 status=raw 的邮件。
    """
    load_dotenv()
    init_db()

    print("163 邮箱轮询已启动（同步 + 处理）...")

    while True:
        try:
            n = sync_from_163(limit=sync_limit)
            print(f"本轮同步拉取 {n} 封。")
            EmailAgent(email_limit=process_limit).run()
        except Exception as e:
            print("本轮执行异常:", e)

        time.sleep(interval)


if __name__ == "__main__":
    start_163_email_listener()
