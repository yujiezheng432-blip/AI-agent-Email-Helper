# services/outlook_mail_service.py

import requests
from bs4 import BeautifulSoup

from services.outlook_auth_service import get_access_token


GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"


def clean_html(html_content):
    """
    将 Outlook 返回的 HTML 正文转换成普通文本。
    """
    if not html_content:
        return ""

    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator="\n").strip()


def fetch_recent_emails(limit=10):
    """
    从 Outlook 收件箱读取最近邮件。
    """

    access_token = get_access_token()

    url = f"{GRAPH_BASE_URL}/me/mailFolders/inbox/messages"

    params = {
        "$top": limit,
        "$orderby": "receivedDateTime desc",
        "$select": "id,subject,from,receivedDateTime,bodyPreview,body"
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise RuntimeError(f"读取 Outlook 邮件失败: {response.status_code}, {response.text}")

    data = response.json()

    emails = []

    for item in data.get("value", []):
        sender_info = item.get("from", {}).get("emailAddress", {})

        body_html = item.get("body", {}).get("content", "")
        body_text = clean_html(body_html)

        emails.append({
            "message_id": item.get("id"),
            "sender_name": sender_info.get("name"),
            "sender_email": sender_info.get("address"),
            "subject": item.get("subject"),
            "received_time": item.get("receivedDateTime"),
            "body_preview": item.get("bodyPreview"),
            "body": body_text
        })

    return emails