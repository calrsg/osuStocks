import discord
from discord.ext import commands
from discord import app_commands
from data.datamanager import *
from utils.paginator import PaginationView


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="profile", with_app_command=True, description="Return basic user information")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def profile(self, ctx, target: discord.Member = None):
        """
        :param ctx: Context
        :param target: An optional Discord user. If no user is passed, your profile is returned.
        :return: The profile of the message sender, or the passed target.
        """
        # Allow for optional user, otherwise use context
        if target is not None:
            user = getUser(target.id)
            userDisc = target
        else:
            user = getUser(ctx.author.id)
            userDisc = ctx.author

        holdings = getUserHoldings(user)
        holdingNo = 0
        holdingCount = 0
        holdingWorth = 0

        # Calculate number of holdings (could be an aggregate/count SQL query) + get value of holdings

        if holdings is not None:
            holdingNo = len(holdings)
            for entry in holdings.objects():
                holdingCount += entry.amount
                holdingWorth += entry.amount * entry.price

        profile_embed = discord.Embed(title=userDisc.name,
                                      description=f"Balance: {user.balance}\n"
                                                  f"Net worth: {holdingWorth}\n"
                                                  f"Total Holdings: {holdingCount}\n"
                                                  f"Total Stocks: {holdingNo}",
                                      color=int(0xdd6ce0))

        profile_embed.set_footer(text=f"⏰ {datetime.datetime.utcnow().strftime('%H:%M:%S')}")
        profile_embed.set_thumbnail(url=userDisc.display_avatar)

        await ctx.send(embed=profile_embed)

    @commands.hybrid_command(name="player", with_app_command=True, description="Return basic player information")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def player(self, ctx, playername: str):
        player = getPlayerWithName(playername)
        if player is not None:
            player_embed = discord.Embed(title=f"{player.playerName} - ${player.price}",
                                         description=f"GB #{player.rank} \n"
                                                     f"{player.country} #{player.rankCountry}\n"
                                                     f"{player.pp}pp, {player.accuracy}% acc")
            player_embed.set_thumbnail(url=f"https://a.ppy.sh/{player.playerID}")
            await ctx.send(embed=player_embed)
        else:
            await ctx.send("Player not found.")

    @commands.hybrid_command(name="players", with_app_command=True, description="Return all players.")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def players(self, ctx):
        players = getPlayers()
        if len(players) == 0:
            await ctx.send("No players found.")
            return
        output = []
        for entry in players:
            output.append({"label": f"{entry.playerName} | ${entry.price}",
                           "item": f"osu! ID: {entry.playerID}\n#{entry.rank}, #{entry.rankCountry} {entry.country} | {entry.pp}pp | {round(entry.accuracy, 2)}%"})
        pagination_view = PaginationView(timeout=None)
        pagination_view.title = "Players (Stocks)"
        pagination_view.data = output
        await pagination_view.send(ctx)

    @commands.hybrid_command(name="myholdings", with_app_command=True, description="Returns your holdings.")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def myholdings(self, ctx):
        user = getUser(ctx.author.id)
        holdings = getUserHoldings(user)
        print(holdings)
        if len(holdings) == 0:
            await ctx.send("No holdings found.")
            return
        output = []
        for entry in holdings:
            output.append({"label": f"{entry.playerName} | ${entry.price}",
                           "item": f"osu! ID: {entry.playerID}\n#{entry.rank}, #{entry.rankCountry} {entry.country} | {entry.pp}pp | {round(entry.accuracy, 2)}%"})

        pagination_view = PaginationView(timeout=None)
        pagination_view.title = f"{ctx.author.name}'s Holdings"
        pagination_view.data = output
        await pagination_view.send(ctx)

    @commands.hybrid_command(name="info", with_app_command=True, description="What is osu! Stocks?")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def info(self, ctx):

        embed = discord.Embed(title="osu! Stocks | Alpha 0",
                              description=f"**What is osu! Stocks?**\n"
                                          f"This project aims to create a virtual stock market on osu! players, "
                                          f"using fake currency to place buy and sell orders on 'stock' in top players.\n"
                                          f"osu! Stocks is currently in the early Alpha stages where not all features are complete. "
                                          f"Once the basic functionality is ready, a private beta will be launched to find bugs and "
                                          f"take on user feedback, after which the market will be reset for release.")

        await ctx.send(embed=embed)


async def setup(bot):
    # take name of class, pass in the bot
    await bot.add_cog(Profile(bot))
