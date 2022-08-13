import discord
from discord.ext import commands
from gambling import givePoints, checkBalance
from gambling import gamble as gam
from gambling import leaderboard as lead
from weather import get_weather, configparser, requests

import random
config = configparser.ConfigParser()
config.read('config.ini')
discord_api_key = config['APIdata']['discord_api_key']

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

# copypastas for random generation
file = open("copypastas.txt")
copyandpastes = file.readlines()

# jokes for random generation
file = open("jokes.txt")
jokes = file.readlines()
jokeSize = len(jokes)

#returns the guild based off of the input message sent by the user

bot = commands.Bot(command_prefix="$")

def get_message_guild(message):
    for guild in bot.guilds:
        if message.guild == guild:
            return guild

#returns a list of all server members belonging to the server of the message

def get_server_users(message):
    currentGuild = get_message_guild(message)
    return currentGuild.members

#returns a list of all server roles belonging to the server of the message

def get_server_roles(message):
    currentGuild = get_message_guild(message)
    return currentGuild.roles

#converts a hex string to RGB

def hex_to_rgb(hex):
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)

    returnArray = []
    returnArray.append(r)
    returnArray.append(g)
    returnArray.append(b)
    return returnArray

#returns a role with a specific name

def get_role_with_name(name, message):
    currentGuild = get_message_guild(message)
    for roles in currentGuild.roles:
        if roles.name.upper() == name.upper():
            return roles

@bot.event
async def on_ready():
    print("Bot is ready.")

#ping command
@bot.command()
async def ping(ctx):
    latency = bot.latency
    await ctx.send(f"Pong! {latency}")

#wordle command
@bot.command()
async def wordle(ctx):
    await ctx.send("Don't spoil the wordle!")

#basics about chungbot and his actions (current is a placeholder)
@bot.command()
async def about(ctx):
    await ctx.send("existence is pain")

#chung
@bot.command()
async def chung(ctx):
    chungstory = copyandpastes[0]
    await ctx.send(chungstory)

#packwatch
@bot.command()
async def packwatch(ctx):
    packwatch = copyandpastes[1]
    await ctx.send(packwatch)

#coincidence
@bot.command()
async def coincidence(ctx):
    coincidence = copyandpastes[2]
    await ctx.send(coincidence)

#minion
@bot.command()
async def minion(ctx):
    minion = copyandpastes[3]
    await ctx.send(minion)

#displays a list of commands
@bot.command()
async def commands(ctx):
    await ctx.send("current commands include: \n$chung, $coincidence, $minion, $about, $packwatch, $randomnumber"
                                   " $jokes, $colors, $color, $addcolor, $removecolor, $weather, $mute, $unmute")

#displays a list of jokes
@bot.command()
async def joke(ctx):
    number = random.randint(0, jokeSize - 1)
    joke = jokes[number]
    await ctx.send(joke)

#random number generation
@bot.command()
async def randomnumber(ctx, arg1, arg2):
    nums = int(arg1)
    nums2 = int(arg2)
    try:
        finalnum = random.randint(nums, nums2)
        await (ctx.send("your number is: {}".format(finalnum)))
    except:
        await(ctx.send("invalid argument - message must be in the form \"$randomnumber x y\" with y > x"))

# heads or tails
@bot.command()
async def coinflip(ctx):
    flip = random.randint(1, 2)
    if flip == 1:
        await(ctx.send("Heads!"))
    else:
        await(ctx.send("Tails!"))


#sets a color
@bot.command()
async def color(ctx):
    if ctx.message.content.startswith('$color'):
        guildRoles = get_server_roles(ctx.message)
        colorname = ctx.message.content[7:len(ctx.message.content)]

        for role in guildRoles:
            if role.name.startswith("color:"):
              if role.name[6:len(role.name)].upper() == colorname.upper():
                    userRoles = ctx.message.author.roles
                    for role2 in userRoles:
                        if role2.name.startswith("color:"):
                            await ctx.message.author.remove_roles(role2)
                    await ctx.message.author.add_roles(role)
                    await(ctx.message.channel.send("{} was given color:{}".format(ctx.message.author.name, role.name[6:len(role.name)])))


