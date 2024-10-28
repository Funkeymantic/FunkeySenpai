import discord
from discord.ext import commands

class Alerts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.custom_alerts = {
            "follow": "{user} just followed!",
            "subscribe": "Thank you {user} for subscribing!",
            "donation": "Wow, {user} donated ${amount}!"
        }

    @commands.command(name="setalert")
    async def set_alert(self, ctx, alert_type: str, *, message: str):
        if alert_type in self.custom_alerts:
            self.custom_alerts[alert_type] = message
            await ctx.send(f"Custom alert for {alert_type} updated.")
        else:
            await ctx.send("Invalid alert type. Choose from 'follow', 'subscribe', 'donation'.")

def setup(bot):
    bot.add_cog(Alerts(bot))