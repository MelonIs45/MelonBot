import discord
import os
import json
import datetime
import sys
from discord.ext import commands, tasks

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
    
    @commands.command()
    @commands.is_owner()
    async def delete(self, ctx):
        count = 0
        filelist = [f for f in os.listdir("./colors") if f.endswith(".jpg")]
        for f in filelist:
            os.remove(os.path.join("./colors", f))
            count += 1
        await ctx.send(f"Deleted {count} images.")

    @commands.command()
    @commands.is_owner()
    async def send(self, ctx, message):
        client = self.client
        guild = client.get_guild(ctx.guild.id)
        message = ctx.message.content.split(" ", 1)[1]
        for channel in guild.text_channels:
            channel = client.get_channel(channel.id)
            await channel.send(message)

def setup(client):
    client.add_cog(Owner_commands(client))