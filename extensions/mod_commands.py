import discord
import os
import json
import datetime
from discord.ext import commands

cwd = os.path.dirname(__file__)
jsonPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
config = json.loads(open(jsonPath, "r").read())
max_purge = 50

class Info_commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help = f"**`$purge [amount | Max is {max_purge}]`**",
    brief = "**Moderator Command:** Deletes the amount of messages specified.",
    usage = "**Usage: `$purge [amount | Max is 50]`**",
    description = "Deletes the amount of messages specified in the `[amount]` argument, requires the `Manage Messages` permission for the bot.\n\nExample: `$purge 25`"
    )
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount = None):
        if amount is None:
            await ctx.channel.send("Please enter a valid amount")
        elif int(amount) > max_purge:
            await ctx.channel.send(f"The maximum amount to purge is `{max_purge}`.")
        else:
            await ctx.channel.purge(limit = int(amount)+1)

def setup(client):
    client.add_cog(Info_commands(client))
    