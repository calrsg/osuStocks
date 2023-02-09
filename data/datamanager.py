import peewee
from peewee import *
from data.models import User, Player, Holding, Transaction, Listing, Order
import time, datetime


# FETCH ONE

def getUser(userID: int):
    """
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

    :param playerName: an int matching an osu! username.
    :return: A Player model object matching the ID, or None if not found.
    """
    try:
        return Player.get(Player.playerName == playerName)
    except Exception as e:
        print(e)
        return None


def addPlayer(playerID: int, playerName: str, country: str, rank: int, rankCountry: int, pp: int, accuracy: float, price: float):
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


def getHolding(holdingID: int):
    """

    :param holdingID: an int matching a holding ID.
    :return: A Holding model object matching the ID, or None if not found.
    """

    try:
        return Holding.get(Holding.holdingID == holdingID)
    except Exception as e:
        print(e)
        return None


def addHolding(holdingID: int, userID: int, playerID: int, amount: int):
    """
    :param holdingID: an int matching a holding ID.
    :param userID: an int matching a Discord user ID.
    :param playerID: an int matching an osu! player ID.
    :param amount: an int declaring how much of the stock is held.
    :return: A Holding model object that was created, or one that already exists.
    """

    result = getHolding(holdingID)
    if result is None:
        result = Holding.create(holdingID=holdingID,
                                userID=userID,
                                playerID=playerID,
                                amount=amount)
    return result


def getTransaction(transactionID: int):
    """

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
    :param listingID: an int matching a listing ID.
    :return: A Listing object including Player and User.
    """

    try:
        return (Listing.select()
                .join(Holding)
                .join_from(Holding, Player)
                .join_from(Holding, User)
                .where(Listing.listingID == listingID)
                .objects())
    except Exception as e:
        return None


def addListing(listingID: int, holdingID: int, amount: int, price: float, listTime: datetime):
    """
    :param listingID:
    :param holdingID:
    :param amount:
    :param price:
    :param listTime:
    :return:
    """

    result = getListing(listingID)

    if result is None:
        result = Listing.create(listingID=listingID,
                                holdingID=holdingID,
                                amount=amount,
                                price=price,
                                listTime=listTime)

    return result


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
                .join_from(Player)
                .join_from(Order, User)
                .order_by(Order.orderTime)
                .objects())
    except Exception as e:
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