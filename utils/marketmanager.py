import sys
import time, datetime

from data.models import *
import data.datamanager


class MarketManager:


    @staticmethod
    def addListingToMarket(holdingID: int, amount: int, price: float):
        listing = data.datamanager.addListing(
            holdingID=holdingID,
            amount=amount,
            price=price,
        )
        # Since this is a new listing, check for price updates on the Player.
        holding = data.datamanager.getHolding(holdingID)
        player = data.datamanager.getPlayerWithID(holding.playerID)
        MarketManager.updatePrice(player)

        return MarketManager.matchListing(listing)

    @staticmethod
    def addOrderToMarket(buyerID: int, playerID: int, amount: int, price: float):
        order = data.datamanager.addOrder(
            buyerID=buyerID,
            playerID=playerID,
            amount=amount,
            price=price)
        return MarketManager.matchOrder(order)

    @staticmethod
    def updatePrice(stock: Player):
        """
        Update the price of a Player model to match the lowest current listing.
        :param stock:
        :return: The updated Player model after being saved, or None if no listings were found.
        """
        # Get Listings for specific Player
        listings = data.datamanager.getPlayerListings(stock)
        if listings is None:
            return None
        lowestPrice = sys.float_info.max

        # Iterate over listings, find lowest price
        for entry in listings:
            if entry.price < lowestPrice:
                lowestPrice = entry.price

        stock.price = lowestPrice
        stock.save()
        return stock

    @staticmethod
    def matchListing(listing: Listing):
        """
        Takes in a Listing Model object and searches all buy orders to find matches.
        :param listing: The newly created Listing model object.
        :return: True if any matches were found, False if none were found.
        """
        # Get all Orders for the Player in the passed Listing
        try:
            holding = data.datamanager.getHolding(listing.holdingID)
            player = data.datamanager.getPlayerWithID(holding.playerID)
            orders = data.datamanager.getOrdersByPlayer(player)
        except Exception as e:
            return False
        # If returned statement is empty
        if orders is None:
            return False

        # Find price matches
        match = False
        for entry in orders:
            if entry.price >= listing.price:
                match = True
                ProcessTransactions.processSale(entry, listing)
                if listing.amount == 0:
                    # Listing has been sold out
                    # probably best for a method to make sale, create transaction, and delete listing and/or order
                    return True

        return match

    @staticmethod
    def matchOrder(order: Order):
        """
        Takes in a Order Model object and searches all listings to find matches.
        :param order: The newly created Listing model object.
        :return: True if any matches were found, False if none were found.
        """
        # Get all Listings for the Player in the passed Order
        try:
            player = data.datamanager.getPlayerWithID(order.playerID)
            listings = data.datamanager.getListingsByPlayer(player)
        except Exception as e:
            return False
        if listings is None:
            return False

        # Find price matches
        match = False
        for entry in listings:
            if entry.price >= order.price:
                match = True
                ProcessTransactions.processSale(order, entry)
                if order.amount == 0:
                    # Order has been filled.
                    # probably best for a method to make sale, create transaction, and delete order and/or listing
                    return True

        return match


class ProcessTransactions:

    @staticmethod
    def processSale(order: Order, listing: Listing):
        """
        Process a sale between an Order and a Listing.
        :order: An Order object that can purchase the passed Listing.
        :listing: A Listing object to be bought by the passed Order.
        :return: Created Transaction if successful, None if sale could not be processed.
        """
        # This method assumes the Order CAN purchase from the Listing.

        buyer = data.datamanager.getUser(order.buyerID)
        # Should never fail, Listing cannot exist without stock being Held
        seller = data.datamanager.getUser(data.datamanager.getHolding(listing.holdingID).userID)

        # Find if order buys out listing or listing fills order
        if order.amount > listing.amount:
            if buyer.balance < listing.amount * listing.price:
                # Buyer is a broke bitch and can't fill their order
                # Potentially cancel the order here too since they have order(s) they cannot afford?
                return None

            # Create transaction in if/else, creating before could make a dud Transaction if the above returns None
            transaction = ProcessTransactions.createTransaction(order, listing, listing.amount)

            # Update buyer/seller balance by: Amount sold * price sold at
            seller.balance += (listing.amount * listing.price)
            buyer.balance -= (listing.amount * listing.price)

            # Update listing/order amounts
            order.amount -= listing.amount
            listing.amount = 0

            # Remove Listing as it was cleared out.
            ProcessTransactions.cleanSale(listing)

        elif order.amount < listing.amount:
            if buyer.balance < order.amount * listing.price:
                # Buyer is a broke bitch and can't fill their order
                # Potentially cancel the order here too since they have order(s) they cannot afford?
                return None

            # Create transaction in if/else, creating before could make a dud Transaction if the above returns None
            transaction = ProcessTransactions.createTransaction(order, listing, order.amount)

            # Update buyer/seller balance by: Amount sold * price sold at
            seller.balance += (order.amount * listing.price)
            buyer.balance -= (order.amount * listing.price)

            # Update listing/order amounts
            listing.amount -= order.amount
            order.amount = 0

            # Remove Order as it was cleared out.
            ProcessTransactions.cleanSale(order)

        else:
            # Both are equal
            if buyer.balance < order.amount * listing.price:
                # Buyer is a broke bitch and can't fill their order
                # Potentially cancel the order here too since they have order(s) they cannot afford?
                return None

            # Create transaction in if/else, creating before could make a dud Transaction if the above returns None
            transaction = ProcessTransactions.createTransaction(order, listing, order.amount)

            # Update buyer/seller balance by: Amount sold * price sold at
            seller.balance += (order.amount * listing.price)
            buyer.balance -= (order.amount * listing.price)

            # Update listing/order amounts
            listing.amount = 0
            order.amount = 0

            # Remove Order and Listing as both were cleared out.
            ProcessTransactions.cleanSale(order)
            ProcessTransactions.cleanSale(listing)

        # As sale has been made, update the price of the sold Player
        MarketManager.updatePrice(data.datamanager.getPlayerWithID(transaction.playerID))
        return transaction

    @staticmethod
    def createTransaction(order: Order, listing: Listing, amount):
        """
        Create a Transaction based on a passed Order, Listing, and pre-calculated amount and price.
        :return: The created Transaction model object.
        """
        listing = data.datamanager.getListingDetail(listing.listingID)
        return data.datamanager.addTransaction(
            sellerID=listing.userID,
            buyerID=order.buyerID,
            playerID=order.playerID,
            listTime=listing.listTime,
            sellTime=datetime.datetime.utcnow(),
            amount=amount,
            price=listing.price)

    @staticmethod
    def cleanSale(item: Order or Listing):
        """
        Remove any Listing(s) or Order(s) after sales have been processed.
        :return: True if successful, False if any errors occur.
        """
        # Try except to be safe, idk how peewee .delete() works too well
        try:
            item.delete()
            return True
        except Exception as e:
            return False
