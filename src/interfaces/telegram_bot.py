import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import sys

# Add project root to path
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

# Initialize Agents
agents = {
    'manager': ManagerAgent(),
    'researcher': ResearcherAgent(),
    'coder': CoderAgent(),
    'auditor': CriticAgent(),
    'operator': OperatorAgent()
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **WiseClaw Mobile Interface** Online\n\n"
        "Available Commands:\n"
        "/m [task] - Manager (Claude 3.5)\n"
        "/r [task] - Researcher (Gemini 3 Pro)\n"
        "/c [task] - Coder (Claude 3.5)\n"
        "/a [task] - Auditor (GPT-4o)\n"
        "/o [task] - Operator (Claude 3.5)\n"
    )

async def handle_agent_command(update: Update, context: ContextTypes.DEFAULT_TYPE, agent_key: str):
    user_task = " ".join(context.args)
    if not user_task:
        await update.message.reply_text(f"⚠️ Please provide a task for the {agent_key}.")
        return

    agent = agents.get(agent_key)
    if not agent:
        await update.message.reply_text("❌ Agent not found.")
        return

    await update.message.reply_text(f"⏳ **{agent.name}** is thinking... ({agent.role})")

    try:
        # Run agent in thread
        response = await asyncio.to_thread(agent.process, user_task)

        # Split long messages (Telegram limit 4096 chars)
        if len(response) > 4000:
            for i in range(0, len(response), 4000):
                await update.message.reply_text(response[i:i+4000])
        else:
            await update.message.reply_text(response)

    except Exception as e:
        await update.message.reply_text(f"[SYSTEM ERROR] {str(e)}")

# Command Wrappers
async def cmd_manager(update, context): await handle_agent_command(update, context, 'manager')
async def cmd_researcher(update, context): await handle_agent_command(update, context, 'researcher')
async def cmd_coder(update, context): await handle_agent_command(update, context, 'coder')
async def cmd_auditor(update, context): await handle_agent_command(update, context, 'auditor')
async def cmd_operator(update, context): await handle_agent_command(update, context, 'operator')

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN not found in .env")
        exit(1)

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('m', cmd_manager))
    application.add_handler(CommandHandler('r', cmd_researcher))
    application.add_handler(CommandHandler('c', cmd_coder))
    application.add_handler(CommandHandler('a', cmd_auditor))
    application.add_handler(CommandHandler('o', cmd_operator))

    print("[TELEGRAM] Bot is polling with Hybrid Brain...")
    application.run_polling()
