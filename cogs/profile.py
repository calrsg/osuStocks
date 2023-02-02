import discord
from discord.ext import commands
from discord import app_commands
import datetime
from data.models import User, Player, Holding, Transaction


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="profile", with_app_command=True, description="Return basic user information")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def profile(self, ctx):
        self.bot.dbt.connect()
        user = User.get(User.userID == ctx.author.id)

        holdings = Holding.select().join(User).where(ctx.author.id == User.userID)

        holdingCount = 0

        for entry in holdings:
            holdingCount += int(entry.amount)

        profile_embed = discord.Embed(title=ctx.author.name,
                                      description=f"Balance: {user.balance}\n"
                                                  f"Total Holdings: {holdingCount}\n"
                                                  f"Total Stocks: {len(holdings)}",
                                      color=int(0xdd6ce0))

        profile_embed.set_footer(text=f"⏰ {datetime.datetime.utcnow().strftime('%H:%M:%S')}")
        profile_embed.set_thumbnail(url=ctx.author.display_avatar)

        await ctx.send(embed=profile_embed)
        self.bot.dbt.close()


async def setup(bot):
    # take name of class, pass in the bot
    await bot.add_cog(Profile(bot))
