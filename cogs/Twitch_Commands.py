from twitchio.ext import commands
import random

class TwitchDiceBot(commands.Bot):
    def __init__(self):
        super().__init__(token='your_twitch_oauth_token', prefix='!', initial_channels=['your_channel_name'])

    @commands.command(name="roll")
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

if __name__ == "__main__":
    bot = TwitchDiceBot()
    bot.run()