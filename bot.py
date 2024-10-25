import discord
from discord.ext import commands
import os
import time
import schedule
from datetime import datetime
import subprocess

# Initialize the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Load your cogs (if any)
initial_extensions = [
    'cogs.server_config',
    # Add other cogs here
]

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

# Define the task to pull from GitHub and restart the bot
def pull_and_restart():
    current_time = datetime.now().strftime("%H:%M")
    if current_time == "05:00":  # Check if it's 5:00 AM
        print("Pulling latest changes from GitHub...")
        
        # Pull the latest changes from the repository
        result = subprocess.run(["git", "pull"], capture_output=True, text=True)
        print(result.stdout)
        
        # Restart the bot
        print("Restarting bot...")
        os.execv(sys.executable, ['python'] + sys.argv)

# Schedule the task to run every minute to check for 5:00 AM
schedule.every().minute.do(pull_and_restart)

# Function to run the schedule in the background
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduling in a separate thread
import threading
threading.Thread(target=run_schedule, daemon=True).start()

# Run the bot
bot.run(os.getenv("DISCORD_TOKEN"))
