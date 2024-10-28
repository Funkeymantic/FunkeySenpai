import discord
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lurk")
    async def lurk(self, ctx):
        await ctx.send(f"{ctx.author.mention} is now lurking!")

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send(f"Hello, {ctx.author.mention}!")

    @commands.command(name="goodbye")
    async def goodbye(self, ctx):
        await ctx.send(f"Goodbye, {ctx.author.mention}!")

def setup(bot):
    bot.add_cog(Greetings(bot))
