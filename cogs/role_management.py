import discord
from discord.ext import commands

class RoleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reaction_roles = {}

    @commands.command(name="setup_reaction_roles")
    @commands.has_permissions(manage_roles=True)
    async def setup_reaction_roles(self, ctx):
        """Command to set up reaction role message."""
        await ctx.send("Let's set up the role reactions! What message would you like users to react to? (type the message below)")

        def check_message(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            # Wait for the user to provide the message
            message_content = await self.bot.wait_for('message', check=check_message, timeout=120.0)
            message_text = message_content.content

            # List of emote-role pairs
            emote_role_pairs = []
            while True:
                await ctx.send("Please provide an emoji and the role name it should be linked to (format: :emoji: role_name). Type 'done' when finished.")

                emoji_role_message = await self.bot.wait_for('message', check=check_message, timeout=120.0)
                if emoji_role_message.content.lower() == 'done':
                    break

                # Parse the emoji and role from the input
                try:
                    emoji, role_name = emoji_role_message.content.split()
                    role = discord.utils.get(ctx.guild.roles, name=role_name)

                    if role is None:
                        await ctx.send(f"Role '{role_name}' not found. Please try again.")
                        continue

                    emote_role_pairs.append((emoji, role))
                    await ctx.send(f"Added role '{role_name}' for emoji '{emoji}'.")

                except ValueError:
                    await ctx.send("Invalid format. Please use the format ':emoji: role_name'.")
            
            await ctx.send("Is that all the reactions? (yes/no)")
            confirmation = await self.bot.wait_for('message', check=check_message, timeout=60.0)

            if confirmation.content.lower() == 'no':
                await ctx.send("You can continue adding more reactions.")
                return

            # Ask if the user can have multiple reactions or only one
            await ctx.send("Can users select multiple roles, or only one? (multiple/one)")
            multiple_selection = await self.bot.wait_for('message', check=check_message, timeout=60.0)
            allow_multiple = multiple_selection.content.lower() == 'multiple'

            # Ask what channel to publish this message to
            await ctx.send("Which channel should the reaction message be posted to? Please mention the channel (e.g. #general).")
            channel_message = await self.bot.wait_for('message', check=check_message, timeout=60.0)

            try:
                channel = channel_message.channel_mentions[0]
            except IndexError:
                await ctx.send("You did not mention a valid channel. Cancelling the setup.")
                return

            # Publish the reaction message to the specified channel
            published_message = await channel.send(message_text)
            for emoji, _ in emote_role_pairs:
                await published_message.add_reaction(emoji)

            # Store the emoji-role pairs for this message
            self.reaction_roles[published_message.id] = {
                "roles": emote_role_pairs,
                "multiple": allow_multiple
            }

            # Clean up by deleting the setup messages in the mod channel
            await ctx.channel.purge(limit=100, check=lambda msg: msg.author == ctx.author or msg.author == self.bot.user)

            await ctx.send(f"Reaction roles set up successfully in {channel.mention}!", delete_after=5)

        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Handle adding roles based on reactions."""
        if payload.message_id not in self.reaction_roles:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member is None or member.bot:
            return

        role_data = self.reaction_roles[payload.message_id]
        emoji = str(payload.emoji)
        for emote, role in role_data['roles']:
            if emoji == emote:
                if not role_data['multiple']:
                    # Remove all other roles if only one is allowed
                    for _, r in role_data['roles']:
                        if r in member.roles:
                            await member.remove_roles(r)
                await member.add_roles(role)
                await member.send(f"You've been assigned the {role.name} role!")
                break

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Handle removing roles when reactions are removed."""
        if payload.message_id not in self.reaction_roles:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member is None or member.bot:
            return

        role_data = self.reaction_roles[payload.message_id]
        emoji = str(payload.emoji)
        for emote, role in role_data['roles']:
            if emoji == emote:
                await member.remove_roles(role)
                await member.send(f"The {role.name} role has been removed from you!")
                break

async def setup(bot):
    await bot.add_cog(RoleManagement(bot))