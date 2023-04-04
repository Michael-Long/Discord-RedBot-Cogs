from redbot.core import Config
from redbot.core import commands

# Using Requests to query website for bingo board row count
import requests
# Using Random to generate random bingo codes
import random

class StreamBingo(commands.Cog):
    """Stream Bingo Cog - Connects to Website to generate Bingo Boards"""

    # Possible Bingo Board Win Configs
    bingos = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 30, 13, 14],
        [15, 16, 17, 18, 19],
        [20, 21, 22, 23, 24],
        [1, 6, 11, 15, 20],
        [2, 7, 12, 16, 21],
        [3, 8, 30, 17, 22],
        [4, 9, 13, 18, 23],
        [5, 10, 14, 19, 24],
        [1, 7, 30, 18, 24],
        [5, 9, 30, 16, 20]
    ]
    count = 0

    def __init__(self, bot):
        self.bot = bot

        # Query Bingo Database for Count
        countPayload = {'count': True}
        countRequest = requests.get('https://michaeldoescoding.net/projects/pokemon/nuzlockebingo/index.php', params=countPayload)
        self.count = 0
        if (countRequest.status_code != 200):
            print("Couldn't retrieve count information, setting count to 0")
        else:
            self.count = int(countRequest.text)

        # Establish Connection to Database
        self.config = Config.get_conf(self, identifier=7908234242)
        default_member = {
            "bingoCode": ""
        }

        self.config.register_member(**default_member)

    @commands.command()
    async def resetUserBingo(self, ctx, userID):
        isOwner = await ctx.bot.is_owner(ctx.author)
        if (not isOwner):
            await ctx.send("You need proper permissions to run this command")
            return

        try:
            int(userID)
        except:
            await ctx.send("The given userID isn't an int value: " + userID)
            return

        user = ctx.guild.get_member(int(userID))
        if (user == None):
            await ctx.send("No user found in this server with ID: " + userID)
            return
        
        await self.config.member(user).bingoCode.set("")
        await ctx.send("Bingo Code has been cleared from " + user.name)

    @commands.command()
    async def bingo(self, ctx):
        currCode = await self.config.member(ctx.author).bingoCode()
        if (len(currCode) == 0):
            while True:
                # generate new code and put it into the table
                pickedEntries = list()
                for index in range(24):
                    randEntry = random.randint(0, self.count - 1)
                    while pickedEntries.count(randEntry) > 0:
                        randEntry = random.randint(0, self.count - 1)
                    randEntryHex = hex(randEntry)[2:]
                    while len(randEntryHex) < 4:
                        randEntryHex = "0" + randEntryHex
                    currCode = currCode + randEntryHex
                    pickedEntries.append(randEntry)
                break
            await self.config.member(ctx.author).bingoCode.set(currCode)
        await ctx.send(ctx.author.mention + " Bingo Code: " + currCode + "\nYou can view your bingo board here: https://michaeldoescoding.net/projects/pokemon/nuzlockebingo/index.html")

    @commands.command()
    async def testBingo(self, ctx):
        await ctx.send("I can do stuff!")