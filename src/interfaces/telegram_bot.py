
import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

load_dotenv("/a0/usr/workdir/.env")
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="WiseClaw is online and listening.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Received: {update.message.text}")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN not found in .env")
        exit(1)

    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    print("[TELEGRAM] Bot is polling...")
    application.run_polling()
