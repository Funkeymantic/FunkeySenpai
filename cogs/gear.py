from discord.ext import commands

class Gear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gear = {
            "Microphone": "Shure SM7B",
            "Camera": "Sony a5100",
            "Headset": "SteelSeries Arctis Pro",
            "PC": "Custom-built gaming PC"
        }

    @commands.command(name="gear")
    async def gear(self, ctx):
        setup = "\n".join([f"{item}: {detail}" for item, detail in self.gear.items()])
        await ctx.send(f"Streamer Setup:\n{setup}")

def setup(bot):
    bot.add_cog(Gear(bot))
