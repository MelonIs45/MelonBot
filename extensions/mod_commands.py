import discord
import os
import json
import datetime
from discord.ext import commands

cwd = os.path.dirname(__file__)
jsonPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
config = json.loads(open(jsonPath, "r").read())

class Info_commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount = None):
        if amount is None:
            await ctx.channel.send("Please enter a valid amount")
        elif int(amount) > 50:
            await ctx.channel.send("The maximum amount to purge is `50`.")
        else:
            await ctx.channel.purge(limit = int(amount)+1)

def setup(client):
    client.add_cog(Info_commands(client))
    