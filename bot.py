import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8804155447:AAFVYcqseEaxW8I6E254mt3L1YuxbNwvfPg"
NOTIFY_CHAT_ID = 489251506
KEYWORDS = ["tickets.ua", "тикетс.юа", "тікетс.юа"]

logging.basicConfig(level=logging.INFO)

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.channel_post
    if not message or not message.text:
        return

    text_lower = message.text.lower()
    if not any(kw in text_lower for kw in KEYWORDS):
        return

    chat = message.chat
    sender = message.from_user
    chat_title = chat.title or "Приватний чат"
    sender_name = "Невідомий"
    if sender:
        sender_name = f"{sender.first_name or ''} {sender.last_name or ''}".strip()
        if sender.username:
            sender_name += f" (@{sender.username})"

    alert = (
        f"🔔 Згадали tickets.ua!\n\n"
        f"📍 Чат: {chat_title}\n"
        f"👤 Від: {sender_name}\n"
        f"💬 Текст: {message.text}"
    )

    await context.bot.send_message(chat_id=NOTIFY_CHAT_ID, text=alert)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))
    print("Bot started!")
    async with app:
        await app.start()
        await app.updater.start_polling(drop_pending_updates=True)
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
