import discord, random, asyncio, datetime, json
from discord.ext import commands as cmds
import os

cwd = os.path.dirname(os.path.realpath(__file__))
config = json.loads(open(cwd + "/config.json", "r").read())
client = cmds.Bot(command_prefix = '$',  help_command=None)
status = ['1', '12', '123', '1234', '12345']

@client.event
async def on_message(message):
    #you can add a list of guilds to log
    if message.guild.id == 657281286905266247:
        log = open("log.txt", "a")
        logText = message.content
        logName = message.author.display_name
        currentDT = datetime.datetime.now()
        logTime = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        logFull = "{0} | {1} | {2}".format(logTime, logName, logText)
        log.write(logFull+"\n")
        
    await client.process_commands(message)

@client.command()
async def help(message):
    user = message.author
    reqMember = message.guild.get_member(user.id)
    reqAvatar = reqMember.avatar_url_as(format='png')

    embed = discord.Embed(
        color = user.colour
    )
    embed.title = 'MelonBot Help'
    embed.add_field(name = '$ping', value = 'Returns ping in ms.', inline = False)
    embed.add_field(name = '$avatar <user>', value = 'Shows the requested user their avatar, leave blank for your own.', inline = False)
    embed.add_field(name = '$someone <message>', value = 'Sends a message to a random person in the server', inline = False)
    embed.add_field(name = '$info (WIP)', value = 'Shows stats about a user', inline = False)
    embed.add_field(name = '$placeholder', value = 'placeholder', inline = False)
    embed.add_field(name = '$placeholder', value = 'placeholder', inline = False)

    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text = f"Requested by {user.name}", icon_url = reqAvatar)

    await message.channel.send(embed = embed) 

@client.command()
async def someone(ctx, message):
    if ctx.author == client.user:
        return
    memberList = []
    for member in ctx.guild.members:
        if member.bot == True:
            pass
        else:
            memberList.append(member.id)
    memberId = random.choice(memberList)
    memberName = ctx.author.display_name
    msgContent = ctx.message.content.split(" ", 1)
    try:
        if '"' in msgContent[1]:
            await ctx.channel.send("Please dont put in quotes as it breaks the bot, try using something else.")
            return
        if "'" in msgContent[1]:
            await ctx.channel.send("Please dont put in quotes as it breaks the bot, try using something else.") 
            return 
        msg = '{0} says: <@{1}> {2}'.format(memberName, memberId, msgContent[1])
        await ctx.channel.send(msg)
    except IndexError:
        await ctx.channel.send("Please specify text to be said after the user mentioned.")

@client.command()
async def avatar(ctx, mUser : discord.Member=None):
    if mUser == None:
        mUser = ctx.message.guild.get_member(ctx.author.id)
        try:
            uAvatar = mUser.avatar_url_as(format='gif', size=256)
        except discord.errors.InvalidArgument:
            uAvatar = mUser.avatar_url_as(format='png', size=256)
    else:
        try:
            uAvatar = mUser.avatar_url_as(format='gif', size=256)
        except discord.errors.InvalidArgument:
            uAvatar = mUser.avatar_url_as(format='png', size=256)
        
    user = ctx.message.author
    reqMember = ctx.message.guild.get_member(ctx.author.id)
    reqAvatar = reqMember.avatar_url_as(format='png')
    embed = discord.Embed(color = user.colour)
    embed.set_author(name = mUser)
    embed.url = str(uAvatar)
    embed.title = "Avatar URL"
    embed.set_image(url = uAvatar)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text = f"Requested by {user.name}", icon_url = reqAvatar)

    await ctx.send(embed = embed) 

@client.command()
async def info():
    pass

@client.command()
async def ping(ctx):
    latency = (client.latency)*1000
    await ctx.send('Pong! {0}ms'.format(round(latency, 1)))    

@client.command()
async def bertas(message):
    await message.channel.send('Bertas is a nibba that has the big gay.')

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = 'Use $ for commands'))
    print('Ready!')
print('Bot made by MelonIs45#8078')
print('------')

client.run(config['data']['token'])