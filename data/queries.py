from models import db, User, Player, Holding, Transaction
# Running peewee SQL queries on a one-time basis

db.connect()

# test = User.create(
#     userID=73389450113069056,
#     balance=1000)


# test.save()