from redbot.core import checks, commands
from random import choice

import discord

class AskLeah(commands.Cog):
    """Ask Leah Cog - Ask Leah Anything!"""

    answers = [
        "Of course!",
        "Only if I get a treat",
        "Seriously? Fine...",
        "Let me ask Potato... He said sure",
        "Let me ask Potato... He said no way!",
        "It is certain",
        "Resounding yes!",
        "Are you sure about that?",
        "I wouldn’t advise that, but okay",
        "Do it, you won’t.",
        "Absolutely not!",
        "Sure, but don’t tell dad I said that >.>",
        "What would Benito do? Do that.",
        "No comment",
        "I don’t want to be held responsible for the outcome",
        "OMG YES",
        "The fuck did you just ask me?",
        "HELLLLLL NO",
        "Excuse me?",
        "Meow?",
        "I don't know, I'm just a lil bean",
        "As long as nobody gets hurt",
        "Commit the violence",
        "I don't see how food is involved.",
        "I must consult the sacred texts, ask again soon.",
        "I see this as an opportunity",
        ">:3 yes",
        ">:( no",
        "Bitch why are you asking me?",
        "*incoherent screaming*"
    ]

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def leah(self, ctx):
        """Ask Leah!"""
        await ctx.send("`" + choice(self.answers) + "`")


