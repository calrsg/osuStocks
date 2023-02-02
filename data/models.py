from peewee import *

db = MySQLDatabase("osustocks", host="localhost", user="root", password="impost3r")


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
    val = FloatField(null=False)


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
    amount = IntegerField(null=False)
    val = FloatField(null=False)
