import discord
from discord.ext import commands

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poll")
    async def poll(self, ctx, *, question):
        message = await ctx.send(f"**{question}**\n👍 for yes | 👎 for no")
        await message.add_reaction("👍")
        await message.add_reaction("👎")

def setup(bot):
    bot.add_cog(Poll(bot))
