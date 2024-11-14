import os
from discord.ext import commands  # Use Discord's commands for the cog
from twitchio.ext import commands as twitch_commands
import random

class TwitchCommands(commands.Cog):  # Inherit from discord.ext.commands.Cog
    def __init__(self, bot):
        self.bot = bot  # Reference to the main bot instance
        twitch_token = os.getenv("TWITCH_OAUTH_TOKEN")

        if not twitch_token:
            raise ValueError("Twitch OAuth token is missing. Please set TWITCH_OAUTH_TOKEN in your .env file.")

        self.twitch_bot = twitch_commands.Bot(
            token=twitch_token,
            prefix="!",
            initial_channels=[os.getenv("TWITCH_CHANNEL")]
        )

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

    async def start_twitch_bot(self):
        await self.twitch_bot.start()  # Start the Twitch bot

    async def cog_load(self):
        """Runs when the cog is loaded to start the Twitch bot asynchronously."""
        self.bot.loop.create_task(self.start_twitch_bot())  # Start Twitch bot as an async task

# Setup function to add the cog
async def setup(bot):
    await bot.add_cog(TwitchCommands(bot))
