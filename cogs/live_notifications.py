from discord.ext import commands, tasks
import discord
import requests
import os

class LiveNotifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.streamers = {}  # Store streamer data
        self.performance_role_name = "Performance Check"
        self.own_channel_id = int(os.getenv("OWN_CHANNEL_ID"))  # Channel for Funkeymantic
        self.performance_channel_id = int(os.getenv("PERFORMANCE_CHANNEL_ID"))  # Channel for other streamers
        self.twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
        self.twitch_client_secret = os.getenv("TWITCH_CLIENT_SECRET")
        self.token = None
        self.check_streamers.start()  # Start the periodic task

    async def refresh_twitch_users(self):
        # Refresh the list of users with the streamer role and their Twitch accounts
        guild = self.bot.guilds[0]  # Assuming single server
        role = discord.utils.get(guild.roles, name=self.performance_role_name)
        if role:
            self.streamers = {member.display_name: member for member in role.members}
        
    async def get_twitch_token(self):
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": self.twitch_client_id,
            "client_secret": self.twitch_client_secret,
            "grant_type": "client_credentials"
        }
        response = requests.post(url, params=params)
        if response.status_code == 200:
            self.token = response.json()["access_token"]

    async def check_if_live(self, streamer_name):
        url = f"https://api.twitch.tv/helix/streams"
        headers = {
            "Client-ID": self.twitch_client_id,
            "Authorization": f"Bearer {self.token}"
        }
        params = {"user_login": streamer_name}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        return bool(data["data"])  # True if live, False otherwise

    @tasks.loop(minutes=5)
    async def check_streamers(self):
        if not self.token:
            await self.get_twitch_token()
        await self.refresh_twitch_users()
        
        for streamer_name, member in self.streamers.items():
            is_live = await self.check_if_live(streamer_name)
            if is_live:
                if streamer_name.lower() == "funkeymantic":
                    # Post to your own channel
                    channel = self.bot.get_channel(self.own_channel_id)
                else:
                    # Post to performance check channel
                    channel = self.bot.get_channel(self.performance_channel_id)

                if channel:
                    await channel.send(f"{streamer_name} is now live! Check it out at https://twitch.tv/{streamer_name}")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.refresh_twitch_users()
        print("Live notifications cog is ready and monitoring streamers.")

async def setup(bot):
    await bot.add_cog(LiveNotifications(bot))
