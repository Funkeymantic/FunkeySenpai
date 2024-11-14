from discord.ext import commands
import discord
from dotenv import load_dotenv
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

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()  # Load environment variables from .env

discord_token = os.getenv("DISCORD_TOKEN")
if not discord_token:
    raise ValueError("DISCORD_TOKEN not found in environment variables")

# Initialize the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="~", intents=intents)

# Replace this with your own Discord user ID to receive DMs
YOUR_USER_ID = 223688811845124096  # Replace with your actual Discord user ID

# List of cogs to load
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
    'cogs.Twitch_Commands',
    'cogs.Discord_Commands'  # Ensure the path matches the directory structure
]

async def load_extensions():
    """Load all the initial extensions."""
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            logging.info(f'Loaded extension: {extension}')
        except Exception as e:
            logging.error(f'Failed to load extension {extension}: {e}')

# Error handler to send DM on errors
@bot.event
async def on_command_error(ctx, error):
    """Handles errors globally and sends a DM to the specified user with the error details."""
    user = await bot.fetch_user(YOUR_USER_ID)
    error_message = f"An error occurred in the bot:\n{str(error)}"
    logging.error(error_message)
    
    # Send error message as a DM to you
    if user:
        await user.send(error_message)
    
    # Optionally, send error message in the channel where it occurred
    await ctx.send("An error occurred. The bot owner has been notified.")
    raise error


openai.api_key = os.getenv("OPEN_API_KEY")

@bot.command()
async def ai_chat(ctx, *, message):
    response = openai.Completion.create(
        engine="davinci",
        prompt=message,
        max_tokens=150
    )
    await ctx.send(response.choices[0].text.strip())


# Task to pull from GitHub and restart the bot
def pull_and_restart():
    current_time = datetime.now().strftime("%H:%M")
    if current_time == "10:35":  # Check if it's 10:35 AM
        logging.info("Initiating Git pull and restart process at 10:35 AM.")
        
        # Pull the latest changes from the repository
        try:
            result = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True)
            logging.info(f"Git pull output: {result.stdout}")
            
            # Restart the bot
            logging.info("Restarting bot...")
            subprocess.run([sys.executable, *sys.argv], shell=True)
            sys.exit()  # Ensure the current process exits after the restart
        except subprocess.CalledProcessError as e:
            logging.error(f"Error during Git pull: {e.stderr}")
        except Exception as e:
            logging.error(f"Unexpected error during restart: {str(e)}")


# Schedule the task to run every minute to check for 5:00 AM
schedule.every().minute.do(pull_and_restart)
logging.info("Scheduled Git pull and restart at 5:00 AM.")

# Function to run the schedule in the background
def run_schedule():
    logging.info("Starting the scheduling thread.")
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduling in a separate thread
threading.Thread(target=run_schedule, daemon=True).start()

async def main():
    """Main function to start the bot and load extensions."""
    await load_extensions()
    await bot.start(discord_token)

# Run the bot
asyncio.run(main())