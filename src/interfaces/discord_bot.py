import os
import discord
from dotenv import load_dotenv
import sys

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

load_dotenv("/a0/usr/workdir/.env")
TOKEN = os.getenv("DISCORD_TOKEN")

class WiseClawClient(discord.Client):
    async def on_ready(self):
        print(f'[DISCORD] Logged on as {self.user}!', flush=True)

    async def on_message(self, message):
        if message.author == self.user:
            return

        content = message.content.lower()
        print(f"[DEBUG] Received: {content}", flush=True)

        if content.startswith('$hello'):
            await message.channel.send('WiseClaw is active.')
        
        elif 'olá' in content or 'ola' in content:
            await message.channel.send('Olá! O sistema WiseClaw está online e a escutar.')
            
        elif 'ajuda' in content or 'help' in content:
            await message.channel.send('Comandos disponíveis: $hello, olá')

if __name__ == '__main__':
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in .env")
        exit(1)

    intents = discord.Intents.default()
    intents.message_content = True

    client = WiseClawClient(intents=intents)
    client.run(TOKEN)
