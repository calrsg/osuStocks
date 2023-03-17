import peewee
from peewee import *
from data.models import User, Player, Holding, Transaction, Listing, Order
from utils.marketmanager import MarketManager, ProcessTransactions
import time, datetime


# FETCH ONE

def getUser(userID: int):
    """
    Returns a User model object matching the passed Discord user ID. Will create an entry to return if none is found.
    :param userID: An integer matching a Discord user ID.
    :return: A User model object matching the stored data for the Discord user.
    """
    try:
        return User.get(User.userID == userID)
    # FIXME Really dirty disgusting ugly ewwww scum ass lookin ass fix
    except Exception as e:
        print(e)
        user = User.create(
            userID=userID,
            balance=0)
        return user


def getPlayerWithID(playerID: int):
    """
    Return a Player model object from an osu! user ID.
    :param playerID: an int matching an osu! user ID.
    :return: A Player model object matching the ID, or None if not found.
    """
    try:
        return Player.get(Player.playerID == playerID)
    except Exception as e:
        print(e)
        return None


def getPlayerWithName(playerName: str):
    """
    Return a Player model object from an osu! username.
    :param playerName: an int matching an osu! username.
    :return: A Player model object matching the ID, or None if not found.
    """
    try:
        return Player.get(Player.playerName == playerName)
    except Exception as e:
        print(e)
        return None


def addPlayer(playerID: int, playerName: str, country: str, rank: int, rankCountry: int, pp: int, accuracy: float, price: float):
    """
    Returns a newly created Player model object, or returns an already existing match.
    :param playerID: An int matching an osu! user ID.
    :param playerName: A string matching an osu! username
    :param country: A string matching an osu! country code.
    :param rank: An int representing the players rank.
    :param rankCountry: An int representing the players country rank
    :param pp: An int representing the players pp.
    :param accuracy: A float representing the players accuracy
    :param price: A float representing the price of the player in the market.
    :return: The Player model object, or an already existing match.
    """
    player = getPlayerWithID(playerID)
    if player is None:
        player = Player.create(playerID=playerID,
                               playerName=playerName,
                               country=country,
                               rank=rank,
                               rankCountry=rankCountry,
                               pp=pp,
                               accuracy=accuracy,
                               price=price)

    return player


def updatePlayer(osuPlayer: dict):
    """
    Updates an osu! player with new osu!api information
    :param osuPlayer: A Player model object.
    :return: The updated Player model object, or None if no matching player to update was found.
    """
    player = getPlayerWithID(int(osuPlayer["user_id"]))
    if player is None:
        return

    player.playerName = osuPlayer["username"]
    player.country = osuPlayer["country"]
    player.rank = osuPlayer["pp_rank"]
    player.rankCountry = int(osuPlayer["pp_country_rank"])
    player.pp = int(float(osuPlayer["pp_raw"]))
    player.accuracy = float(osuPlayer["accuracy"])
    player.save()
    return player


def getHolding(holdingID: int):
    """
    Returns a Holding model object matching the holding ID.
    :param holdingID: an int matching a holding ID.
    :return: A Holding model object matching the ID, or None if not found.
    """

    try:
        return Holding.get(Holding.holdingID == holdingID)
    except Exception as e:
        print(e)
        return None


def addHolding(userID: int, playerID: int, amount: int):
    """
    Returns a newly created Holding model object.
    :param userID: an int matching a Discord user ID.
    :param playerID: an int matching an osu! player ID.
    :param amount: an int declaring how much of the stock is held.
    :return: A Holding model object that was created, or one that already exists.
    """

    return Holding.create(
        userID=userID,
        playerID=playerID,
        amount=amount)


def getTransaction(transactionID: int):
    """
    Returns a Transaction model object matching the transaction ID.
    :param transactionID: an int matching a transaction ID.
    :return: A Transaction model object matching the ID, or None if not found.
    """

    try:
        return Transaction.get(Transaction.transactionID == transactionID)
    except Exception as e:
        print(e)
        return None


