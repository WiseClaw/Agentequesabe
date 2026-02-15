
import os
import discord
from dotenv import load_dotenv
import sys
import asyncio

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

sys.stdout.reconfigure(line_buffering=True)
load_dotenv("/a0/usr/workdir/.env")
TOKEN = os.getenv("DISCORD_TOKEN")

agents = {
    'gestao': ManagerAgent(),
    'investigacao': ResearcherAgent(),
    'dev-lab': CoderAgent(),
    'auditoria': CriticAgent(),
    'operacoes': OperatorAgent()
}

CHANNEL_MAP = {
    'gestao': 'gestao',
    'investigacao': 'investigacao',
    'dev-lab': 'dev-lab',
    'auditoria': 'auditoria',
    'operacoes': 'operacoes',
    'geral': 'gestao'
}

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Factory Online: {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f"[MSG] #{message.channel.name}: {message.content}")

    # Routing Logic: Factory Channels -> Specialized Agents | Others -> Manager
    if message.channel.name in CHANNEL_MAP:
        agent_key = CHANNEL_MAP[message.channel.name]
    else:
        agent_key = 'gestao'

    if agent_key:
        agent = agents[agent_key]
        async with message.channel.typing():
            try:
                response = await asyncio.to_thread(agent.process, message.content)
                if len(response) > 2000:
                    for i in range(0, len(response), 1900):
                        await message.channel.send(response[i:i+1900])
                else:
                    await message.channel.send(response)
            except Exception as e:
                await message.channel.send(f"[SYSTEM ERROR] {str(e)}")


if __name__ == '__main__':
    if not TOKEN:
        print('[ERROR] DISCORD_TOKEN not found in .env')
    else:
        client.run(TOKEN)