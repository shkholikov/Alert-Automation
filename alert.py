import imaplib
import email
from email.header import decode_header
import time
import requests
import logging


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email credentials and settings
EMAIL_USER = 'your-email@mail.ru'
EMAIL_PASS = 'your-email-password'
IMAP_SERVER = 'imap.mail.ru'

# Telegram Bot settings
TELEGRAM_BOT_TOKEN = 'your-telegram-bot-token'
TELEGRAM_CHAT_ID = 'your-telegram-chat-id'
# Topic ID if it's a super group
TELEGRAM_THREAD_ID = 'your-telegram-thread-id'


def connect_to_email():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")
    return mail


def fetch_unread_emails(mail):
    # Change '(UNSEEN)' to 'ALL' to fetch all emails
    status, messages = mail.search(None, '(UNSEEN)')
    email_ids = messages[0].split()
    return email_ids


def send_to_telegram(subject, body):
    message = f"Subject: {subject}\n\n{body}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }
    # If it's a supergroup
    # data = {
    #     "chat_id": TELEGRAM_CHAT_ID,
    #     "text": message,
    #     "message_thread_id": TELEGRAM_THREAD_ID
    # }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        logger.info(f"Message sent successfully: {subject}")
    else:
        logger.error(f"Failed to send message: {
                     response.status_code} - {response.text}")


def process_email(mail, email_id):
    status, msg_data = mail.fetch(email_id, '(RFC822)')
    msg = email.message_from_bytes(msg_data[0][1])

    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else "utf-8")

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = msg.get_payload(decode=True).decode()

    send_to_telegram(subject, body)
    # mail.store(email_id, '+FLAGS', '\\Seen')


def main():
    while True:
        mail = connect_to_email()
        email_ids = fetch_unread_emails(mail)
        print(email_ids)
        for email_id in email_ids:
            process_email(mail, email_id)
        mail.logout()
        # runs every 60 seconds
        time.sleep(60)


if __name__ == "__main__":
    main()
