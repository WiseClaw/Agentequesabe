# -*- coding: utf-8 -*-
import discord
import os
from dotenv import load_dotenv
from achievement_manager import AchievementManager

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    try:
        print(f'Logged in as {client.user}')
        manager = AchievementManager()
        blocks = manager.get_message_blocks()

        for guild in client.guilds:
            channel = discord.utils.get(guild.text_channels, name="achievements")
            if not channel:
                channel = await guild.create_text_channel("achievements")

            # Limpar mensagens anteriores do bot
            async for message in channel.history(limit=100):
                if message.author == client.user:
                    await message.delete()

            # Enviar blocos
            for block in blocks:
                await channel.send(block)

            print(f"Achievements updated in {guild.name}!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.close()

if __name__ == '__main__':
    client.run(TOKEN)
