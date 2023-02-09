from models import db, User, Player, Holding, Transaction, Listing
from data.osuapi import getPlayer
import datetime
# # Running peewee SQL queries on a one-time basis
#
# db.connect()
#
# db.drop_tables([User, Player, Holding, Transaction, Listing])
# db.create_tables([User, Player, Holding, Transaction, Listing])

# test = User.create(
#     userID=73389450113069056,
#     balance=1000)

# DEBUG/TEST DATASET
db.drop_tables([User, Player, Holding, Transaction, Listing])
db.create_tables([User, Player, Holding, Transaction, Listing])
# Create user: Gala
User.create(
    userID=73389450113069056,
    balance=374
)
# Create user: uyghti
User.create(
    userID=106225176907120640,
    balance=590
)
# Add player: mrekk
player = getPlayer("mrekk")
Player.create(playerID=int(player["user_id"]),
              playerName=player["username"],
              country=player["country"],
              rank=int(player["pp_rank"]),
              rankCountry=int(player["pp_country_rank"]),
              pp=int(float(player["pp_raw"])),
              accuracy=float(player["accuracy"]),
              price=28.88
)

# Add player: uyghti
player = getPlayer("uyghti")
Player.create(playerID=int(player["user_id"]),
              playerName=player["username"],
              country=player["country"],
              rank=int(player["pp_rank"]),
              rankCountry=int(player["pp_country_rank"]),
              pp=int(float(player["pp_raw"])),
              accuracy=float(player["accuracy"]),
              price=4.5
)

# Add player: Utami
player = getPlayer("Utami")
Player.create(playerID=int(player["user_id"]),
              playerName=player["username"],
              country=player["country"],
              rank=int(player["pp_rank"]),
              rankCountry=int(player["pp_country_rank"]),
              pp=int(float(player["pp_raw"])),
              accuracy=float(player["accuracy"]),
              price=15.36
)

# Add player: Dumii
player = getPlayer("Dumii")
Player.create(playerID=int(player["user_id"]),
              playerName=player["username"],
              country=player["country"],
              rank=int(player["pp_rank"]),
              rankCountry=int(player["pp_country_rank"]),
              pp=int(float(player["pp_raw"])),
              accuracy=float(player["accuracy"]),
              price=6.43
)

# Add holding: Gala holds mrekk
Holding.create(
    userID=73389450113069056,
    playerID=7562902,
    amount=5
)

# Add holding: Gala holds uyghti
Holding.create(
    userID=73389450113069056,
    playerID=7562902,
    amount=27
)

# Add holding: Gala holds Utami

Holding.create(
    userID=73389450113069056,
    playerID=7512553,
    amount=7
)

# Add holding: uyghti holds uyghti
Holding.create(
    userID=106225176907120640,
    playerID=3641404,
    amount=12
)

# Add listing: Gala sells mrekk
Listing.create(
    holdingID=1,
    amount=3,
    price=29,
    listTime=datetime.datetime.utcnow()
)

# Add listing: Gala sells Utami
t1 = datetime.datetime.utcnow()
Listing.create(
    holdingID=3,
    amount=2,
    price=16.5,
    listTime=t1
)

# Add fake Transaction: Gala sells Utami to uyghti
Transaction.create(
    sellerID=73389450113069056,
    buyerID=106225176907120640,
    playerID=7512553,
    listTime=t1,
    sellTime=datetime.datetime.utcnow(),
    amount=2,
    price=16.5
)



# test.save()

