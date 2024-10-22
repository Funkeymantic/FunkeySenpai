from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log_action(self, action):
        with open("actions.log", "a") as log_file:
            log_file.write(action + "\n")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        await self.log_action(f"User {user} was banned in {guild.name}")

def setup(bot):
    bot.add_cog(Logging(bot))
