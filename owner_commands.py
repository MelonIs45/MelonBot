import discord
import os
import json
import datetime
from discord.ext import commands

cwd = os.path.dirname(__file__)
jsonPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
config = json.loads(open(jsonPath, "r").read())

class Owner_commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, message):
        client = self.client

        status = ctx.message.content.split(" ", 1)[1]
        await client.change_presence(activity = discord.Game(str(status)))
        await ctx.send(f"Changed status to **`{status}`**.")

def setup(client):
    client.add_cog(Owner_commands(client))