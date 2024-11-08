import discord
import sqlite3
from discord.ext import commands

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('quotes.db')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS quotes (id INTEGER PRIMARY KEY, quote TEXT)")

    @commands.command(name="quote")
    async def quote(self, ctx, *, quote: str = None):
        if quote:
            self.cur.execute("INSERT INTO quotes (quote) VALUES (?)", (quote,))
            self.conn.commit()
            await ctx.send("Quote added.")
        else:
            self.cur.execute("SELECT quote FROM quotes ORDER BY RANDOM() LIMIT 1")
            row = self.cur.fetchone()
            await ctx.send(row[0] if row else "No quotes available.")

async def setup(bot):
    await bot.add_cog(Quotes(bot))