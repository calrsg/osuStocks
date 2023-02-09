import discord
from discord.ext import commands
from discord import app_commands
from data.datamanager import *
from utils.paginator import PaginationView


class Marketplace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="market", with_app_command=True, description="Return active listings")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def market(self, ctx):
        listings = getListingDetails()
        if len(listings) == 0:
            await ctx.send("Market is currently empty")
            return
        output = []
        for entry in listings:
            output.append({"label": f"#{entry.listingID}",
                           "item": f"{entry.playerName} | ${entry.price} | {entry.amount}"})

        pagination_view = PaginationView(timeout=None)
        pagination_view.title = "Market"
        pagination_view.data = output
        await pagination_view.send(ctx)


async def setup(bot):
    # take name of class, pass in the bot
    await bot.add_cog(Marketplace(bot))