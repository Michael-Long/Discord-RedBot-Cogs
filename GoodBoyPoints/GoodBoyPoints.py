from redbot.core import checks, commands, Config

import random

class GoodBoyPoints(commands.Cog):
    """Good Boy Points Cog - Reward your friends with the points they deserve!"""

    def __init__(self, bot):
        self.bot = bot

        # Create Default Config
        self.config = Config.get_conf(self, identifier=7908234242)
        default_member = {
            "GoodBoyPoints": 0
        }

        self.config.register_member(**default_member)

    @commands.command()
    async def givePoints(self, ctx, friend: discord.Member, points):
        """Give points to a friend!"""
        if (friend.id == ctx.author.id):
            await ctx.send("You can't give yourself point, dingus.")
            return
        if (points < 0):
            await ctx.send("Why are you trying to give them negative points? :(")
            return
        elif (points == 0):
            await ctx.send("No points? what")
            return
        else:
            await self.config.member(friend).GoodBoyPoints.set(self.config.member(friend).GoodBoyPoints() + points)
            await ctx.send(ctx.author.name + " gave " + friend.mention + " " + points + " Good Boy Points!")

    @commands.command()
    async def checkPoints(self, ctx, user: discord.Member = None):
        """Check your own or someone else's Good Boy Points"""
        if (user == None):
            await ctx.send("Your Good Boy Points: " + self.config.member(ctx.author).GoodBoyPoints())
        else:
            await ctx.send(user.name + "'s Good Boy Points: " + self.config.member(user).GoodBoyPoints())

    @commands.command()
    async def cashPoints(self, ctx, points):
        """Cash in your good boy points"""
        yourPoints = self.config.member(ctx.author).GoodBoyPoints()
        if (points > yourPoints):
            await ctx.send("You only have " + yourPoints + " Good Boy Points... Collect or beg for some more!")
            return
        remainingPoints = yourPoints - points
        await self.config.member(ctx.author).GoodBoyPoints.set(remainingPoints)
        await ctx.send(ctx.author.name + " has redeemed " + points + " Good Boy Points! They have " + remainingPoints + " left.")