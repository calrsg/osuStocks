import discord
from discord.ext import commands
from discord import app_commands
from data import database, parsedata


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="me", with_app_command=True, description="Return user information such as balance, stock holdings, etc.")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def me(self, ctx):
        userData = await database.Users.getUser(ctx.author.id)
        userData = parsedata.Users.parseUser(userData)
        await ctx.send(userData["balance"])


async def setup(bot):
    # take name of class, pass in the bot
    await bot.add_cog(Profile(bot))
