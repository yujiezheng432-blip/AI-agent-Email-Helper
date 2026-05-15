from database.db import get_connection


def _normalize_incoming_email(email_data):
    """统一 163 / Outlook 等来源的字段，便于入库与后续 Agent 使用。"""
    message_id = (email_data.get("message_id") or "").strip()
    subject = email_data.get("subject") or ""
    body = email_data.get("body") or ""

    sender = email_data.get("sender")
    if sender is None:
        name = (email_data.get("sender_name") or "").strip()
        addr = (email_data.get("sender_email") or "").strip()
        if addr:
            sender = f"{name} <{addr}>" if name else addr
        else:
            sender = name or ""

    return {
        "message_id": message_id,
        "sender": sender,
        "subject": subject,
        "body": body,
    }


def save_raw_email(email_data):
    row = _normalize_incoming_email(email_data)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO emails (
        message_id, sender, subject, body
    ) VALUES (?, ?, ?, ?)
    """, (
        row["message_id"],
        row["sender"],
        row["subject"],
        row["body"],
    ))

    conn.commit()
    conn.close()


def get_unprocessed_emails(limit=100):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, message_id, sender, subject, body
    FROM emails
    WHERE status = 'raw'
    ORDER BY id ASC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows


def row_to_agent_email(row):
    """数据库行 -> Agent 使用的统一邮件字典（含数据库主键 id）。"""
    return {
        "id": row[0],
        "message_id": row[1],
        "sender": row[2] or "",
        "subject": row[3] or "",
        "body": row[4] or "",
    }


def update_email_after_processing(
    email_db_id,
    summary,
    category,
    need_reply,
    importance_score,
    draft_reply,
    status="processed",
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE emails SET
        summary = ?,
        category = ?,
        need_reply = ?,
        importance_score = ?,
        draft_reply = ?,
        status = ?
    WHERE id = ?
    """, (
        summary,
        category,
        1 if need_reply else 0,
        importance_score,
        draft_reply or "",
        status,
        email_db_id,
    ))

    conn.commit()
    conn.close()