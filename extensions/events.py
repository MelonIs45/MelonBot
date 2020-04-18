import discord
import os
import json
import datetime
import sys
from discord.ext import commands, tasks

cwd = os.path.dirname(__file__)
jsonPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')
config = json.loads(open(jsonPath, "r").read())

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        client = self.client
        print(f"-----------\nBot made by MelonIs45#8078\nLogged in as: {client.user.name}\nReady!")
        tasks = client.get_cog("Tasks")
        await tasks.auto_restart()

    @commands.Cog.listener()
    async def on_message(self, message):
        global embed
        embed = discord.Embed(color = message.author.color)
        utils = self.client.get_cog("Utils")
        client = self.client
        member = message.guild.get_member(message.author.id)

        masterChannelId = client.get_channel(int(config['log']['channelId']))
        if message.guild.id == int(config['log']['logGuild']) and message.author != client.user:
            if len(message.attachments) > 0:
                attUrl = "".join(str(x) for x in message.attachments)
                attUrl = attUrl.split(" ")[3]
                attUrl = attUrl.lstrip("url='").rstrip("'>'")
                logText = "{0} {1}".format(message.content, attUrl)
            else:
                attUrl = ""
                logText = message.content

            log = open("log.txt", "a")
            logName = message.author.display_name
            currentDT = datetime.datetime.now()
            logTime = currentDT.strftime("%Y-%m-%d %H:%M:%S")
            logFull = "{0} | {1} | {2}".format(logTime, logName, logText)
            log.write(logFull + "\n")

            utils.create_embed(message, embed, member)    
            embed.description = f"{message.content} {attUrl}"
            embed.set_footer(text = f"Sent by {member}", icon_url = member.avatar_url_as(format='png'))

            await masterChannelId.send(embed = embed)

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, commands.MissingPermissions):
    #         await ctx.send("Missing permissions.")
    #     elif isinstance(error, commands.NotOwner):
    #         await ctx.send("You aren't the bot owner :D")
    #     else:
    #         print(error)

def setup(client):
    client.add_cog(Events(client))
