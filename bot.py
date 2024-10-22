import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Load Cogs (the modular features)
initial_extensions = [
    'cogs.live_notifications',
    'cogs.moderation',
    'cogs.mini_games',
    'cogs.role_management',
    'cogs.contest',
    'cogs.logging'
]

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

# Environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot.run(DISCORD_TOKEN)
