import discord
import os
import json
from discord.ext import commands

cwd = os.path.dirname(os.path.realpath(__file__))
config = json.loads(open(cwd + "/config.json", "r").read())
client = commands.Bot(command_prefix = config["data"]["prefix"],  help_command=None)

@client.command()
async def load(ctx, extension):
    client.load_extension(f"extensions.{extension}")
    await ctx.send(f"Extension: `{extension}` loaded!")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"extensions.{extension}")
    await ctx.send(f"Extension: `{extension}` unloaded!")
    
@client.command()
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
client.run(config["data"]["token"])
