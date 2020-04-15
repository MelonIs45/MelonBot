import discord
import os
import json
import datetime
from discord.ext import commands

cwd = os.path.dirname(__file__)
jsonPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
config = json.loads(open(jsonPath, "r").read())

class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_member(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.guild.get_member(ctx.author.id)
        else:
            pass
        return member

    def create_embed(self, ctx, embed, member : discord.Member = None):
        embed.color = ctx.author.colour
        embed.set_author(name = member)
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url_as(format='png'))
        embed.timestamp = datetime.datetime.utcnow()

def setup(client):
    client.add_cog(Utils(client))
    