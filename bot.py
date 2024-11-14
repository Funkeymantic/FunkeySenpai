from discord.ext import commands
from twitchio.ext import commands as twitch_commands
from dotenv import load_dotenv
import discord
import os
import schedule
import subprocess
from datetime import datetime
import sys
import time
import asyncio
import threading
import logging
import openai
import random

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
twitch_token = os.getenv("TWITCH_OAUTH_TOKEN")
twitch_channel = os.getenv("TWITCH_CHANNEL")
openai.api_key = os.getenv("OPEN_API_KEY")

# Initialize the Discord bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="~", intents=intents)

# Twitch Bot Class
class TwitchBot(twitch_commands.Bot):
    def __init__(self):
        super().__init__(token=twitch_token, prefix="!", initial_channels=[twitch_channel])

    @twitch_commands.command(name="roll")
    async def roll(self, ctx, dice: str):
        """Rolls a dice. Use formats like d6, d20, d100."""
        try:
            sides = int(dice[1:])
            if sides in [2, 4, 6, 8, 10, 20, 100]:
                result = random.randint(1, sides)
                await ctx.send(f"{ctx.author.name} rolled a {dice}: {result}")
            else:
                await ctx.send("Invalid dice type! Use one of: d2, d4, d6, d8, d10, d20, d100.")
        except ValueError:
            await ctx.send("Invalid format! Please use the format like d20, d6, etc.")

# Instantiate the Twitch bot
twitch_bot = TwitchBot()

# Load Discord bot extensions
initial_extensions = [
    'cogs.server_config',
    'cogs.schedule',
    'cogs.socials',
    'cogs.gear',
    'cogs.loyalty',
    'cogs.logging',
    'cogs.polls',
    'cogs.greetings',
    'cogs.quotes',
    'cogs.moderation',
    'cogs.alerts',
    'cogs.todo',
    'cogs.Discord_Commands'
]

async def load_extensions():
    """Load all the initial extensions."""
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            logging.info(f'Loaded extension: {extension}')
        except Exception as e:
            logging.error(f'Failed to load extension {extension}: {e}')

# Error handler for Discord bot
@bot.event
async def on_command_error(ctx, error):
    """Handles errors globally and sends a DM to the specified user with the error details."""
    user = await bot.fetch_user(223688811845124096)
    error_message = f"An error occurred in the bot:\n{str(error)}"
    logging.error(error_message)
    
    if user:
        await user.send(error_message)
    await ctx.send("An error occurred. The bot owner has been notified.")
    raise error

# Example command using OpenAI API for Discord
@bot.command()
async def ai_chat(ctx, *, message):
    response = openai.Completion.create(
        engine="davinci",
        prompt=message,
        max_tokens=150
    )
    await ctx.send(response.choices[0].text.strip())

# Git pull and restart function
def pull_and_restart():
    current_time = datetime.now().strftime("%H:%M")
    if current_time == "10:35":  # Example scheduled restart time
        logging.info("Initiating Git pull and restart process.")
        try:
            result = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True)
            logging.info(f'Git pull output: {result.stdout}')
            subprocess.run([sys.executable, *sys.argv], shell=True)
            sys.exit()
        except Exception as e:
            logging.error(f"Error during restart: {e}")

# Schedule to check every minute
schedule.every().minute.do(pull_and_restart)
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)
threading.Thread(target=run_schedule, daemon=True).start()

# Setup hook to start Twitch bot
@bot.event
async def setup_hook():
    # Start Twitch bot in the background
    bot.loop.create_task(twitch_bot.start())

# Main function to start both Discord and Twitch bots
async def main():
    await load_extensions()
    await bot.start(discord_token)

# Run the main function
asyncio.run(main())