def addTransaction(sellerID: int, buyerID: int, playerID: int,
                   listTime: datetime, sellTime: datetime, amount: int, price: float):
    """
    Returns the newly created Transaction model object.
    :param sellerID: An int matching a userID
    :param buyerID: An int matching a userID
    :param playerID: An int matching an osu! player ID
    :param listTime: A datetime when the listing was made
    :param sellTime: A datetime when the transaction was made
    :param amount: The amount of stock sold
    :param price: The price paid for each stock
    :return: The created Transaction
    """

    return Transaction.create(sellerID=sellerID,
                              buyerID=buyerID,
                              playerID=playerID,
                              listTime=listTime,
                              sellTime=sellTime,
                              amount=amount,
                              price=price)


def getListing(listingID: int):
    """
    Returns a Listing model object matching the listing ID.
    :param listingID: an int matching a listing ID.
    :return: A Transaction model object matching the ID, or None if not found.
    """

    try:
        return Listing.get(Listing.listingID == listingID)
    except Exception as e:
        print(e)
        return None


def getListingDetail(listingID: int):
    """
    Returns a Listing model object including the Holding, Player, and User tables, matching the listing ID.
    :param listingID: an int matching a listing ID.
    :return: A Listing object including Player and User, or None if no match is found.
    """

    try:
        return (Listing.select(Listing, Holding, Player, User)
                .join(Holding)
                .join_from(Holding, Player)
                .join_from(Holding, User)
                .where(Listing.listingID == listingID)
                .objects()
                .get())
    except Exception as e:
        print(e)
        return None


def addListing(holdingID: int, amount: int, price: float):
    """
    Returns the newly created Listing model object.
    :param holdingID:
    :param amount:
    :param price:
    :return:
    """

    return Listing.create(
        holdingID=holdingID,
        amount=amount,
        price=price,
        listTime=datetime.datetime.utcnow())


def getOrder(orderID: int):
    """
    Returns an Order model object matching the order ID.
    :param orderID: an int matching an order ID.
    :return: An Order model object matching the order ID, or None if no match is found.
    """

    try:
        return Order.get(Order.orderID == orderID)
    except Exception as e:
        return None


def getOrderDetail(orderID: int):
    """
    Return an Order model object including Player and User tables.
    :param orderID: an int matching an order ID.
    :return: An Order object including Player and User, or None if no match is found.
    """

    try:
        return (Order.select()
                .join(User)
                .join_from(Order, Player)
                .where(orderID == Order.orderID)
                .objects())
    except Exception as e:
        return None


def getOrderDetailFromUser(orderID: int, userID: int):
    """
    Return an Order model object including Player and User tables.
    :param orderID: an int matching an order ID.
    :param userID: an int matching a User ID.
    :return: An Order object including Player and User, or None if no match is found.
    """

    try:
        return (Order.select()
                .join(User)
                .join_from(Order, Player)
                .where(orderID == Order.orderID and userID == User.userID)
                .get())
    except Exception as e:
        return None


def addOrder(buyerID: int, playerID: int, amount: int, price: float):
    """
    Returns the newly created Order object.
    :param buyerID:
    :param playerID:
    :param amount:
    :param price:
    :return:
    """
    return Order.create(
        buyerID=buyerID,
        playerID=playerID,
        orderTime=datetime.datetime.utcnow(),
        amount=amount,
        price=price
    )


def delOrder(orderID: int):
    """
    Delete an order matching an orderID.
    :param orderID: An int matching an orderID.
    :return: True if deleted, False if an error occured.
    """
    try:
        order = getOrder(orderID)
        order.delete_instance()
        return True
    except Exception as e:
        print(e)
        return False

# FETCH ALL


def getUsers():
    """
    :return: A list of all stored users as User model objects
    """
    return User.select()


def getPlayers():
    """
    :return: A list of all stored players as Player model objects
    """
    return Player.select().order_by(Player.rank)


