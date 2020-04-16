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

    @commands.command(help = "**`$help <command>`**",
    brief = "Specify a command and it will tell you information on how to properly use it.",
    usage = "**Usage: `$help <command>`**",
    description = "Hmm are you that much of a melon to understand???\n\nExample: `$help ping`"
    )
    async def help(self, ctx, r_command = None):
        utils = self.client.get_cog("Utils")
        member = ctx.guild.get_member(ctx.author.id)
        if r_command is None:
            embed = discord.Embed()
            utils.get_member(ctx, member)
            utils.create_embed(ctx, embed, member)
            embed.title = "MelonBot Help"
            for command in self.client.commands:
                if command.help is None:
                    pass
                else:
                    embed.add_field(name = command.help, value = command.brief, inline = False)
            embed.set_author(name = "")
            await ctx.channel.send(embed = embed)
        else:
            for command in self.client.commands: 
                if command.name == r_command:
                    embed = discord.Embed()
                    utils.get_member(ctx, member)
                    utils.create_embed(ctx, embed, member)

                    embed.title = "MelonBot Help"
                    embed.add_field(name = command.usage, value = command.description, inline = False)
                    embed.set_author(name = "")

                    await ctx.channel.send(embed = embed) 
                else:
                    ctx.send("Unable to find command!")       

    @commands.command(help = "**`$ping`**",
    brief = "Returns ping in ms.",
    usage = "**Usage: `$ping`**",
    description = "Returns the client latency in milliseconds, no arguments are to be given.\n\nExample: `$ping`"
    )
    async def ping(self, ctx):
        utils = self.client.get_cog("Utils")
        client = self.client
        member = None

        if ctx.author == client.user:
            return

        embed = discord.Embed()
        utils.get_member(ctx, member)
        utils.create_embed(ctx, embed, member)
        embed.description = 'Pong! {0}ms'.format(round((client.latency)*1000, 1))

        await ctx.send(embed = embed)  

    @commands.command(help = "**`$info <user>`**",
    brief = "Shows info about a user.",
    usage = "**Usage: `$info <user>`**",
    description = "Returns information about the user specified in the `<user>` argument, an empty `<user>` argument will return the authors information instead.\n\nExample: `$info @MelonBot#0396`"
    )
    async def info(self, ctx, member : discord.Member = None):
        utils = self.client.get_cog("Utils")
        client = self.client

        if ctx.author == client.user:
            return

        if member is None:
            member = ctx.guild.get_member(ctx.author.id)

        roleTags = ""
        for role in member.roles:
            if role.name == "@everyone":
                pass
            else:
                roleTags += (f"<@&{role.id}> ")

        url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=512".format(member)
        
        utils.get_member(ctx, member)
        embed = discord.Embed()
        utils.create_embed(ctx, embed, member)
        embed.set_thumbnail(url = url)
        embed.add_field(name = "**ID:**", value = member.id, inline = True)
        embed.add_field(name = "**Nickname:**", value = member.nick, inline = True)
        embed.add_field(name = "**Account Created:**", value = member.created_at.strftime("%A %d %B %Y at %X%p"), inline = False)
        embed.add_field(name = "**Guild Join Date:**", value = member.joined_at.strftime("%A %d %B %Y at %X%p"), inline = False)
        embed.add_field(name = "**Roles:**", value = roleTags, inline = False)

        await ctx.send(embed = embed)

    @commands.command(help = "**`$channel <channel>`**",
        brief = "Shows stats about the specified channel.",
        usage = "**Usage: `$channel <channel>`**",
        description = "Shows various information about the channel specified in the `<channel>` argument, leave blank for information of the current channel.\n\nExample: `$channel #bot-commands`"
    )
    async def channel(self, ctx, channel : discord.TextChannel = None):
        utils = self.client.get_cog("Utils")

        member = None
        embed = discord.Embed()
        utils.get_member(ctx, member)
        utils.create_embed(ctx, embed, member)

        if channel is None:
            channel = ctx.guild.get_channel(ctx.channel.id)

        embed.set_author(name = f"Info for channel: {channel.name}")
        embed.add_field(name = "**Channel ID:**", value = channel.id, inline = False)
        embed.add_field(name = "**Channel Description:**", value = channel.topic, inline = False)

        await ctx.send(embed = embed)

    @commands.command(help = "**`$server | roles`**",
    brief = "Shows stats about the server.",
    usage = "**Usage: `$server | roles`**",
    description = "Shows various information about the server, shows roles in the guild if included `roles` flag.\n\nExample: `$guild roles`"
    )
    async def server(self, ctx, flag = None):
        utils = self.client.get_cog("Utils")
        client = self.client

        member = None
        embed = discord.Embed()
        utils.get_member(ctx, member)
        utils.create_embed(ctx, embed, member)

        guild = client.get_guild(ctx.guild.id)

        if flag is None:
            embed.set_author(name = "")
            embed.title = f"Info for guild: **{guild.name}**"
            embed.add_field(name = "**Channel ID:**", value = guild.id, inline = False)
            embed.add_field(name = "**Verification Level:**", value = guild.verification_level, inline = False)
            embed.add_field(name = "**Region:**", value = guild.region, inline = True)
            embed.add_field(name = "**Shard:**", value = guild.shard_id, inline = True)
            embed.add_field(name = "**Members:**", value = len(guild.members), inline = True)
            embed.add_field(name = "**Text Channels:**", value = len(guild.text_channels), inline = False)
            embed.add_field(name = "**Voice Channels:**", value = len(guild.voice_channels), inline = False)
            embed.add_field(name = "**Owner:**", value = guild.owner, inline = True)
            embed.add_field(name = "**Owner ID:**", value = guild.owner_id, inline = True)
            embed.add_field(name = "**Created At:**", value = guild.created_at.strftime("%A %d %B %Y at %X%p"), inline = False)
            embed.set_thumbnail(url = guild.icon_url)
        else:
            roles = ""
            for role in guild.roles:
                if role.name == "@everyone":
                    pass
                else:
                    roles += (f"<@&{role.id}> ")

            embed.set_author(name = "")
            embed.title = f"Roles for server: **{guild.name}**"
            embed.add_field(name = "**Roles:**", value = roles, inline = False)

        await ctx.send(embed = embed)

    @commands.command(help = "**`$invite`**",
    brief = "Sends an invite link for the bot.",
    usage = "**Usage: `$invite`**",
    description = "Sends an invite link for the bot which can be used to add the bot to a server, no arguments are to be given.\n\nExample: `$invite`"
    )
    async def invite(self, ctx):
        utils = self.client.get_cog("Utils")
        client = self.client
        member = None
        embed = discord.Embed()
        utils.get_member(ctx, member)
        utils.create_embed(ctx, embed, member)

        embed.set_author(name = f"Invite link for: {client.user.name}")
        embed.description = "https://discordapp.com/api/oauth2/authorize?client_id=560526844705636374&permissions=27648&scope=bot"

        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Info_commands(client))
    