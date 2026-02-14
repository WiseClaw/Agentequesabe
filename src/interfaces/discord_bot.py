
import os
import discord
from dotenv import load_dotenv

load_dotenv("/a0/usr/workdir/.env")
TOKEN = os.getenv("DISCORD_TOKEN")

class WiseClawClient(discord.Client):
    async def on_ready(self):
        print(f'[DISCORD] Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('WiseClaw is active.')

if __name__ == '__main__':
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in .env")
        exit(1)

    intents = discord.Intents.default()
    intents.message_content = True

    client = WiseClawClient(intents=intents)
    client.run(TOKEN)
