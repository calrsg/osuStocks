import peewee
from peewee import *
from data.models import User, Player, Holding, Transaction
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


def getUserHoldings(user: User):
    """
    :param user: a User model object.
    :return: A table consisting of all Holding objects corresponding to the User passed in, and the val of the joined Player. Returns None if no Holdings found.
    """
    try:
        return (Holding.select(Holding.amount, Player.val)
                .join(User)
                .join_from(Holding, Player)
                .where(user.userID == User.userID))
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
    return Player.select()


def getHoldings():
    """
    :return: A list of all stored Holdings as Holding model objects // This will be very very large, be careful
    """
    return Holding.select()


def getTransactions():
    """
    :return: A list of all stored Transactions as Transaction model objects // This will be fucking massive, do not use outside of debug or mass data editing.
    """
    return Transaction.select()


