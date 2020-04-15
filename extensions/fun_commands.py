import discord
import os
import json
import datetime
import random
from discord.ext import commands

cwd = os.path.dirname(__file__)
jsonPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
config = json.loads(open(jsonPath, "r").read())

class Fun_commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(help = "**`$avatar <user>`**",
    brief = "Shows the requested user avatar.",
    usage = "**Usage: `$avatar <user>`**",
    description = "Returns the user specified avatar, the `<user>` argument does not have to be specified and will return with the message authors avatar instead.\n\nExample: `$avatar <@MelonBot#0396`",
    example = "`$avatar <@560526844705636374>`"
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

        embed = discord.Embed(color = ctx.author.colour)
        utils.get_member(ctx, member)
        utils.create_embed(ctx, embed, member)
        embed.url = str(uAvatar)
        embed.title = "Avatar URL"
        embed.set_image(url = uAvatar)

        await ctx.send(embed = embed) 

    @commands.command(help = "**`$someone [message]`**",
    brief = "Sends a message to a random person in the server.",
    usage = "**Usage: `$someone [message]`**",
    description = "Sends the message specified in the `<message>` argument to a random person in the server, argument of `<message>` has to be given.\n\nExample: `$someone lmao get cucked retard`",
    example = "`$someone lmao get cucked retard`"
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

def setup(client):
    client.add_cog(Fun_commands(client))
    