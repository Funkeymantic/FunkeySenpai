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
    category = discord.utils.get(ctx.guild.categories, name='𝕋ℝ𝔼𝔼 ℍ𝕆𝕌𝕊𝔼')
    
    # Create category if it doesn't exist
    if category is None:
        category = await ctx.guild.create_category('𝕋ℝ𝔼𝔼 ℍ𝕆𝕌𝕊𝔼')
    
    # Create the voice channel in the category
    voice_channel = await ctx.guild.create_voice_channel(fancy_channel_name, category=category)
    
    # Create the office role for the owner
    fancy_role_name = ''.join(fancy_font.get(char, char) for char in f"{channel_name} Key")
    office_role = await ctx.guild.create_role(name=fancy_role_name, permissions=discord.Permissions(connect=True, speak=True))
    
    # Assign the office role to the user
    await user.add_roles(office_role)
    
    # Add explicit permissions for the owner in the voice channel
    await voice_channel.set_permissions(user, manage_permissions=True, connect=True, speak=True)
    
    # Set default permissions to prevent others from connecting
    await voice_channel.set_permissions(ctx.guild.default_role, connect=False)
    
    # Grant mods permissions to manage the voice channel
    for mod_role in ['Dungeon Master', 'Deities']:
        role = discord.utils.get(ctx.guild.roles, name=mod_role)
        if role:
            await voice_channel.set_permissions(role, manage_channels=True, connect=True)
    
    await ctx.send(f"Office '{channel_name}' has been created for {user.mention}!")

# Command to give a key (role) to a user
@discord_bot.command()
@commands.has_any_role('Dungeon Master', 'Deities')
async def givekey(ctx, user: discord.Member):
    # Get the voice channel the command was used in
    if ctx.author.voice and ctx.author.voice.channel:
        vc = ctx.author.voice.channel
    else:
        await ctx.send("You must be in the voice channel you own to use this command.")
        return

    # Check if the author has explicit permissions on the voice channel (owner check)
    owner_permissions = vc.overwrites_for(ctx.author)
    if owner_permissions.manage_permissions:
        # Find the office role (key role) associated with the voice channel
        role_name = f"{vc.name} Key"
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role is None:
            await ctx.send("Could not find the key role for this office.")
            return
        
        # Add the role to the specified user
        await user.add_roles(role)
        await ctx.send(f"{user.mention} has been given the key to '{vc.name}'!")
    else:
        await ctx.send("You don't have permission to give keys in this voice channel.")

# Command to take a key (role) from a user
@discord_bot.command()
@commands.has_any_role('Dungeon Master', 'Deities')
async def takekey(ctx, user: discord.Member):
    # Get the voice channel the command was used in
    if ctx.author.voice and ctx.author.voice.channel:
        vc = ctx.author.voice.channel
    else:
        await ctx.send("You must be in the voice channel you own to use this command.")
        return

    # Check if the author has explicit permissions on the voice channel (owner check)
    owner_permissions = vc.overwrites_for(ctx.author)
    if owner_permissions.manage_permissions:
        # Find the office role (key role) associated with the voice channel
        role_name = f"{vc.name} Key"
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role is None:
            await ctx.send("Could not find the key role for this office.")
            return
        
        # Remove the role from the specified user
        await user.remove_roles(role)
        await ctx.send(f"The key has been taken from {user.mention} for '{vc.name}'.")
    else:
        await ctx.send("You don't have permission to take keys in this voice channel.")
