from discord.ext import commands
import discord
import os
from utils.discord_helpers import timestamp, fancy_font
import sys
import subprocess
import random
import textwrap

class OfficeManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Shutdown command, restricted to moderators
    @commands.command(name="shutdown")
    @commands.has_any_role('🧙‍♂️ Dungeon Master (Admin)', '🍺 Tavern Keeper (Moderator)')
    async def shutdown(self, ctx):
        await ctx.send("Shutting down the bot...")
        await self.bot.close()

    # Restart command, restricted to moderators
    @commands.command(name="restart")
    @commands.has_any_role('🧙‍♂️ Dungeon Master (Admin)', '🍺 Tavern Keeper (Moderator)')
    async def restart(self, ctx):
        await ctx.send("Pulling latest changes from GitHub and restarting the bot...")

        # Pull the latest changes from the repository
        result = subprocess.run(["git", "pull"], capture_output=True, text=True)
        await self.send_long_message(ctx, f"Git pull output:\n{result.stdout}")

        # Install requirements
        install_result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], capture_output=True, text=True)

        # Fetch the owner user defined in bot.py
        owner_user = await self.bot.fetch_user(223688811845124096)  # Replace with YOUR_USER_ID from bot.py
        if owner_user:
            await self.send_long_message_dm(owner_user, f"Pip install output:\n{install_result.stdout}")

        # Restart the bot
        os.execv(sys.executable, [sys.executable] + sys.argv)

    async def send_long_message(self, ctx, content, limit=2000):
        """Sends long messages split into chunks in the current channel."""
        for chunk in textwrap.wrap(content, limit):
            await ctx.send(chunk)

    async def send_long_message_dm(self, user, content, limit=2000):
        """Sends long messages split into chunks as a DM."""
        for chunk in textwrap.wrap(content, limit):
            await user.send(chunk)


    @commands.command(name="roll")
    async def roll(self, ctx, dice: str):
        """Rolls a dice. Use formats like d6, d20, d100."""
        try:
            # Extract the number of sides from the dice format (e.g., "d20")
            sides = int(dice[1:])
            if sides in [2, 4, 6, 8, 10, 20, 100]:
                result = random.randint(1, sides)
                await ctx.send(f"{ctx.author.mention} rolled a {dice}: **{result}**")
            else:
                await ctx.send("Invalid dice type! Use one of: d2, d4, d6, d8, d10, d20, d100.")
        except ValueError:
            await ctx.send("Invalid format! Please use the format like d20, d6, etc.")
    
    # Command for new Office (𝐓𝐡𝐞 𝐆𝐮𝐢𝐥𝐝 𝐎𝐟𝐟𝐢𝐜𝐞𝐬 (𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐕𝐂𝐬))
    @commands.command()
    @commands.has_any_role('🧙‍♂️ Dungeon Master (Admin)', '🍺 Tavern Keeper (Moderator)')
    async def createhouse(self, ctx, channel_name: str, user: discord.Member):
        fancy_channel_name = ''.join(fancy_font.get(char, char) for char in channel_name)
        category = discord.utils.get(ctx.guild.categories, name='𝗧𝗿𝗲𝗲 𝗛𝗼𝘂𝘀𝗲')

        # Create category if it doesn't exist
        if category is None:
            category = await ctx.guild.create_category('𝐓𝐡𝐞 𝐆𝐮𝐢𝐥𝐝 𝐎𝐟𝐟𝐢𝐜𝐞𝐬 (𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐕𝐂𝐬)')

        # Create the voice channel in the category
        voice_channel = await ctx.guild.create_voice_channel(fancy_channel_name, category=category)

        # Create the office role for the owner
        fancy_role_name = ''.join(fancy_font.get(char, char) for char in f"{channel_name} 𝙺𝚎𝚢")
        office_role = await ctx.guild.create_role(name=fancy_role_name, permissions=discord.Permissions(connect=True, speak=True))

        # Assign the office role to the user
        await user.add_roles(office_role)

        # Add explicit permissions for the owner in the voice channel
        await voice_channel.set_permissions(user, overwrite=discord.PermissionOverwrite(manage_permissions=True, connect=True, speak=True, view_channel=True))

        # Set default permissions to prevent others from connecting or viewing
        await voice_channel.set_permissions(ctx.guild.default_role, overwrite=discord.PermissionOverwrite(connect=False, view_channel=False))

        # Grant mods permissions to manage the voice channel
        for mod_role in ('🧙‍♂️ Dungeon Master (Admin)', '🍺 Tavern Keeper (Moderator)'):
            role = discord.utils.get(ctx.guild.roles, name=mod_role)
            if role:
                await voice_channel.set_permissions(role, overwrite=discord.PermissionOverwrite(manage_channels=True, connect=True, view_channel=True))

        await ctx.send(f"Office '{channel_name}' has been created for {user.mention}!")

    # Command to give a 𝙺𝚎𝚢 (role) to a user
    @commands.command()
    @commands.has_any_role('🧙‍♂️ Dungeon Master (Admin)', '🍺 Tavern Keeper (Moderator)')
    async def givekey(self, ctx, user: discord.Member):
        if ctx.author.voice and ctx.author.voice.channel:
            vc = ctx.author.voice.channel
        else:
            await ctx.send("You must be in the voice channel you own to use this command.")
            return

        if '🍺 Tavern Keeper (Moderator)' in [role.name for role in ctx.author.roles] or '🧙‍♂️ Dungeon Master (Admin)' in [role.name for role in ctx.author.roles] or vc.overwrites_for(ctx.author).manage_permissions:
            role_name = f"{vc.name} 𝙺𝚎𝚢"
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role is None:
                await ctx.send("Could not find the 𝙺𝚎𝚢 role for this office.")
                return
            
            await user.add_roles(role)
            await ctx.send(f"{user.mention} has been given the 𝙺𝚎𝚢 to '{vc.name}'!")
        else:
            await ctx.send("You don't have permission to give 𝙺𝚎𝚢s in this voice channel.")

    # Command to take a 𝙺𝚎𝚢 (role) from a user
    @commands.command()
    @commands.has_any_role('🧙‍♂️ Dungeon Master (Admin)', '🍺 Tavern Keeper (Moderator)')
    async def takekey(self, ctx, user: discord.Member):
        if ctx.author.voice and ctx.author.voice.channel:
            vc = ctx.author.voice.channel
        else:
            await ctx.send("You must be in the voice channel you own to use this command.")
            return

        if '🍺 Tavern Keeper (Moderator)' in [role.name for role in ctx.author.roles] or '🧙‍♂️ Dungeon Master (Admin)' in [role.name for role in ctx.author.roles] or vc.overwrites_for(ctx.author).manage_permissions:
            role_name = f"{vc.name} 𝙺𝚎𝚢"
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role is None:
                await ctx.send("Could not find the 𝙺𝚎𝚢 role for this office.")
                return
            
            await user.remove_roles(role)
            await ctx.send(f"The 𝙺𝚎𝚢 has been taken from {user.mention} for '{vc.name}'.")
        else:
            await ctx.send("You don't have permission to take 𝙺𝚎𝚢s in this voice channel.")

# Setup function to add the cog
async def setup(bot):
    await bot.add_cog(OfficeManagement(bot))