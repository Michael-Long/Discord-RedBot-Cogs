from redbot.core import checks, commands, Config

import discord
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
    async def givePoints(self, ctx, friend: discord.Member, points: int):
        """Give points to a friend!"""
        if (friend.id == ctx.author.id):
            await ctx.send("You can't give yourself point, dingus.")
            return
        if (points < 0):
            who = "them"
            if (friend.id == ctx.bot.user.id):
                who = "me"
            await ctx.send("Why are you trying to give " + who + " negative points? :(")
            return
        elif (points == 0):
            await ctx.send("No points? what")
            return
        else:
            currPoints = await self.config.member(friend).GoodBoyPoints()
            await self.config.member(friend).GoodBoyPoints.set(currPoints + points)

            extraText = ""
            if (friend.id == ctx.bot.user.id):
                extraText = " Hey, thanks! :D"

            await ctx.send(ctx.author.display_name + " gave " + friend.display_name + " " + str(points) + " Good Boy Points!" + extraText)

    @commands.command()
    async def checkPoints(self, ctx, user: discord.Member = None):
        """Check your own or someone else's Good Boy Points"""
        if (user == None):
            points = await self.config.member(ctx.author).GoodBoyPoints()
            await ctx.send("Your Good Boy Points: " + str(points))
        else:
            points = await self.config.member(user).GoodBoyPoints()
            who = user.display_name + "'s"
            if (user.id == ctx.bot.user.id):
                who = "My"
            await ctx.send(who + " Good Boy Points: " + str(points))

    @commands.command()
    async def cashPoints(self, ctx, points: int):
        """Cash in your good boy points"""
        yourPoints = await self.config.member(ctx.author).GoodBoyPoints()
        if (points > yourPoints):
            await ctx.send("You only have " + str(yourPoints) + " Good Boy Points... Collect or beg for some more!")
            return
        remainingPoints = yourPoints - points
        await self.config.member(ctx.author).GoodBoyPoints.set(remainingPoints)
        await ctx.send(ctx.author.display_name + " has redeemed " + str(points) + " Good Boy Points! They have " + str(remainingPoints) + " left.")