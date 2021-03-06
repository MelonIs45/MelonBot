import discord
import os
import json
import sys
import aiohttp
import subprocess
from discord.ext import commands, tasks

cwd = os.path.dirname(os.path.realpath(__file__))
config = json.loads(open(cwd + "/config.json", "r").read())
client = commands.Bot(command_prefix = config["data"]["prefix"],  help_command=None)
aiosession = aiohttp.ClientSession(loop = client.loop)


@client.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.send("Restarting... (Please allow at least 5 seconds.)")
    python = sys.executable
    os.execl(python, python, * sys.argv)
    
@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"extensions.{extension}")
    await ctx.send(f"Extension: `{extension}` loaded!")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f"extensions.{extension}")
    await ctx.send(f"Extension: `{extension}` unloaded!")
    
@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    if ctx.message.content.split(" ")[1] == "all":
        unloadall()
        loadall()
        await ctx.send("Reloaded all extensions!")
    else:
        client.reload_extension(f"extensions.{extension}")
        await ctx.send(f"Extension: `{extension}` reloaded!")

def loadall():
    for filename in os.listdir(cwd + "/extensions"):
        if filename.endswith(".py"):
            client.load_extension(f"extensions.{filename[:-3]}")
            print(f"Loaded {filename}")

def unloadall():
    for filename in os.listdir(cwd + "/extensions"):
        if filename.endswith(".py"):
            client.unload_extension(f"extensions.{filename[:-3]}")
            print(f"Unloaded {filename}")

loadall()


with open("token.txt", "r") as file:
    token = file.readline()
client.run(token)