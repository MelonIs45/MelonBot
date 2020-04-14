import discord
import os
import json
import datetime
from discord.ext import commands

cwd = os.path.dirname(__file__)
jsonPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')
config = json.loads(open(jsonPath, "r").read())

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("-----------\nBot made by MelonIs45#8078\nReady!")

    @commands.Cog.listener()
    async def on_message(self, ctx, message):
        utils = self.client.get_cog("Utils")
        client = self.client

        masterChannelId = client.get_channel(int(config['log']['channelId']))
        if ctx.guild.id == int(config['log']['logGuild']) and ctx.author != client.user:
            if len(ctx.attachments) > 0:
                attUrl = "".join(str(x) for x in ctx.attachments)
                attUrl = attUrl.split(" ")[3]
                attUrl = attUrl.lstrip("url='").rstrip("'>'")
                logText = "{0} {1}".format(ctx.content, attUrl)
            else:
                attUrl = ""
                logText = ctx.content

            log = open("log.txt", "a")
            logName = ctx.author.display_name
            currentDT = datetime.datetime.now()
            logTime = currentDT.strftime("%Y-%m-%d %H:%M:%S")
            logFull = "{0} | {1} | {2}".format(logTime, logName, logText)
            log.write(logFull + "\n")

            embed = discord.Embed(color = ctx.author.color)
            utils.create_embed(ctx, embed)    
            embed.description = f"{ctx.content} {attUrl}"

            await masterChannelId.send(embed = embed)
        await client.process_commands(message)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, UnboundLocalError):
            pass
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Missing `Manage Messages` permission.")
        


def setup(client):
    client.add_cog(Events(client))