#prints a list of colors
@bot.command()
async def colors(ctx):
    message = ctx.message
    for guild in bot.guilds:
        if message.guild == guild:
            guildRoles = guild.roles
            await message.channel.send("List of availible colors:")
            roleList = ""
            for role in guildRoles:
                if (role.name.startswith("color:")):
                    roleList = roleList + role.name[6:len(role.name)] + ", "
            roleList = roleList[0:len(roleList) - 2]
            await message.channel.send(roleList)

@bot.command()
async def addcolor(ctx):
    if ctx.message.author.guild_permissions.administrator:
        message = ctx.message
        try:
            guildRoles = get_server_roles(message)
            colorhex = int(message.content[10:17], 16)
            colorname = "color:" + message.content[17:len(message.content)]
            whichGuild = get_message_guild(message)
            role = get_role_with_name(colorname, message)
            if role is not None:
                raise AttributeError
            await whichGuild.create_role()
            newRole = get_role_with_name("new role", message)
            await newRole.edit(colour=colorhex)
            await newRole.edit(name=colorname)
            await newRole.edit(position=6)
            newRole.name = colorname
            await message.channel.send('added color role {} with hex value {}'.format(colorname, message.content[10:17]))
        except AttributeError:
            await message.channel.send('cannot add: color name already in use')
        except:
            await message.channel.send('invalid argument- please make sure request is in the form $addcolor ' '*hex* *colorname*')
    else:
        await ctx.send('only administrators can add and remove colors.')

@bot.command()
async def removecolor(ctx):
    if ctx.message.author.guild_permissions.administrator:
        message = ctx.message
        try:
            colorname = 'color:' + message.content[13:len(message.content)]
            role2get = get_role_with_name(colorname, message)
            if role2get is None:
                raise ValueError('color does not exist')
            if len(role2get.members) != 0:
                raise ValueError('$$cannot delete; color is currently in use')
            await role2get.delete()
            await message.channel.send('{} successfully deleted'.format(colorname))
        except ValueError:
            await message.channel.send('cannot delete; color is either currently in use or does not exist')
            return
    else:
        await ctx.send('only administrators can add and remove colors.')


#calls on the weather API to return the weather of a designated city

#works
@bot.command()
async def weather(ctx):
    message = ctx.message
    try:
        if len(message.content) == 8:
            raise ValueError
        weather = get_weather(message.content[9:len(message.content)])
        await message.channel.send("Weather data for {}, {}:".format(weather[4], weather[5]) + "\n" + weather[6] +
                                   " " + weather[3] + "\nTemperature: " + weather[0] + " °F\nPressure: " +
                                   weather[1] + " hPa\nHumidity: " + weather[2] + "%")

    except ValueError:
        await message.channel.send('error: city was not located')

#does not work afteer refactor - still troubleshooting
@bot.command()
async def gamble(ctx, arg1):
    message = ctx.message
    try:
        points = gam(message, int(arg1))
        if points[0] == 0:
            await message.channel.send("You lost :(")
        if points[0] == 1:
            await message.channel.send("You won! :D")
        await message.channel.send(
            message.author.name + " gambled " + str(points[2]) + " points and now has " + str(points[1]) + " points.")

    except ValueError:
         await message.channel.send("Error: User not found in gambling database. if this is the case, please do $dailypoints to start gambling.")
    except AttributeError:
         await message.channel.send("Invalid argument: Please format your message in the form $gamble *points*. if you have not yet gambled using this bot, please run $dailyoints to start gambling.")
    except:
         await message.channel.send("Error: User does not have enough points to gamble. if you have not yet gambled, please run $dailypoints to start gambilng")

