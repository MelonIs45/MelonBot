import discord
import os
import json
import datetime
import sys
import time
from discord.ext import commands, tasks

cwd = os.path.dirname(__file__)
jsonPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
config = json.loads(open(jsonPath, "r").read())

class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def auto_restart(self):
        time.sleep(14400) #4 hours in seconds
        python = sys.executable
        os.execl(python, python, * sys.argv)

def setup(client):
    client.add_cog(Tasks(client))