import os
import discord
from dotenv import load_dotenv
import sys
import asyncio

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

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

load_dotenv("/a0/usr/workdir/.env")
TOKEN = os.getenv("DISCORD_TOKEN")

# Initialize Agents
agents = {
    'gestao': ManagerAgent(),
    'investigacao': ResearcherAgent(),
    'dev-lab': CoderAgent(),
    'auditoria': CriticAgent(),
    'operacoes': OperatorAgent()
}

# Channel Mapping (Channel Name -> Agent Key)
CHANNEL_MAP = {
    'gestao': 'gestao',
    'investigacao': 'investigacao',
    'dev-lab': 'dev-lab',
    'auditoria': 'auditoria',
    'operacoes': 'operacoes'
}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Factory Online: {client.user}')
    print(f'Active Agents: {list(agents.keys())}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check if message is in a mapped channel
    channel_name = message.channel.name
    agent_key = CHANNEL_MAP.get(channel_name)

    if agent_key:
        agent = agents[agent_key]
        print(f"[ROUTER] Message in #{channel_name} -> Routing to {agent.name}")

        async with message.channel.typing():
            try:
                # Run agent in thread to not block event loop
                response = await asyncio.to_thread(agent.process, message.content)

                # Split long messages (Discord limit 2000 chars)
                if len(response) > 2000:
                    for i in range(0, len(response), 1900):
                        await message.channel.send(response[i:i+1900])
                else:
                    await message.channel.send(response)
            except Exception as e:
                await message.channel.send(f"[SYSTEM ERROR] {str(e)}")

client.run(TOKEN)
