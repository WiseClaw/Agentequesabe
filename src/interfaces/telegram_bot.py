
import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from src.agents.manager import ManagerAgent
    from src.agents.researcher import ResearcherAgent
    from src.agents.coder import CoderAgent
    from src.agents.critic import CriticAgent
    from src.agents.operator import OperatorAgent
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    sys.exit(1)

load_dotenv("/a0/usr/workdir/.env")
TOKEN = os.getenv("TELEGRAM_TOKEN")

agents = {
    'manager': ManagerAgent(),
    'researcher': ResearcherAgent(),
    'coder': CoderAgent(),
    'auditor': CriticAgent(),
    'operator': OperatorAgent()
}

async def handle_agent_task(update: Update, agent_key: str, task: str):
    agent = agents.get(agent_key)
    if not agent:
        await update.message.reply_text("❌ Agent not found.")
        return

    # Send typing action
    await update.message.chat.send_action(action="typing")

    try:
        response = await asyncio.to_thread(agent.process, task)
        if len(response) > 4000:
            for i in range(0, len(response), 4000):
                await update.message.reply_text(response[i:i+4000])
        else:
            await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"[SYSTEM ERROR] {str(e)}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 **WiseClaw** Online. Send me a message to talk to the Manager, or use /r, /c, /a, /o.")

async def handle_plain_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Default to Manager
    await handle_agent_task(update, 'manager', update.message.text)

async def cmd_manager(update, context): await handle_agent_task(update, 'manager', " ".join(context.args))
async def cmd_researcher(update, context): await handle_agent_task(update, 'researcher', " ".join(context.args))
async def cmd_coder(update, context): await handle_agent_task(update, 'coder', " ".join(context.args))
async def cmd_auditor(update, context): await handle_agent_task(update, 'auditor', " ".join(context.args))
async def cmd_operator(update, context): await handle_agent_task(update, 'operator', " ".join(context.args))

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('m', cmd_manager))
    application.add_handler(CommandHandler('r', cmd_researcher))
    application.add_handler(CommandHandler('c', cmd_coder))
    application.add_handler(CommandHandler('a', cmd_auditor))
    application.add_handler(CommandHandler('o', cmd_operator))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_plain_text))

    print("[TELEGRAM] Bot is polling...")
    application.run_polling()
