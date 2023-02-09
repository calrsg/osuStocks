import discord
from discord.ext import commands
from discord import app_commands
import os
from data.datamanager import *
import data.osuapi
from utils.paginator import PaginationView


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.hybrid_command(name="load", with_app_command=True, description="Load a cog.")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def load(self, ctx, extension):
        # awful fix for errors with unknown filenames
        load_success = False
        for filename in os.listdir("./cogs"):
            if f"{extension}.py" == filename:
                await self.bot.load_extension(f"cogs.{extension}")
                await ctx.send(f"**{extension}** loaded successfully")
                load_success = True
        if not load_success:
            await ctx.send(f"**{extension}** has *not* been loaded, please check cog name.")

    @commands.is_owner()
    @commands.hybrid_command(name="unload", with_app_command=True, description="Unload a cog")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def unload(self, ctx, extension):
        # awful fix for errors with unknown filenames
        unload_success = False
        for filename in os.listdir("./cogs"):
            if f"{extension}.py" == filename:
                if filename == "admin.py":
                    await ctx.send(f"**admin** cannot be unloaded, only reloaded.")
                    return
                await self.bot.unload_extension(f"cogs.{extension}")
                await ctx.send(f"**{extension}** unloaded successfully")
                unload_success = True
        if not unload_success:
            await ctx.send(f"**{extension}** has *not* been unloaded, please check cog name.")

    @commands.is_owner()
    @commands.hybrid_command(name="reload", with_app_command=True, description="Reload a cog.")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def reload(self, ctx, extension):
        # awful fix for errors with unknown filenames
        reload_success = False
        for filename in os.listdir("./cogs"):
            if f"{extension}.py" == filename:
                await self.bot.unload_extension(f"cogs.{extension}")
                await self.bot.load_extension(f"cogs.{extension}")
                await ctx.send(f"**{extension}** reloaded successfully")
                reload_success = True
        if not reload_success:
            await ctx.send(f"**{extension}** has *not* been reloaded, please check cog name.")

    @commands.is_owner()
    @commands.hybrid_command(name="listcogs", with_app_command=True, description="List all cogs in the cogs folder.")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def listcogs(self, ctx):
        cogs = []
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                cogs.append(filename)
        await ctx.send(f"Found the following cogs: {str(cogs)[1:-1]}")

    @commands.is_owner()
    @commands.hybrid_command(name="addplayer", with_app_command=True, description="Add a player to the database")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def addplayer(self, ctx, playername: str):
        player = data.osuApi.getPlayer(playername)
        if player is not None:
            player = player[0]
            newp = addPlayer(playerID=int(player["user_id"]),
                   playerName=player["username"],
                   country=player["country"],
                   rank=int(player["pp_rank"]),
                   rankCountry=int(player["pp_country_rank"]),
                   pp=int(float(player["pp_raw"])),
                   accuracy=float(player["accuracy"]),
                   price=2)
            print(newp.playerName)
            await ctx.send(newp.playerName)

    @commands.is_owner()
    @commands.hybrid_command(name="transactions", with_app_command=True, description="[DEBUG] Return all transactions.")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def transactions(self, ctx):
        transactions = getTransactions()
        if len(transactions) == 0:
            await ctx.send("No transactions found.")
            return
        output = []
        count = 0
        for entry in transactions:
            if count < 100:
                output.append({"label": f"{entry.transactionID}",
                               "item": f"seller: {entry.sellerID} | buyer: {entry.buyerID}\n"
                                       f"listed: {entry.listTime} | sold: {entry.sellTime}\n"
                                       f"amount: {entry.amount} | price: {entry.price} | total: {entry.amount * entry.price}"})
                count += 1
        pagination_view = PaginationView(timeout=None)
        pagination_view.title = "[DEBUG] Transactions"
        pagination_view.data = output
        await pagination_view.send(ctx)

    @commands.is_owner()
    @commands.hybrid_command(name="holdings", with_app_command=True, description="[DEBUG] Return all holdings.")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def holdings(self, ctx):
        holdings = getHoldings()
        if len(holdings) == 0:
            await ctx.send("No holdings found.")
            return
        output = []
        count = 0
        for entry in holdings:
            if count < 100:
                output.append({"label": f"{entry.holdingID}",
                               "item": f"holder: {entry.userID}\n"
                                       f"player: {entry.playerID}\n"
                                       f"amount: {entry.amount}"})
                count += 1
        pagination_view = PaginationView(timeout=None)
        pagination_view.title = "[DEBUG] Holdings"
        pagination_view.data = output
        await pagination_view.send(ctx)


async def setup(bot):
    # take name of class, pass in the bot
    await bot.add_cog(Admin(bot))