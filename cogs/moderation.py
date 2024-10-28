from discord.ext import commands
import discord

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}

    @commands.command(name="warn")
    async def warn(self, ctx, user: discord.User, *, reason=None):
        await ctx.send(f"{user.mention} has been warned for: {reason}")

    @commands.command(name="kick")
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked for: {reason}")

def setup(bot):
    bot.add_cog(Moderation(bot))
