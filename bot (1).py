import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ===== НАЛАШТУВАННЯ =====
BOT_TOKEN = "8804155447:AAFVYcqseEaxW8I6E254mt3L1YuxbNwvfPg"
NOTIFY_CHAT_ID = 489251506
KEYWORDS = ["tickets.ua", "тикетс.юа", "тікетс.юа"]
# ========================

logging.basicConfig(level=logging.INFO)

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.channel_post
    if not message or not message.text:
        return

    text_lower = message.text.lower()
    found = [kw for kw in KEYWORDS if kw in text_lower]

    if not found:
        return

    chat = message.chat
    sender = message.from_user

    chat_title = chat.title or "Приватний чат"
    sender_name = "Невідомий"
    sender_username = ""
    if sender:
        sender_name = f"{sender.first_name or ''} {sender.last_name or ''}".strip()
        sender_username = f" (@{sender.username})" if sender.username else ""

    alert = (
        f"🔔 *Згадали tickets.ua\\!*\n\n"
        f"📍 Чат: *{chat_title}*\n"
        f"👤 Від: {sender_name}{sender_username}\n"
        f"💬 Текст:\n`{message.text}`"
    )

    await context.bot.send_message(
        chat_id=NOTIFY_CHAT_ID,
        text=alert,
        parse_mode="MarkdownV2"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))
    print("✅ Бот запущено!")
    app.run_polling()
