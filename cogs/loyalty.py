import discord
from discord.ext import commands
import sqlite3

class Loyalty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('loyalty_points.db')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS points (user_id INTEGER PRIMARY KEY, points INTEGER)")
    
    @commands.command(name="points")
    async def points(self, ctx):
        user_id = ctx.author.id
        self.cur.execute("SELECT points FROM points WHERE user_id = ?", (user_id,))
        row = self.cur.fetchone()
        points = row[0] if row else 0
        await ctx.send(f"{ctx.author.mention}, you have {points} points.")

    @commands.command(name="addpoints")
    async def add_points(self, ctx, points: int):
        user_id = ctx.author.id
        self.cur.execute("INSERT OR IGNORE INTO points (user_id, points) VALUES (?, ?)", (user_id, 0))
        self.cur.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (points, user_id))
        self.conn.commit()
        await ctx.send(f"Added {points} points to {ctx.author.mention}.")

def setup(bot):
    bot.add_cog(Loyalty(bot))
