from discord.ext import commands

class Gear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gear = {
            "Gaming Computer":
                "CPU: AMD Ryzen 9 7900X"
                "GPU: GeForce RTX 4070 Ti SUPER",
            "Gaming Computer Peripheral": 
                "Steel Series APEX PRO"
                "Orei HDMI Martix 2x2",
            "Audio":
                "Desktop Speakers: Cerwin-Vegas"
                "Mixer: Mackie Mix12FX",
            "Streaming Computer":
                "CPU: Intel i7-6700K"
                "GPU: Geforce RTX 3080",
            "Streaming Computer Periferals":
                "Stream Deck Mk1",
            "Microphone": "Shure SM7B",
            "Camera": "Sony a5100",
            "Headset": "SteelSeries Arctis Pro"
        }

    @commands.command(name="gear")
    async def gear(self, ctx):
        setup = "\n".join([f"{item}: {detail}" for item, detail in self.gear.items()])
        await ctx.send(f"Streamer Setup:\n{setup}")

async def setup(bot):
    await bot.add_cog(Gear(bot))
