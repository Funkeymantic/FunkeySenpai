import discord
from discord.ext import commands
import datetime
import asyncio

class ContestManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_contests = {}
        self.contest_participants = {}
    
    @commands.command(name="create_contest")
    @commands.has_permissions(manage_guild=True)
    async def create_contest(self, ctx):
        """Command to create a contest with customizable parameters."""
        await ctx.send("Let's set up a new contest! Please answer the following questions.")

        def check_message(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            # Get game
            await ctx.send("What game is the contest for?")
            game_message = await self.bot.wait_for('message', check=check_message, timeout=120.0)
            game = game_message.content

            # Get start date
            await ctx.send("When does the contest start? (format: YYYY-MM-DD)")
            start_date_message = await self.bot.wait_for('message', check=check_message, timeout=120.0)
            start_date = datetime.datetime.strptime(start_date_message.content, "%Y-%m-%d")

            # Get duration
            await ctx.send("How long is the contest duration? (e.g., 5 days, 2 weeks)")
            duration_message = await self.bot.wait_for('message', check=check_message, timeout=120.0)
            duration = duration_message.content

            # Get reward
            await ctx.send("What is the reward for winning the contest?")
            reward_message = await self.bot.wait_for('message', check=check_message, timeout=120.0)
            reward = reward_message.content

            # Get objective
            await ctx.send("What is the contest objective? (e.g., most kills, highest score)")
            objective_message = await self.bot.wait_for('message', check=check_message, timeout=120.0)
            objective = objective_message.content

            # Followers or Subscribers
            await ctx.send("Is this contest for followers, subscribers, or both?")
            group_message = await self.bot.wait_for('message', check=check_message, timeout=120.0)
            group = group_message.content

            # Get rules (comma-separated)
            await ctx.send("What are the contest rules? Please separate by commas.")
            rules_message = await self.bot.wait_for('message', check=check_message, timeout=120.0)
            rules = rules_message.content.split(',')

            # Store the contest details
            contest_id = len(self.active_contests) + 1
            self.active_contests[contest_id] = {
                "game": game,
                "start_date": start_date,
                "duration": duration,
                "reward": reward,
                "objective": objective,
                "group": group,
                "rules": rules,
                "participants": []
            }

            await ctx.send(f"Contest created successfully for {game}! Contest ID: {contest_id}")

        except asyncio.TimeoutError:
            await ctx.send("Contest setup timed out. Please try again.")

    @commands.command(name="join_contest")
    async def join_contest(self, ctx, contest_id: int, player_id: str):
        """Command for users to join a contest."""
        if contest_id not in self.active_contests:
            await ctx.send("Invalid contest ID. Please check and try again.")
            return

        contest = self.active_contests[contest_id]
        user = ctx.author

        # Check if user already joined
        if any(participant['discord_id'] == user.id for participant in contest['participants']):
            await ctx.send("You have already joined this contest!")
            return

        # Add user to contest participants
        participant_data = {
            "discord_name": str(user),
            "discord_id": user.id,
            "player_id": player_id
        }
        contest['participants'].append(participant_data)

        await ctx.send(f"{user.mention}, you have successfully joined the contest '{contest['game']}' with Player ID: {player_id}.")

    @commands.command(name="list_contests")
    async def list_contests(self, ctx):
        """Command to list all active contests."""
        if not self.active_contests:
            await ctx.send("There are no active contests at the moment.")
            return
        
        contest_list = []
        for contest_id, contest in self.active_contests.items():
            contest_info = (
                f"**Contest ID:** {contest_id}\n"
                f"**Game:** {contest['game']}\n"
                f"**Start Date:** {contest['start_date'].strftime('%Y-%m-%d')}\n"
                f"**Duration:** {contest['duration']}\n"
                f"**Reward:** {contest['reward']}\n"
                f"**Objective:** {contest['objective']}\n"
                f"**Group:** {contest['group']}\n"
                f"**Rules:** {', '.join(contest['rules'])}\n"
            )
            contest_list.append(contest_info)
        
        await ctx.send("\n\n".join(contest_list))

    @commands.command(name="list_participants")
    @commands.has_permissions(manage_guild=True)
    async def list_participants(self, ctx, contest_id: int):
        """Command to list participants for a given contest."""
        if contest_id not in self.active_contests:
            await ctx.send("Invalid contest ID. Please check and try again.")
            return

        contest = self.active_contests[contest_id]
        if not contest['participants']:
            await ctx.send("No participants have joined this contest yet.")
            return

        participant_list = []
        for participant in contest['participants']:
            participant_info = (
                f"**Discord Name:** {participant['discord_name']}\n"
                f"**Player ID:** {participant['player_id']}\n"
            )
            participant_list.append(participant_info)

        await ctx.send(f"Participants for contest '{contest['game']}':\n\n" + "\n\n".join(participant_list))

def setup(bot):
    bot.add_cog(ContestManagement(bot))
