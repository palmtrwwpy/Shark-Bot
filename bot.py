import discord
import os
import json
import sqlite3
import aiohttp
from discord.ext import commands

COGS = [path.split(os.sep)[-1][:-3] for path in glob("./cogs/*.py")]

def load_config():
    """
    This Is to load the configs for the bot so people can customize it
    """
    with open("creds.json", "r") as cf:
        return json.load(cf)


creds = load_config()

class SharkBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=['.', '!', '?', '<', '>'], intents=discord.Intents.all(), case_sensitive=True)
        self.cxn = sqlite3.connect("sharkbot.db")
        self.c = self.cxn.cursor()
        self.token = creds['TOKEN']
        self.owner_id = creds['OWNER_ID']
        self.client_id = creds['CLIENT_ID']
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def on_ready(self):
        print('Logged in as:')
        print('Username: ' + self.user.name)
        print('ID: ' + str(self.user.id))
        print('------')
        self.c.execute("CREATE TABLE IF NOT EXISTS greetings(guildid integer PRIMARY KEY NOT NUll, welcomemsg text, leavemsg text)")
        self.cxn.commit()

        for cog in COGS:
            self.load_extension(f"cogs.{cog}")

    async def close(self):
        await super().close()
        await self.session.close()

    def run(self):
        super().run(self.token, reconnect=True)

if __name__ == "__main__":
    sharkbot = SharkBot()
    sharkbot.run()