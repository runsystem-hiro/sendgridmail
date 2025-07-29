import csv
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_NAME = os.getenv("FROM_NAME")

CSV_FILE = "recipients.csv"
TEMPLATE_FILE = "mail_template.txt"
SENT_LOG_FILE = "sent_log.csv"
ERROR_LOG_FILE = "error_log.csv"


def load_sent_emails():
    try:
        with open(SENT_LOG_FILE, newline="", encoding="utf-8") as f:
            return set(row["email"] for row in csv.DictReader(f))
    except FileNotFoundError:
        return set()


def append_log(filename, row):
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "status", "message"])
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(row)


def build_full_name(first, last):
    if first and last:
        return f"{last} {first} 様"
    elif last:
        return f"{last} 様"
    elif first:
        return f"{first} 様"
    else:
        return "お客様"


def main():
    if not SENDGRID_API_KEY or not FROM_EMAIL or not FROM_NAME:
        raise RuntimeError("❌ .envファイルの設定に不備があります")

    with open(TEMPLATE_FILE, encoding="utf-8") as f:
        lines = f.read().splitlines()

    if len(lines) < 3 or lines[1].strip() != "":
        raise ValueError(
            "❌ mail_template.txt は『1行目：件名』『2行目：空行』『3行目以降：本文』形式である必要があります")

    subject = lines[0].strip()
    body_template = "\n".join(lines[2:]).strip()

    sent_emails = load_sent_emails()

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        recipients = [row for row in reader if row.get(
            "email") and row["email"] not in sent_emails]

    for i, r in enumerate(recipients, start=1):
        email = r["email"]
        first = r.get("first_name", "").strip()
        last = r.get("last_name", "").strip()
        company = r.get("company", "").strip()
        full_name = build_full_name(first, last)

        body = body_template.format(
            first_name=first,
            last_name=last,
            company=company,
            full_name=full_name
        )

        payload = {
            "personalizations": [{
                "to": [{"email": email, "name": full_name}],
                "subject": subject
            }],
            "from": {"email": FROM_EMAIL, "name": FROM_NAME},
            "content": [{
                "type": "text/plain",
                "value": body
            }]
        }

        try:
            response = requests.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={
                    "Authorization": f"Bearer {SENDGRID_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            if 200 <= response.status_code < 300:
                print(f"✅ [{i}] Sent to {email}")
                append_log(SENT_LOG_FILE, {
                    "email": email, "status": "sent", "message": "OK"
                })
            else:
                print(f"✘ [{i}] Failed to {email}: {response.status_code}")
                append_log(ERROR_LOG_FILE, {
                    "email": email, "status": "fail", "message": response.text
                })
        except Exception as e:
            print(f"✘ [{i}] Exception for {email}: {e}")
            append_log(ERROR_LOG_FILE, {
                "email": email, "status": "exception", "message": str(e)
            })

        time.sleep(1.2)  # Essentials プラン負荷対策


if __name__ == "__main__":
    main()
