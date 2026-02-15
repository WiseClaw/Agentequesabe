import os
import asyncio
from telebot.async_telebot import AsyncTeleBot
from src.agents.manager import ManagerAgent
from src.memory.context_manager import ContextManager
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = AsyncTeleBot(TOKEN)
manager = ManagerAgent()
ctx_mgr = ContextManager()

@bot.message_handler(func=lambda message: True)
async def handle_all_messages(message):
    # Sincronização Bilateral: Cada mensagem no Telegram alimenta a memória global
    await bot.send_chat_action(message.chat.id, 'typing')
    
    # O ManagerAgent processa usando o Cérebro Híbrido e Memória ChromaDB
    response = manager.process(message.text)
    
    ctx_mgr.update_state("active_platform", "Telegram")
    await bot.reply_to(message, response)

async def main():
    print("WiseClaw Telegram Terminal (Neural Sync) Online...")
    await bot.polling()

if __name__ == '__main__':
    asyncio.run(main())

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    bot.reply_to(message, "🎙️ Mensagem de voz recebida. A processar via Sovereign STT Engine...")
    # Lógica de processamento futura integrada aqui