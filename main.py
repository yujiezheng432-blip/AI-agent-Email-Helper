"""
邮件 AI 助手 — 统一入口

目录职责（简要）：
- config/          环境变量与 .env（账号、密钥勿提交仓库）
- database/      SQLite 表结构与读写
- services/      对外系统：163 IMAP、Outlook Graph、同步、可选监听
- tools/         Agent 可调用的原子能力（读库、摘要、分类等）
- agents/        编排 tools 的流程
- llm/           大模型调用（摘要/回复等后续可接入）

常用命令（在项目根目录执行）：
  python main.py sync 163 --limit 30    # 从 163 拉邮件写入数据库
  python main.py sync outlook --limit 20
  python main.py process --limit 10     # 处理库中未处理邮件
  python main.py run 163                # 先同步 163 再处理
"""

import argparse
import sys

from dotenv import load_dotenv

from agents.email_agent import EmailAgent
from database.db import init_db
from services.sync_service import sync_from_163, sync_from_outlook


def cmd_sync(args) -> int:
    if args.source == "163":
        n = sync_from_163(limit=args.limit)
    else:
        n = sync_from_outlook(limit=args.limit)
    print(f"同步完成，写入或跳过重复后本轮拉取 {n} 封。")
    return 0


def cmd_process(args) -> int:
    agent = EmailAgent(email_limit=args.limit)
    agent.run()
    return 0


def cmd_run(args) -> int:
    if args.source == "163":
        sync_from_163(limit=args.sync_limit)
    else:
        sync_from_outlook(limit=args.sync_limit)
    agent = EmailAgent(email_limit=args.limit)
    agent.run()
    return 0


def main() -> int:
    load_dotenv()
    init_db()

    parser = argparse.ArgumentParser(description="邮件 AI 助手")
    sub = parser.add_subparsers(dest="command", required=True)

    p_sync = sub.add_parser("sync", help="从邮箱同步到本地数据库")
    p_sync.add_argument(
        "source",
        choices=["163", "outlook"],
        help="邮箱来源",
    )
    p_sync.add_argument("--limit", type=int, default=30, help="最多拉取封数")
    p_sync.set_defaults(func=cmd_sync)

    p_process = sub.add_parser("process", help="处理数据库中未处理邮件")
    p_process.add_argument("--limit", type=int, default=10, help="本轮最多处理封数")
    p_process.set_defaults(func=cmd_process)

    p_run = sub.add_parser("run", help="先同步再处理")
    p_run.add_argument(
        "source",
        choices=["163", "outlook"],
        help="先同步哪个邮箱",
    )
    p_run.add_argument("--sync-limit", type=int, default=30, help="同步时最多拉取封数")
    p_run.add_argument("--limit", type=int, default=10, help="处理时最多处理封数")
    p_run.set_defaults(func=cmd_run)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
