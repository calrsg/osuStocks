BOT = None


def setBot(bot):
    global BOT
    BOT = bot


class Users:
    # TABLE: users
    # columns: userID (PK, bigint), balance(int)

    @staticmethod
    async def getUser(userID: int):
        try:
            async with await BOT.db.acquire() as conn:
                async with await conn.cursor() as cur:
                    await cur.execute(f"SELECT * FROM users WHERE userID={userID}")
                    data = await cur.fetchone()
                    await cur.close()
                    return data
        except Exception as e:
            print(e)
            return None

    @staticmethod
    async def addUser(userID: int):
        try:
            async with await BOT.db.acquire() as conn:
                async with await conn.cursor() as cur:
                    await cur.execute(f"INSERT INTO users (userID, balance) VALUES (%s, %s)",
                                      (userID, 0))
                    await cur.close()
                    return True
        except Exception as e:
            print(e)
            return False


class Players:
    # TABLE: players
    # COLUMNS: playerID(PK, int, osu! ID), player_name(str), country(str), rank(int), rank_country(int), pp(int), accuracy(float), val(double)

    @staticmethod
    async def getPlayer(playerName: str):
        try:
            async with await BOT.db.acquire() as conn:
                async with await conn.cursor() as cur:
                    await cur.execute(f"SELECT * FROM players WHERE player_name={playerName}")
                    data = await cur.fetchone()
                    await cur.close()
                    return data
        except Exception as e:
            print(e)
            return None

    @staticmethod
    async def addPlayer(playerID: int, playerName: str, country: str, rank: int, rank_country: int, pp: int, accuracy: float, val: float):
        try:
            async with await BOT.db.acquire() as conn:
                async with await conn.cursor() as cur:
                    await cur.execute(f"INSERT INTO players (playerID, player_name, country, rank, rank_country, pp, accuracy, val) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                      (playerID, playerName, country, rank, rank_country, pp, accuracy, val))
                    await cur.close()
                    return True
        except Exception as e:
            print(e)
            return False


class Holdings:

    @staticmethod
    async def getHolding(userID: int):
        try:
            async with await BOT.db.acquire() as conn:
                async with await conn.cursor() as cur:
                    await cur.execute(f"SELECT * FROM holdings WHERE userID={userID}")
                    data = await cur.fetchall()
                    await cur.close()
                    return data
        except Exception as e:
            print(e)
            return None

    @staticmethod
    async def addHolding(userID: int, playerID: int, amount: int):
        try:
            async with await BOT.db.acquire() as conn:
                async with await conn.cursor() as cur:
                    await cur.execute(f"INSERT INTO holdings (userID, stockID, amount) VALUES (%s, %s, %s)",
                                      (userID, playerID, amount))
                    await cur.close()
                    return True
        except Exception as e:
            print(e)
            return False
