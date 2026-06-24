import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ===== НАЛАШТУВАННЯ =====
BOT_TOKEN = "8804155447:AAFVYcqseEaxW8I6E254mt3L1YuxbNwvfPg"
NOTIFY_CHAT_ID = 489251506  # Твій особистий chat_id
KEYWORDS = ["tickets.ua", "тикетс.юа", "тікетс.юа"]
# ========================

logging.basicConfig(level=logging.INFO)

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.channel_post
    if not message or not message.text:
        return

    text_lower = message.text.lower()
    found = [kw for kw in KEYWORDS if kw in text_lower]

    if found:
        chat = message.chat
        sender = message.from_user

        chat_title = chat.title or "Приватний чат"
        chat_link = f"https://t.me/c/{str(chat.id).replace('-100', '')}/{message.message_id}"

        sender_name = "Невідомий"
        sender_username = ""
        if sender:
            sender_name = f"{sender.first_name or ''} {sender.last_name or ''}".strip()
            sender_username = f" (@{sender.username})" if sender.username else ""

        alert = (
            f"🔔 *Згадали tickets.ua!*\n\n"
            f"📍 Чат: *{chat_title}*\n"
            f"👤 Від: {sender_name}{sender_username}\n"
            f"💬 Текст:\n_{message.text}_\n\n"
            f"🔗 [Перейти до повідомлення]({chat_link})"
        )

        await context.bot.send_message(
            chat_id=NOTIFY_CHAT_ID,
            text=alert,
            parse_mode="Markdown"
        )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))

print("✅ Бот запущено! Моніторинг активний.")
app.run_polling()
