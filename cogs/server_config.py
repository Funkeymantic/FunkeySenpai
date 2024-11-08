from discord.ext import commands
import discord
import json

class ServerConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = 'server_config.json'  # Ensure this path is correct

    def load_config(self):
        """Load the server configurations from file."""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"servers": {}}

    def save_config(self, config):
        """Save the server configurations to file."""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def get_server_config(self, guild_id):
        """Get the configuration for a specific server."""
        config = self.load_config()
        return config["servers"].get(str(guild_id), {})

    def set_server_config(self, guild_id, new_config):
        """Set the configuration for a specific server."""
        config = self.load_config()
        config["servers"][str(guild_id)] = new_config
        self.save_config(config)

    @commands.command(name="set_channel")
    @commands.has_permissions(administrator=True)
    async def set_channel(self, ctx, channel: discord.TextChannel):
        """Set the default channel for the bot in the server."""
        guild_id = ctx.guild.id
        config = self.get_server_config(guild_id)
        config["channel_id"] = channel.id
        self.set_server_config(guild_id, config)
        await ctx.send(f"Default channel set to {channel.mention}")

    @commands.command(name="set_category")
    @commands.has_permissions(administrator=True)
    async def set_category(self, ctx, category: discord.CategoryChannel):
        """Set the default category for the bot in the server."""
        guild_id = ctx.guild.id
        config = self.get_server_config(guild_id)
        config["category_id"] = category.id
        self.set_server_config(guild_id, config)
        await ctx.send(f"Default category set to {category.name}")

    @commands.command(name="set_role")
    @commands.has_permissions(administrator=True)
    async def set_role(self, ctx, role: discord.Role):
        """Set a specific role for the bot to assign or track."""
        guild_id = ctx.guild.id
        config = self.get_server_config(guild_id)
        config["role_id"] = role.id
        self.set_server_config(guild_id, config)
        await ctx.send(f"Role set to {role.name}")

    @commands.command(name="show_config")
    @commands.has_permissions(administrator=True)
    async def show_config(self, ctx):
        """Show the current server configuration."""
        guild_id = ctx.guild.id
        config = self.get_server_config(guild_id)

        if not config:
            await ctx.send("No configuration found for this server.")
            return

        channel = self.bot.get_channel(config.get("channel_id", None))
        category = self.bot.get_channel(config.get("category_id", None))
        role = ctx.guild.get_role(config.get("role_id", None))

        await ctx.send(f"**Server Configurations:**\n"
                       f"Channel: {channel.mention if channel else 'Not set'}\n"
                       f"Category: {category.name if category else 'Not set'}\n"
                       f"Role: {role.name if role else 'Not set'}")

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(ServerConfig(bot))
