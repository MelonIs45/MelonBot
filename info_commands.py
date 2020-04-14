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
    async def help(self, ctx, command = None):
        utils = self.client.get_cog("Utils")
        
        if command is None:
            embed = discord.Embed(color = ctx.author.colour)
            utils.create_embed(ctx, embed)
            embed.title = 'MelonBot Help'
            embed.add_field(name = '**`$help <command>`**', value = 'Specify a command and it will tell you information on how to properly use it.', inline = False)
            embed.add_field(name = '**`$ping`**', value = 'Returns ping in ms.', inline = False)
            embed.add_field(name = '**`$avatar <user>`**', value = 'Shows the requested user their avatar.', inline = False)
            embed.add_field(name = '**`$someone [message]`**', value = 'Sends a message to a random person in the server.', inline = False)
            embed.add_field(name = '**`$info <user>`**', value = 'Shows stats about a user.', inline = False)
            embed.add_field(name = '**`$purge [amount | Max is 50]`**', value = '**Moderator Command:** Deletes the amount of messages specified.', inline = False)
    
            await ctx.channel.send(embed = embed) 
        else:
            embed = discord.Embed(color = ctx.author.color)
            utils.create_embed(ctx, embed)
            if command == "help":
                embed.add_field(name = '**Usage: `$help`**', value = 'Hmm are you that much of a melon to understand???')
            elif command == "ping":
                embed.add_field(name = '**Usage: `$ping`**', value = 'Returns the client latency in milliseconds, no arguments are to be given.')
            elif command == "avatar":
                embed.add_field(name = '**Usage: `$avatar <user>`**', value = 'Returns the user specified avatar, the `<user>` argument does not have to be specified and will return with the message authors avatar instead.')
            elif command == "someone":
                embed.add_field(name = '**Usage: `$someone [message]`**', value = 'Sends the message specified in the `<message>` argument to a random person in the server, argument of `<message>` has to be given.')
            elif command == "info":
                embed.add_field(name = '**Usage: `$info <user>`**', value = 'Returns information about the user specified in the `<user>` argument, an empty `<user>` argument will return the authors information instead.')
            elif command == "purge":
                embed.add_field(name = '**Usage: `$purge [amount | Max is 50]`**', value = 'Deletes the amount of messages specified in the `[amount]` argument, requires the `Manage Messages` permission for the bot.')
            else:
                embed.add_field(name = '**Error:**', value = 'Not a vaild command, please refer to the **`$help`** command for guidance.')
                
            await ctx.send(embed = embed) 

    @commands.command()
    async def ping(self, ctx):
        utils = self.client.get_cog("Utils")
        client = self.client

        if ctx.author == client.user:
            return

        embed = discord.Embed(color = ctx.author.color)
        utils.create_embed(ctx, embed)
        embed.description = 'Pong! {0}ms'.format(round((client.latency)*1000, 1))

        await ctx.send(embed = embed)  

    @commands.command()
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

        embed = discord.Embed(color = ctx.author.colour)
        utils.create_embed(ctx, embed, member)
        embed.set_thumbnail(url = url)
        embed.add_field(name = "**ID:**", value = member.id, inline = True)
        embed.add_field(name = "**Nickname:**", value = member.nick, inline = True)
        embed.add_field(name = "**Account Created:**", value = member.created_at.strftime("%A %d %B %Y at %X%p"), inline = False)
        embed.add_field(name = "**Guild Join Date:**", value = member.joined_at.strftime("%A %d %B %Y at %X%p"), inline = False)
        embed.add_field(name = "**Roles:**", value = roleTags, inline = False)

        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Info_commands(client))
    