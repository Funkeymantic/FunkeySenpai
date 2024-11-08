import discord
from discord.ext import commands
import datetime
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery

class schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="schedule")
    async def schedule(self, ctx):
        # Connect to Google Calendar API (OAuth2 setup required)
        creds = None
        service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=5, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        
        if not events:
            await ctx.send("No upcoming events found.")
            return

        event_list = ""
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_list += f"{event['summary']} - {start}\n"
        
        await ctx.send(f"Upcoming schedule:\n{event_list}")

async def setup(bot):
    await bot.add_cog(schedule(bot))