import discord
from discord.ext import commands
from game_apis import valorant_api, cod_api, satisfactory_api, rocketleague_api, overwatch_api

class ContestManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_contests = {}

    @commands.command(name="create_contest")
    @commands.has_permissions(manage_guild=True)
    async def create_contest(self, ctx):
        """Command to create a contest with customizable parameters."""
        await ctx.send("Let's set up a new contest! Please answer the following questions.")

        def check_message(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            # Get game
            await ctx.send("What game is the contest for? (e.g., Valorant, Call of Duty, Satisfactory, Rocket League, Overwatch)")
            game_message = await self.bot.wait_for('message', check=check_message, timeout=120.0)
            game = game_message.content.lower()

            # Get other contest parameters
            await ctx.send("When does the contest start? (format: YYYY-MM-DD)")
            start_date_message = await self.bot.wait_for('message', check=check_message, timeout=120.0)
            start_date = start_date_message.content

            await ctx.send("What is the contest objective? (e.g., most kills, highest score)")
            objective_message = await self.bot.wait_for('message', check=check_message, timeout=120.0)
            objective = objective_message.content

            await ctx.send("What is the reward?")
            reward_message = await self.bot.wait_for('message', check=check_message, timeout=120.0)
            reward = reward_message.content

            contest_id = len(self.active_contests) + 1
            self.active_contests[contest_id] = {
                "game": game,
                "start_date": start_date,
                "objective": objective,
                "reward": reward,
                "participants": []
            }

            await ctx.send(f"Contest created successfully for {game.capitalize()}! Contest ID: {contest_id}")

        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

    @commands.command(name="join_contest")
    async def join_contest(self, ctx, contest_id: int, player_id: str):
        """Command for users to join a contest."""
        if contest_id not in self.active_contests:
            await ctx.send("Invalid contest ID. Please check and try again.")
            return

        contest = self.active_contests[contest_id]
        game = contest['game']
        user = ctx.author

        # Fetch player stats based on game
        if game == "valorant":
            player_stats = valorant_api.get_player_stats(player_id)
        elif game == "call of duty":
            player_stats = cod_api.get_player_stats(player_id)
        elif game == "satisfactory":
            player_stats = satisfactory_api.get_player_stats(player_id)
        elif game == "rocket league":
            player_stats = rocketleague_api.get_player_stats(player_id)
        elif game == "overwatch":
            player_stats = overwatch_api.get_player_stats(player_id)
        else:
            await ctx.send("Unsupported game for contest.")
            return

        # Add player to the contest if stats are fetched successfully
        if player_stats:
            contest['participants'].append({
                "discord_name": str(user),
                "discord_id": user.id,
                "player_id": player_id,
                "stats": player_stats
            })
            await ctx.send(f"{user.mention}, you have successfully joined the contest '{game.capitalize()}' with Player ID: {player_id}.")
        else:
            await ctx.send(f"Failed to fetch stats for Player ID: {player_id} in '{game.capitalize()}'.")

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(ContestManagement(bot))
