from peewee import *
import json

with open("./config.json") as file:
    contents = json.loads(file.read())

db = MySQLDatabase(contents["database"]["database"], host=contents["database"]["host"], user=contents["database"]["user"], password=contents["database"]["password"])


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    userID = BigIntegerField(primary_key=True, unique=True, null=False)
    balance = IntegerField(null=False)


class Player(BaseModel):
    playerID = IntegerField(primary_key=True, unique=True, null=False)
    playerName = CharField(null=False)
    country = CharField(null=False)
    rank = IntegerField(null=False)
    rankCountry = IntegerField(null=False)
    pp = IntegerField(null=False)
    accuracy = FloatField(null=False)
    price = FloatField(null=False)


class Holding(BaseModel):
    holdingID = AutoField(primary_key=True, unique=True, null=False)
    userID = ForeignKeyField(User, to_field='userID', backref='holdings', null=False)
    playerID = ForeignKeyField(Player, to_field='playerID', backref='holdings', null=False)
    amount = IntegerField(null=False)


class Transaction(BaseModel):
    transactionID = AutoField(primary_key=True, unique=True, null=False)
    sellerID = ForeignKeyField(User, to_field='userID', backref='transactions', null=False)
    buyerID = ForeignKeyField(User, to_field='userID', backref='transactions', null=False)
    playerID = ForeignKeyField(Player, to_field='playerID', backref='transactions', null=False)
    listTime = DateTimeField(null=False)
    sellTime = DateTimeField(null=False)
    amount = IntegerField(null=False)
    price = FloatField(null=False)


class Listing(BaseModel):
    listingID = AutoField(primary_key=True, unique=True, null=False)
    holdingID = ForeignKeyField(Holding, to_field='holdingID', backref='listings', null=False)
    amount = IntegerField(null=False)
    price = FloatField(null=False)
    listTime = DateTimeField(null=False)

