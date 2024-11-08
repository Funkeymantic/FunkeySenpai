import discord
from discord.ext import commands

class ToDoList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.todo_list = []

    @commands.command(name="addtodo")
    async def add_todo(self, ctx, *, task):
        self.todo_list.append(task)
        await ctx.send(f"Task added: {task}")

    @commands.command(name="listtodo")
    async def list_todo(self, ctx):
        if not self.todo_list:
            await ctx.send("To-do list is empty.")
        else:
            tasks = "\n".join(f"{idx + 1}. {task}" for idx, task in enumerate(self.todo_list))
            await ctx.send(f"To-do list:\n{tasks}")

async def setup(bot):
    await bot.add_cog(ToDoList(bot))