
class Users:

    @staticmethod
    def parseUser(data):
        return {"userID": data[0],
                "balance": data[1]}


class Players:

    @staticmethod
    def parsePlayer(data):
        return {"playerID": data[0],
                "player_name": data[1],
                "country": data[2],
                "rank": data[3],
                "rank_country": data[4],
                "pp": data[5],
                "accuracy": data[6],
                "val": data[7]}


class Holdings:

    @staticmethod
    def parseHolding(data):
        return {"holdingID": data[0],
                "userID": data[1],
                "stockID": data[2],
                "amount": data[3]}
