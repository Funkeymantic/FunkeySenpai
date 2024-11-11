import discord
from discord.ext import commands

class Socials(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.social_links = {
            "twitter": "https://twitter.com/Funkeymantic",
            "youtube": "https://youtube.com/Funkeymantic",
            "instagram": "https://instagram.com/Funkeymantic"
        }

    @commands.command(name="socials")
    async def socials(self, ctx):
        links = "\n".join([f"{platform}: {url}" for platform, url in self.social_links.items()])
        await ctx.send(f"Follow on social media:\n{links}")

async def setup(bot):
    await bot.add_cog(Socials(bot))