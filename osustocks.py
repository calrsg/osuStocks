import discord
from discord.ext import commands
import os
import json


class OsuStocks(commands.Bot):
    intents = discord.Intents.default()

    bot = commands.Bot(command_prefix="!", intents=intents)

    def __init__(self):
        self.discord_bot_token = ""
        self.discord_command_prefixes = [""]
        self.load_config()

        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)

        owners = [73389450113069056]
        super().__init__(command_prefix=self.discord_command_prefixes, case_insensitive=True,
                         intents=discord.Intents.all(), owner_ids=set(owners), allowed_mentions=allowed_mentions)

    def load_config(self):
        with open("config.json") as file:
            contents = json.loads(file.read())

            self.discord_bot_token = contents['discord']['bot_token']
            self.discord_command_prefixes = contents['discord']['command_prefixes']

    @bot.event
    async def on_ready(self):
        print("Bot initialised.")
        await self.startup()
        await self.change_presence(activity=discord.Game(name=f"discord.gg/happy"))

    async def startup(self):
        print("Attempting to load cogs...")
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                # loads filename, removes last 3 characters (because load works with filename itself, not extension)
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"{filename} successfully loaded.")

        await self.tree.sync(guild=discord.Object(id=833991086740996117))

    @bot.event
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing argument.")
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("This command is for DM's only.")
        if isinstance(error, commands.NotOwner):
            await ctx.send("Bot author command only.")
        if isinstance(error, commands.UserNotFound):
            await ctx.send("Specified user not found.")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Specified member not found.")
        if isinstance(error, commands.MessageNotFound):
            await ctx.send("Specified message not found.")
        if isinstance(error, commands.ChannelNotFound):
            await ctx.send("Specified channel not found.")
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("You do not have the role required for this command.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission for this command")
        if isinstance(error, commands.BotMissingRole):
            await ctx.send("I do not have the role required for this command.")
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I do not have permission for this command")

    def run(self):
        super().run(self.discord_bot_token)


if __name__ == "__main__":
    maika = OsuStocks()
    maika.run()
