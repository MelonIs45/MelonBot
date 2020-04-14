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

    def create_embed(self, ctx, embed):
        member = ctx.guild.get_member(ctx.author.id)
        embed.set_author(name = member)
        embed.set_footer(text = f"Requested by {member}", icon_url = member.avatar_url_as(format='png'))
        embed.timestamp = datetime.datetime.utcnow()

        #return embed


def setup(client):
    client.add_cog(Utils(client))