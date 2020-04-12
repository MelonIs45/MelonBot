import discord, random, asyncio, datetime, json
from discord.ext import commands as cmds
import os

cwd = os.path.dirname(os.path.realpath(__file__))
config = json.loads(open(cwd + "/config.json", "r").read())
client = cmds.Bot(command_prefix = '$',  help_command=None)


@client.event
async def on_message(message):
    masterChannelId = client.get_channel(int(config['log']['channelId']))
    if message.guild.id == int(config['log']['logGuild']) and message.author != client.user:
        if len(message.attachments) > 0:
            attUrl = "".join(str(x) for x in message.attachments)
            attUrl = attUrl.split(" ")[3]
            attUrl = attUrl.lstrip("url='").rstrip("'>'")
            logText = "{0} {1}".format(message.content, attUrl)
        else:
            attUrl = None
            logText = message.content
        log = open("log.txt", "a")
        logName = message.author.display_name
        currentDT = datetime.datetime.now()
        logTime = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        logFull = "{0} | {1} | {2}".format(logTime, logName, logText)
        log.write(logFull + "\n")

        embed = discord.Embed()
        embed.set_author(name = message.guild.get_member(message.author.id), icon_url = message.author.avatar_url)
        embed.description = f"{message.content} {attUrl}"
        embed.set_footer(text = "channel: {0}".format(message.channel.name))
        embed.timestamp = message.created_at
        await masterChannelId.send(embed = embed)
        
    await client.process_commands(message)

@client.command()
async def help(message):
    user = message.author

    embed = discord.Embed(color = user.colour)
    embed.title = 'MelonBot Help'
    embed.add_field(name = '$ping', value = 'Returns ping in ms.', inline = False)
    embed.add_field(name = '$avatar <user>', value = 'Shows the requested user their avatar, leave blank for your own.', inline = False)
    embed.add_field(name = '$someone <message>', value = 'Sends a message to a random person in the server', inline = False)
    embed.add_field(name = '$info (WIP)', value = 'Shows stats about a user', inline = False)
    embed.add_field(name = '$placeholder', value = 'placeholder', inline = False)
    embed.add_field(name = '$placeholder', value = 'placeholder', inline = False)

    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text = f"Requested by {message.guild.get_member(message.author.id)}", icon_url = message.guild.get_member(user.id).avatar_url_as(format='png'))

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
    if ctx.author == client.user:
        return
    if mUser == None:
        mUser = ctx.message.guild.get_member(ctx.message.author.id)
        try:
            uAvatar = mUser.avatar_url_as(format='gif', size=256)
        except discord.errors.InvalidArgument:
            uAvatar = mUser.avatar_url_as(format='png', size=256)
    else:
        try:
            uAvatar = mUser.avatar_url_as(format='gif', size=256)
        except discord.errors.InvalidArgument:
            uAvatar = mUser.avatar_url_as(format='png', size=256)
    
    
    #roles = mUser.roles
    #roles = roles.split(", ")
    #print(roles)
    #attUrl = attUrl.split(" ")[3]
    #attUrl = attUrl.lstrip("url='").rstrip("'>'")
    user = ctx.message.author
    embed = discord.Embed(color = user.colour)
    embed.set_author(name = mUser)
    embed.url = str(uAvatar)
    embed.title = "Avatar URL"
    embed.set_image(url = uAvatar)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text = f"Requested by {ctx.message.guild.get_member(ctx.message.author.id)}", icon_url = ctx.message.guild.get_member(user.id).avatar_url_as(format='png'))

    await ctx.send(embed = embed) 

@client.command()
async def info(ctx, mUser : discord.Member=None):
    if ctx.author == client.user:
        return
    if mUser == None:
        mUser = ctx.message.guild.get_member(ctx.message.author.id)
    user = ctx.message.author
    print(ctx.message.author.roles)
    roleTags = ""
    for role in mUser.roles:
        if role.name == "@everyone":
            pass
        else:
            print(role.id)
            roleTags += (f"<@&{role.id}> ")
    print(roleTags)
    
    embed = discord.Embed(color = user.colour)
    embed.set_author(name = ctx.message.guild.get_member(ctx.message.author.id))
    embed.timestamp = datetime.datetime.utcnow()
    embed.add_field(name = "**ID:**", value = ctx.message.author.id, inline = True)
    embed.add_field(name = "**Nickname:**", value = mUser.nick, inline = True)
    embed.add_field(name = "**Account Created:**", value = mUser.created_at.strftime("%A %d %B %Y at %X%p"), inline = False)
    embed.add_field(name = "**Guild Join Date:**", value = mUser.joined_at.strftime("%A %d %B %Y at %X%p"), inline = False)
    embed.add_field(name = "**Roles:**", value = roleTags, inline = False)
    embed.set_footer(text = f"Requested by {ctx.message.guild.get_member(ctx.message.author.id)}", icon_url = ctx.message.guild.get_member(user.id).avatar_url_as(format='png'))

    await ctx.send(embed = embed) 

@client.command()
async def ping(ctx):
    if ctx.author == client.user:
        return
    user = ctx.message.author
    embed = discord.Embed(color = user.color)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_author(name = ctx.message.guild.get_member(ctx.message.author.id))
    latency = (client.latency)*1000
    embed.description = 'Pong! {0}ms'.format(round(latency, 1))
    embed.set_footer(text = f"Requested by {ctx.message.guild.get_member(ctx.message.author.id)}", icon_url = ctx.message.guild.get_member(user.id).avatar_url_as(format='png'))

    await ctx.send(embed = embed)    

@client.command()
async def bertas(message):
    if message.author == client.user:
        return
    user = message.author
    embed = discord.Embed(color = user.color)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_author(name = message.guild.get_member(message.author.id))
    embed.description = 'Bertas is a nibba that has the big gay.'
    embed.set_footer(text = f"Requested by {message.guild.get_member(message.author.id)}", icon_url = message.guild.get_member(user.id).avatar_url_as(format='png'))

    await message.channel.send(embed = embed)

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = 'Use $ for commands'))
    print('Ready!')
print('Bot made by MelonIs45#8078')
print('------')

client.run(config['data']['token'])