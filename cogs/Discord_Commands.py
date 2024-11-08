from discord.ext import commands
import discord
import os
from utils.discord_helpers import timestamp, fancy_font


class OfficeManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def hello(self, ctx):
    #     await ctx.send('Hello!')

    # Command for new Office (TREE HOUSE)
    @commands.command()
    @commands.has_any_role('Dungeon Master', 'Deities')
    async def createhouse(self, ctx, channel_name: str, user: discord.Member):
        fancy_channel_name = ''.join(fancy_font.get(char, char) for char in channel_name)
        category = discord.utils.get(ctx.guild.categories, name='𝗧𝗿𝗲𝗲 𝗛𝗼𝘂𝘀𝗲')
        
        # Create category if it doesn't exist
        if category is None:
            category = await ctx.guild.create_category('𝗧𝗿𝗲𝗲 𝗛𝗼𝘂𝘀𝗲')
        
        # Create the voice channel in the category
        voice_channel = await ctx.guild.create_voice_channel(fancy_channel_name, category=category)
        
        # Create the office role for the owner
        fancy_role_name = ''.join(fancy_font.get(char, char) for char in f"{channel_name} 𝙺𝚎𝚢")
        office_role = await ctx.guild.create_role(name=fancy_role_name, permissions=discord.Permissions(connect=True, speak=True))
        
        # Assign the office role to the user
        await user.add_roles(office_role)
        
        # Add explicit permissions for the owner in the voice channel
        await voice_channel.set_permissions(user, manage_permissions=True, connect=True, speak=True)
        
        # Set default permissions to prevent others from connecting
        await voice_channel.set_permissions(ctx.guild.default_role, connect=False)
        
        # Grant mods permissions to manage the voice channel
        for mod_role in ('Dungeon Master', 'Deities'):
            role = discord.utils.get(ctx.guild.roles, name=mod_role)
            if role:
                await voice_channel.set_permissions(role, manage_channels=True, connect=True)
        
        await ctx.send(f"Office '{channel_name}' has been created for {user.mention}!")

    # Command to give a 𝙺𝚎𝚢 (role) to a user
    @commands.command()
    @commands.has_any_role('Dungeon Master', 'Deities')
    async def givekey(self, ctx, user: discord.Member):
        if ctx.author.voice and ctx.author.voice.channel:
            vc = ctx.author.voice.channel
        else:
            await ctx.send("You must be in the voice channel you own to use this command.")
            return

        if 'Deities' in [role.name for role in ctx.author.roles] or 'Dungeon Master' in [role.name for role in ctx.author.roles] or vc.overwrites_for(ctx.author).manage_permissions:
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
    @commands.has_any_role('Dungeon Master', 'Deities')
    async def takekey(self, ctx, user: discord.Member):
        if ctx.author.voice and ctx.author.voice.channel:
            vc = ctx.author.voice.channel
        else:
            await ctx.send("You must be in the voice channel you own to use this command.")
            return

        if 'Deities' in [role.name for role in ctx.author.roles] or 'Dungeon Master' in [role.name for role in ctx.author.roles] or vc.overwrites_for(ctx.author).manage_permissions:
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
