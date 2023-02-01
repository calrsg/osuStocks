from data import osuApi
import discord
from discord.ext import commands
from discord import app_commands


class PlayerInteraction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="who", with_app_command=True, description="Return information on an osu! player.")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def who(self, ctx, playername):
        await ctx.send(str(osuApi.getPlayer(playername)))




async def setup(bot):
    # take name of class, pass in the bot
    await bot.add_cog(PlayerInteraction(bot))
