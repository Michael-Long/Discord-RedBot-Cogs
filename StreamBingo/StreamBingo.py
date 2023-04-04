from redbot.core import commands

class StreamBingo(commands.Cog):
    """Stream Bingo Cog - Connects to Website to generate Bingo Boards"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")