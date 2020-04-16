import discord
import os
import json
import datetime
import random
import PIL
import webcolors
import colorsys
from discord.ext import commands
from PIL import Image
from random import randint

cwd = os.path.dirname(__file__)
jsonPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
config = json.loads(open(jsonPath, "r").read())

class Fun_commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(help = "**`$avatar <user>`**",
    brief = "Shows the requested user avatar.",
    usage = "**Usage: `$avatar <user>`**",
    description = "Returns the user specified avatar, the `<user>` argument does not have to be specified and will return with the message authors avatar instead.\n\nExample: `$avatar <@MelonBot#0396`"
    )
    async def avatar(self, ctx, member : discord.Member = None):
        utils = self.client.get_cog("Utils")
        client = self.client
        if ctx.author == client.user:
            return

        if member is None:
            member = ctx.guild.get_member(ctx.author.id)

            try:
                uAvatar = member.avatar_url_as(format='gif', size=256)
            except discord.errors.InvalidArgument:
                uAvatar = member.avatar_url_as(format='png', size=256)
        else:
            try:
                uAvatar = member.avatar_url_as(format='gif', size=256)
            except discord.errors.InvalidArgument:
                uAvatar = member.avatar_url_as(format='png', size=256)

        embed = discord.Embed()
        utils.get_member(ctx, member)
        utils.create_embed(ctx, embed, member)
        embed.url = str(uAvatar)
        embed.title = "Avatar URL"
        embed.set_image(url = uAvatar)

        await ctx.send(embed = embed) 

    @commands.command(help = "**`$someone [message]`**",
    brief = "Sends a message to a random person in the server.",
    usage = "**Usage: `$someone [message]`**",
    description = "Sends the message specified in the `<message>` argument to a random person in the server, argument of `<message>` has to be given.\n\nExample: `$someone lmao get cucked retard`"
    )
    async def someone(self, ctx):
        client = self.client
        if ctx.author == client.user:
            return

        memberList = []
        for member in ctx.guild.members:
            if member.bot is True:
                pass
            else:
                memberList.append(member.id)

        memberId = random.choice(memberList)
        memberName = ctx.author.display_name
        msgContent = ctx.message.content.split(" ", 1)

        msg = str(memberName) + ": <@" + str(memberId) + "> " + str(msgContent[1])
        await ctx.send(msg)

    @commands.command(help = "**`$color [hex | rgb]`**",
    brief = "Returns an image of the requested color.",
    usage = "**Usage: `$color [hex | rgb]`**",
    description = "Returns an image of the color specified in the `[hex | rgb]` parameter, also returns other information on the color.\n\nExample: `$color 128 44 188`",
    aliases = ["colour"]
    )
    async def color(self, ctx, code):
        utils = self.client.get_cog("Utils")
        code  = ctx.message.content.split(" ", 1)[1]
        embed = discord.Embed()
        member = None
        utils.get_member(ctx, member)
        utils.create_embed(ctx, embed, member)

        if code.startswith("rgb") or " " in code:
            code = code.lstrip("rgb(").rstrip(")").replace(",", " ").split(" ")
            code = list(filter(None, code))
            code = f"{code[0]}, {code[1]}, {code[2]}"
            rgb = tuple(map(int, code.split(', ')))  
        else:
            if not code.startswith("#"):
                code = f"#{code}"
            rgb = webcolors.hex_to_rgb(code)
            rgb = str(rgb).rstrip(")").split("(")[1].split(", ")
            red, green, blue = str(rgb[0]).split("=")[1], str(rgb[1]).split("=")[1], str(rgb[2]).split("=")[1]
            code = f"{red}, {green}, {blue}"
            rgb = tuple(map(int, code.split(', ')))

        image = Image.new("RGB", (256, 256), color = rgb)
        rand = randint(1, 1000000)
        image.save(f"./colors/{rand}.jpg")
        
        url = f"https://melonis.xyz/bot/colors/{rand}.jpg"
        embed.set_thumbnail(url = url)
        try:
            color_name = webcolors.rgb_to_name(rgb)
        except ValueError:
            color_name = ""

        rgb_int = (rgb[0]<<16) + (rgb[1]<<8) + rgb[2]

        hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hls = colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
        cmyk = utils.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        hsv = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, hsv))
        hls = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, hls))
        cmyk = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, cmyk))

        embed.set_author(name = f"Colour Information: {color_name}")
        embed.add_field(name = "Hex Value:", value = str(webcolors.rgb_to_hex(rgb)), inline = False)
        embed.add_field(name = "RGB Value:", value = f"rgb{str(rgb)}", inline = False)
        embed.add_field(name = "HSV Value:", value = f"hsv{str(hsv)}", inline = False)
        embed.add_field(name = "HLS Value:", value = f"hls{str(hls)}", inline = False)
        embed.add_field(name = "CMYK Value:", value = f"cmyk{str(cmyk)}", inline = False)
        embed.add_field(name = "Integer Value:", value = rgb_int, inline = False)
        
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Fun_commands(client))
    