def getHoldings():
    """
    :return: A list of all stored Holdings as Holding model objects // This will be very very large, be careful
    """
    return Holding.select()


def getTransactions():
    """
    :return: A list of all stored Transactions as Transaction model objects // This will be fucking massive, do not use outside of debug or mass data editing.
    """
    return Transaction.select().order_by(Transaction.sellTime)


def getListings():
    """
    :return: A list of all active Listings as Listing model objects
    """
    return Listing.select()


def getOrders():
    """
    :return: A list of all active Orders as Order model objects.
    """
    return Order.select()


def getUserHoldings(user: User):
    """
    :param user: a User model object.
    :return: A table consisting of all Holding objects corresponding to the User passed in, and the val of the joined Player. Returns None if no Holdings found.
    """
    try:
        print(user.userID)
        return (Holding.select(Holding, User, Player)
                .join(User)
                .join_from(Holding, Player)
                .where(user.userID == User.userID)
                .objects())
    except Exception as e:
        return None


def getUserTransactions(user: User):
    """
    :param user: a User model object.
    :return: A table consisting of all Transaction objects corresponding to the User passed in.
    """
    return (Transaction.select()
            .where(Transaction.buyerID == user.userID or Transaction.sellerID == user.userID))


def getUserSaleTransactions(user: User):
    """
    :param user: a User model object.
    :return: A table consisting of Transaction objects where the passed user was the seller.
    """
    return (Transaction.select()
            .where(Transaction.sellerID == user.userID))


def getUserBuyerTransactions(user: User):
    """
    :param user: a User model object.
    :return: A table consisting of Transaction objects where the passed user was the buyer.
    """
    return (Transaction.select()
            .where(Transaction.buyerID == user.userID))


def getPlayerListings(player: Player):
    """
    :param player: A Player model object
    :return: A table consisting of Listings for a specific Player.
    """
    try:
        return (Listing.select()
                .join(Holding)
                .join(Player)
                .where(Player.playerID == player.playerID))
    except Exception as e:
        return None


def getListingDetails():
    """
    :return: A Listing object including Player and User, or None if no Listings are found.
    """

    try:
        return (Listing.select(Listing, Holding, Player, User)
                .join(Holding)
                .join_from(Holding, Player)
                .join_from(Holding, User)
                .order_by(Player.rank)
                .objects())
    except Exception as e:
        return None


def getListingsByPlayer(player: Player):
    """
    :param player: A Player model object.
    :return: A Listing object including Player and User, or None if no Listings are found.
    """

    try:
        return (Listing.select(Listing, Holding, Player, User)
                .join(Holding)
                .join_from(Holding, Player)
                .join_from(Holding, User)
                .where(Player.playerID == player.playerID)
                .order_by(Player.rank)
                .objects())
    except Exception as e:
        return None


def getOrderDetails(orderID):
    """
    :param orderID: an int matching an order ID.
    :return: An Order object including Player and User, or None if no Orders are found.
    """

    try:
        return (Order.select(Order, Player, User)
                .join(Player)
                .join_from(Order, User)
                .order_by(Order.orderTime)
                .objects())
    except Exception as e:
        return None


def getOrdersByUser(user: User):
    """
    :param user: A User model object.
    :return: An Order object including Player and User, or None if no Orders are found.
    """

    try:
        return (Order.select(Order, Player, User)
                .join(Player)
                .join_from(Order, User)
                .where(User.userID == user.userID)
                .order_by(Order.orderTime)
                .objects())
    except Exception as e:
        print(e)
        return None


def getOrdersByPlayer(player: Player):
    """
    :param player: A Player model object.
    :return: An Order object including Player and User, or None if no Orders are found.
    """

    try:
        return (Order.select(Order, Player, User)
                .join_from(Player)
                .join_from(Order, User)
                .where(Player.playerID == player.playerID)
                .order_by(Order.orderTime)
                .objects())
    except Exception as e:
        return None