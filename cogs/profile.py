import discord
from discord.ext import commands
from discord import app_commands
from data.datamanager import *


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="profile", with_app_command=True, description="Return basic user information")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def profile(self, ctx):
        user = getUser(ctx.author.id)

        holdings = getUserHoldings(user)
        holdingNo = 0
        holdingCount = 0
        holdingWorth = 0

        # Calculate number of holdings (could be an aggregate/count SQL query) + get value of holdings
        print(holdings)

        if holdings is not None:
            holdingNo = len(holdings)
            for entry in holdings.objects():
                holdingCount += entry.amount
                holdingWorth += entry.amount * entry.val

        profile_embed = discord.Embed(title=ctx.author.name,
                                      description=f"Balance: {user.balance}\n"
                                                  f"Net worth: {holdingWorth}\n"
                                                  f"Total Holdings: {holdingCount}\n"
                                                  f"Total Stocks: {holdingNo}",
                                      color=int(0xdd6ce0))

        profile_embed.set_footer(text=f"⏰ {datetime.datetime.utcnow().strftime('%H:%M:%S')}")
        profile_embed.set_thumbnail(url=ctx.author.display_avatar)

        await ctx.send(embed=profile_embed)

    @commands.hybrid_command(name="player", with_app_command=True, description="Return basic player information")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def player(self, ctx, playername: str):
        player = getPlayerWithName(playername)
        if player is not None:
            player_embed = discord.Embed(title=f"{player.playerName} - ${player.price}",
                                         description=f"GLOBAL #{player.rank} \n"
                                                     f"{player.country} #{player.rankCountry}\n"
                                                     f"{player.pp}pp, {player.accuracy}% acc")
            player_embed.set_thumbnail(url=f"https://a.ppy.sh/{player.playerID}")
            await ctx.send(embed=player_embed)
        else:
            await ctx.send("Player not found.")


async def setup(bot):
    # take name of class, pass in the bot
    await bot.add_cog(Profile(bot))

