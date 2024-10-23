from discord.ext import commands
import discord
import os
from discord_helpers import timestamp
from discord_helpers import fancy_font

# Define Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True
intents.voice_states = True

# Discord bot instance
discord_bot = commands.Bot(command_prefix='~', intents=intents, case_insensitive=True)

# Command for new Office (TREE HOUSE)
@discord_bot.command()
@commands.has_role('Dungeon Master', 'Deities')
async def createhouse(ctx, channel_name: str, user: discord.Member):
    fancy_channel_name = ''.join(fancy_font.get(char, char) for char in channel_name)
    category = discord.utils.get(ctx.guild.categories, name = '𝕋ℝ𝔼𝔼 ℍ𝕆𝕌𝕊𝔼')
    if category is None:
        category = await ctx.guild.create_category('𝕋ℝ𝔼𝔼 ℍ𝕆𝕌𝕊𝔼')
    voice_channel = await ctx.guild.create_voice_channel(fancy_channel_name, category=category)
    fancy_role_name = ''.join(fancy_font.get(char, char) for char in f"{channel_name} Key")
    office_role = await ctx.guild.create_role(name=fancy_role_name, permissions=discord.Permissions(connect=True, speak=True))
    await user.add_roles(office_role)
    await voice_channel.set_permissions(user, manage_permissions=True, connect=True, speak=True)
    await voice_channel.set_permissions(ctx.guild.default_role, connect=False)
    for mod_role in ['Dungeon Master', 'Deities']:
        role = discord.utils.get(ctx.guild.roles, name=mod_role)
        if role:
            await voice_channel.set_permissions(role, manage_channels=True, connect=True)
    await ctx.send(f"Office '{channel_name}' has been created for {user.mention}!")