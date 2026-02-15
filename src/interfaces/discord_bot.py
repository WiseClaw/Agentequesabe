import discord
import os
from discord.ext import commands
from src.agents.manager import ManagerAgent
from src.agents.coder import CoderAgent
from src.agents.researcher import ResearcherAgent
from src.memory.context_manager import ContextManager
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

# Instanciar Agentes (Eles já carregam o ContextManager e Librarian internamente)
agents = {
    "manager": ManagerAgent(),
    "coder": CoderAgent(),
    "researcher": ResearcherAgent()
}
ctx_mgr = ContextManager()

@bot.event
async def on_ready():
    print(f'WiseClaw HQ Online: {bot.user}')
    ctx_mgr.log_decision("Discord HQ synchronized with Neural Memory.")

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    
    # Mapeamento de canais para agentes
    channel_name = str(message.channel.name)
    agent = agents.get("manager") # Default
    if "dev" in channel_name or "code" in channel_name: agent = agents.get("coder")
    elif "investigacao" in channel_name: agent = agents.get("researcher")

    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel) or agent != agents.get("manager"):
        async with message.channel.typing():
            # O process() do agente agora cuida da Memória, Contexto e Fluxo B
            response = agent.process(message.content)
            await message.reply(response)

bot.run(TOKEN)
