import sys
import asyncio
import discord
import os
from dotenv import load_dotenv
from achievement_manager import AchievementManager

async def update_discord():
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        manager = AchievementManager()
        blocks = manager.get_message_blocks()

        for guild in client.guilds:
            channel = discord.utils.get(guild.text_channels, name="achievements")
            if channel:
                # Limpar e reenviar para manter ordem e integridade
                async for message in channel.history(limit=50):
                    if message.author == client.user:
                        await message.delete()
                for block in blocks:
                    await channel.send(block)
        await client.close()
    await client.start(token)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(1)

    phase = sys.argv[1]
    item = sys.argv[2]

    manager = AchievementManager()
    manager.add_achievement(phase, item)

    asyncio.run(update_discord())
