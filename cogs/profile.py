import discord
from discord.ext import commands
from discord import app_commands


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="me", with_app_command=True, description="Return user information such as balance, stock holdings, etc.")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def me(self, ctx):
        await ctx.send("Placeholder, will return user balance and stock holdings in a nice looking embed :)")


async def setup(bot):
    # take name of class, pass in the bot
    await bot.add_cog(Profile(bot))
