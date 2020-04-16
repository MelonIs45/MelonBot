import discord
import os
import json
import datetime
from discord.ext import commands

cwd = os.path.dirname(__file__)
jsonPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
config = json.loads(open(jsonPath, "r").read())
rgb_scale = 255
cmyk_scale = 100

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

    def rgb_to_cmyk(self, r, g, b):
        if (r, g, b) == (0, 0, 0):
            return 0, 0, 0, cmyk_scale

        c = 1 - r / rgb_scale
        m = 1 - g / rgb_scale
        y = 1 - b / rgb_scale

        min_cmy = min(c, m, y)
        c = (c - min_cmy) / (1 - min_cmy)
        m = (m - min_cmy) / (1 - min_cmy)
        y = (y - min_cmy) / (1 - min_cmy)
        k = min_cmy

        return c * cmyk_scale, m * cmyk_scale, y * cmyk_scale, k * cmyk_scale

def setup(client):
    client.add_cog(Utils(client))
    