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

    @commands.hybrid_command(name="buyo", with_app_command=True, description="Place a buy order.")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def buyo(self, ctx, stock: str, amount: int, price: float):
        player = getPlayerWithName(stock)
        if player is None:
            await ctx.send(f"No stock found matching {stock}")
        # FIXME, potential problem, invalid Users is only handled by getUser creating a new User if none is found
        # CONT eg for below, could try to add userID directly without creating obj first
        # CONT best fix, add a getUser() call to all DataManager methods?
        user = getUser(ctx.author.id)
        MarketManager.addOrderToMarket(
            buyerID=user.userID,
            playerID=player.playerID,
            amount=amount,
            price=price)
        await ctx.send(f"Your buy order for {amount} {stock} @ {price} has been placed, with a total cost of {amount * price}.")

    @commands.hybrid_command(name="cancel", with_app_command=True, description="Cancel a buy order.")
    @app_commands.guilds(discord.Object(id=833991086740996117))
    async def cancel(self, ctx, orderid: int):
        # FIXME: At some point move all of this logic to a different class/method?
        user = getUser(ctx.author.id)
        order = getOrderDetailFromUser(orderid, ctx.author.id)
        if order is None:
            await ctx.send(f"No order found matching id {orderid}.")
            return
        if delOrder(orderid) is False:
            await ctx.send(f"Error deleting order matching id {orderid}.")
            return

        await ctx.send(f"Order {orderID} successfully cancelled.")


async def setup(bot):
    # take name of class, pass in the bot
    await bot.add_cog(Marketplace(bot))