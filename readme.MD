### Email alert automation using telegram bot

The following libaries are required to run the script:

```
pip install imaplib2 python-telegram-bot requests
```

Replace the following settings with your own:

```
# Email credentials and settings
EMAIL_USER = 'your-email@mail.ru'
EMAIL_PASS = 'your-email-password'
IMAP_SERVER = 'imap.mail.ru'

# Telegram Bot settings
TELEGRAM_BOT_TOKEN = 'your-telegram-bot-token'
TELEGRAM_CHAT_ID = 'your-telegram-chat-id'
# Topic ID if it's a super group
TELEGRAM_THREAD_ID = 'your-telegram-thread-id'
```