#works
@bot.command()
async def dailypoints(ctx):
    message = ctx.message
    try:
        points = givePoints(message)
        if points[0] == 0 or points[0] == 1:
            await message.channel.send("100 daily points have been deposited into your account.")
        if points[0] == 2:
            await message.channel.send("Please wait 24 hours before claiming daily points again.")
    except:
        await message.channel.send("Argument error. Please try again using the format $dailypoints")

#works
@bot.command()
async def balance(ctx):
    message = ctx.message
    balance = checkBalance(message)
    if balance[0] == 0:
        await message.channel.send(
            "You are not in the gambling system. Please type *$dailypoints* to begin gambling on this server.")
    elif balance[0] == 1:
        await message.channel.send(message.author.name + " currently has " + str(balance[1]) + " points.")

#works
@bot.command()
async def points(ctx):
    message = ctx.message
    balance = checkBalance(message)
    if balance[0] == 0:
        await message.channel.send(
            "You are not in the gambling system. Please type *$dailypoints* to begin gambling on this server.")
    elif balance[0] == 1:
        await message.channel.send(message.author.name + " currently has " + str(balance[1]) + " points.")

#does not work after refactor- still troubleshooting
@bot.command()
async def leaderboard(ctx):
    message = ctx.message
    users = get_server_users(message)
    winners = "leaderboard is currently unresponsive following code refactoring. we are sorry for the temporary loss of functionality."
    topGamblers = lead(message, users)
    i = 1
    for gamblers in topGamblers:
        winners += (str(i) + ". " + str(gamblers[0]) + " (points: " + str(gamblers[1]) + ")\n")
        i += 1
    await message.channel.send(winners)

@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):

    if ctx.message.author.guild_permissions.administrator:
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=False, read_messages=False)

        await member.add_roles(mutedRole, reason=reason)
        await ctx.send(f"Muted {member.mention} for reason {reason}")
        await member.send(f"You were muted in  {guild.name} :(")

@bot.command()
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}")
    await member.send(f"You were unmuted in {ctx.guild.name}!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    #gambles a certian amount of points (the number that follows the $gamble keyword)

    if message.content.startswith('$gamble'):
        try:
            points = gamble(message, int(message.content[8:len(message.content)]))
            if points[0] == 0:
                await message.channel.send("You lost :(")
            if points[0] == 1:
                await message.channel.send("You won! :D")
            await message.channel.send(message.author.name + " gambled " + str(points[2]) + " points and now has " + str(points[1]) + " points.")

        except ValueError:
            await message.channel.send("Error: User not found in gambling database")
        except AttributeError:
            await message.channel.send("Error: User does not have enough points to gamble")
        except:
            await message.channel.send("Invalid argument: Please format your message in the form $gamble *points*")

    #claims a user's 100 daily points

    if message.content.startswith('$dailypoints'):
        try:
            points = givePoints(message)
            if points[0] == 0 or points[0] == 1:
                await message.channel.send("100 daily points have been deposited into your account.")
            if points[0] == 2:
                await message.channel.send("Please wait 24 hours before claiming daily points again.")
        except:
            await message.channel.send("Argument error. Please try again using the format $dailypoints")

    #checks a user's balance

    if message.content.startswith('$balance') or message.content.startswith('$points'):
        balance = checkBalance(message)
        if balance[0] == 0:
            await message.channel.send("You are not in the gambling system. Please type *$dailypoints* to begin gambling on this server.")
        elif balance[0] == 1:
            await message.channel.send(message.author.name + " currently has " + str(balance[1]) + " points.")

    if message.content.startswith('$leaderboard'):
        users = get_server_users(message)
        winners = ""
        topGamblers = leaderboard(message, users)
        i = 1
        for gamblers in topGamblers:
            winners += (str(i) + ". " + str(gamblers[0]) + " (points: " + str(gamblers[1]) + ")\n")
            i += 1
        await message.channel.send(winners)


bot.run(discord_api_key)
