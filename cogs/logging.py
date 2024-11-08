from discord.ext import commands
import discord
from datetime import datetime

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_name = "📝-𝚌𝚘𝚞𝚗𝚌𝚒𝚕-𝚌𝚑𝚊𝚖𝚋𝚎𝚛"

    async def log_action(self, action, guild):
        """Log the action to a file, print it to the terminal, and send it to the specified Discord channel."""
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        formatted_action = f"{timestamp} {action}"
        print(f"Logging action: {formatted_action}")  # Print to terminal for real-time monitoring

        # Log to a file
        try:
            with open("actions.log", "a", encoding="utf-8") as log_file:
                log_file.write(formatted_action + "\n")
        except Exception as e:
            print(f"Failed to write to file: {e}")

        # Send logs to the specified channel
        channel = discord.utils.get(guild.text_channels, name=self.log_channel_name)
        if channel:
            try:
                await channel.send(f"```{formatted_action}```")
            except discord.Forbidden:
                print("Bot lacks permission to send messages to the channel.")
            except Exception as e:
                print(f"Failed to send message to channel: {e}")
        else:
            print(f"Channel '{self.log_channel_name}' not found in guild '{guild.name}'.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            action = f"Message sent by {message.author} (ID: {message.author.id}) in #{message.channel}: '{message.content}'"
            print(action)  # Print to terminal
            # Optionally, log this action to a file or send it to the Discord channel
            # await self.log_action(action, message.guild)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            action = f"Message deleted in #{message.channel} by {message.author} (ID: {message.author.id}): '{message.content}'"
            print(action)  # Print to terminal
            await self.log_action(action, message.guild)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.author.bot:
            action = (f"Message edited in #{before.channel} by {before.author} (ID: {before.author.id}):\n"
                      f"Before: '{before.content}'\nAfter: '{after.content}'")
            print(action)  # Print to terminal
            await self.log_action(action, before.guild)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        action = f"Member joined: {member} (ID: {member.id})"
        await self.log_action(action, member.guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        action = f"Member left: {member} (ID: {member.id})"
        await self.log_action(action, member.guild)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        action = f"User {user} (ID: {user.id}) was banned from {guild.name}"
        await self.log_action(action, guild)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        action = f"User {user} (ID: {user.id}) was unbanned in {guild.name}"
        await self.log_action(action, guild)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            action = (f"Member roles updated for {before} (ID: {before.id}) in {before.guild}:\n"
                      f"Before: {[role.name for role in before.roles]}\nAfter: {[role.name for role in after.roles]}")
            await self.log_action(action, before.guild)

    @commands.Cog.listener()
    async def on_member_kick(self, member):
        action = f"User {member} (ID: {member.id}) was kicked from {member.guild.name}"
        await self.log_action(action, member.guild)

async def setup(bot):
    print("Setting up Logging cog...")
    await bot.add_cog(Logging(bot))
