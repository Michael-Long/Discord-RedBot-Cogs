from .AskLeah import AskLeah

async def setup(bot):
    await bot.add_cog(AskLeah(bot))