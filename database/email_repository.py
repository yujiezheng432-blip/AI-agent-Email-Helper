from database.db import get_connection


def save_raw_email(email_data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO emails (
        message_id, sender, subject, body
    ) VALUES (?, ?, ?, ?)
    """, (
        email_data["message_id"],
        email_data["sender"],
        email_data["subject"],
        email_data["body"]
    ))

    conn.commit()
    conn.close()


def get_unprocessed_emails():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, message_id, sender, subject, body
    FROM emails
    WHERE status = 'raw'
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows