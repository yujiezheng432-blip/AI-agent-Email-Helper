import os

from dotenv import load_dotenv

load_dotenv()


def get_mail163_credentials():
    """返回 (账号, 授权码)。未配置时为空字符串。"""
    account = os.getenv("MAIL163_ACCOUNT", "").strip()
    auth_code = os.getenv("MAIL163_AUTH_CODE", "").strip()
    return account, auth_code
