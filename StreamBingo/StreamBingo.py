from redbot.core import commands

# Using APSW for SQLite Database Management - https://rogerbinns.github.io/apsw/example.html
import apsw
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
    database = NULL
    dbCursor = NULL

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
        self.database = apsw.Connection("data/db.sqlite")
        self.dbCursor = database.cursor()
        if (len(list(dbCursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bingo';"))) == 0):
            self.dbCursor.execute("CREATE TABLE 'bingo' ('ServerID' TEXT, 'UserID' TEXT, 'BingoCode' TEXT);")
        if (len(list(dbCursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adminRoles';"))) == 0):
            self.dbCursor.execute("CREATE TABLE 'adminRoles' ('ServerID' TEXT, 'AdminRoleID' TEXT);")
        if (len(list(dbCursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='flags';"))) == 0):
            self.dbCursor.execute("CREATE TABLE 'flags' ('ServerID' TEXT, 'JoinRoleID' TEXT, 'LoggingChannelID' TEXT, 'AllowBingo' INTEGER NOT NULL);")

    @commands.command()
    async def resetUserBingo(self, ctx):
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
        
        self.dbCursor.execute("delete from bingo where ServerID = ? and UserID = ?;", (ctx.guild.id, userID))
        await ctx.send("Bingo Code has been cleared from " + user.name)

    @commands.command()
    async def bingo(self, ctx):
        allowBingo = list(self.dbCursor.execute("select AllowBingo from flags where ServerID = ?;", (ctx.guild.id, )))
        if (len(allowBingo) > 0 and allowBingo[0][0] != 0):
            userEntry = list(self.dbCursor.execute("select BingoCode from bingo where ServerID = ? and UserID = ?;", (ctx.guild.id, ctx.author.id)))
            bingoCode = ""
            if (len(userEntry) == 0):
                while True:
                    # generate new code and put it into the table
                    pickedEntries = list()
                    for index in range(24):
                        randEntry = random.randint(0, count - 1)
                        while pickedEntries.count(randEntry) > 0:
                            randEntry = random.randint(0, count - 1)
                        randEntryHex = hex(randEntry)[2:]
                        while len(randEntryHex) < 4:
                            randEntryHex = "0" + randEntryHex
                        bingoCode = bingoCode + randEntryHex
                        pickedEntries.append(randEntry)
                    break
                self.dbCursor.execute("insert into bingo (ServerID, UserID, BingoCode) values (?, ?, ?);", (ctx.guild.id, ctx.author.id, bingoCode))
            else:
                bingoCode = userEntry[0][0]
            await ctx.send(ctx.author.mention + " Bingo Code: " + bingoCode + "\nYou can view your bingo board here: https://michaeldoescoding.net/projects/pokemon/nuzlockebingo/index.html")

    @commands.command()
    async def testBingo(self, ctx):
        await ctx.send("I can do stuff!")