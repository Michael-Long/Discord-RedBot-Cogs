from .GoodBoyPoints import GoodBoyPoints

async def setup(bot):
    await bot.add_cog(GoodBoyPoints(bot))