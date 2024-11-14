from twitchio.ext import commands as twitch_commands
import random

class TwitchCommands(twitch_commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Reference to the main bot instance

    @twitch_commands.command(name="roll")
    async def roll(self, ctx, dice: str):
        """Rolls a dice. Use formats like d6, d20, d100."""
        try:
            # Extract the number of sides from the dice format
            sides = int(dice[1:])
            if sides in [2, 4, 6, 8, 10, 20, 100]:
                result = random.randint(1, sides)
                await ctx.send(f"{ctx.author.name} rolled a {dice}: {result}")
            else:
                await ctx.send("Invalid dice type! Use one of: d2, d4, d6, d8, d10, d20, d100.")
        except ValueError:
            await ctx.send("Invalid format! Please use the format like d20, d6, etc.")

async def setup(bot):
    await bot.add_cog(TwitchCommands(bot))
