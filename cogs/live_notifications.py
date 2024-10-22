from discord.ext import commands
import discord
import requests
import os

class LiveNotifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def refresh_twitch_users(self):
        # Refresh the list of users with the streamer role and their Twitch accounts
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        await self.refresh_twitch_users()

def setup(bot):
    bot.add_cog(LiveNotifications(bot))
