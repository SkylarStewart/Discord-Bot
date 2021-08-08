import discord
from gambling import gamble, givePoints, random, checkBalance
from weather import get_weather, configparser, requests

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

def get_message_guild(message):
    for guild in client.guilds:
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

# runs upon bot initialization
@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))



# handles commands and misc. messages. main event loop for message handling.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # basics about Chungbot & his actions

    if message.content.startswith('$about'):
        await message.channel.send("existence is pain")

    if message.content.startswith('$chung'):
        chungstory = copyandpastes[0]
        await message.channel.send(chungstory)

    # packwatch

    if message.content.startswith('$packwatch'):
        packwatch = copyandpastes[1]
        await message.channel.send(packwatch)

    # there's no such thing as a coincidence...

    if message.content.startswith('$coincidence'):
        coincidence = copyandpastes[2]
        await message.channel.send(coincidence)

    # minion image

    if message.content.startswith('$minion'):
        minion = copyandpastes[3]
        await message.channel.send(minion)

    # list of all available commands from ChungBot

    if message.content.startswith('$commands'):
        await message.channel.send("current commands include: \n$chung, $coincidence, $minion, $about, $packwatch,"
                                   " $jokes, $colors, $color, $addcolor, $removecolor, $weather")

    # returns a series of jokes based off of random number generation

    if message.content.startswith('$joke'):
        number = random.randint(0, jokeSize - 1)
        joke = jokes[number]
        await message.channel.send(joke)

    # random number generation

    if message.content.startswith('$random'):
        nums = message.content[7:len(message.content)]
        try:
            numbers = nums.split('-')
            finalnum = random.randint(int(numbers[0]), int(numbers[1]))
            await(message.channel.send("your number is: {}".format(finalnum)))
        except:
            await(message.channel.send("invalid argument- message must be in the form \"$random x-y\" with y > x"))

    # heads-or-tails
    if message.content.startswith('$coinflip'):
        flip = random.randint(1, 2)
        if flip == 1:
            await(message.channel.send("Heads!"))
        if flip == 2:
            await(message.channel.send("Tails!"))

    # role color management (allows users to choose their nickname's color)]
    guildRoles = []

    if message.content.startswith('$color'):
        guildRoles = get_server_roles(message)
        colorname = message.content[7:len(message.content)]

        for role in guildRoles:
            if role.name.startswith("color:"):
              if role.name[6:len(role.name)].upper() == colorname.upper():
                    userRoles = message.author.roles
                    for role2 in userRoles:
                        if role2.name.startswith("color:"):
                            await message.author.remove_roles(role2)
                    await message.author.add_roles(role)
                    await(message.channel.send("{} was given color:{}".format(message.author.name, role.name[6:len(role.name)])))

    #lists all availible colors

    if message.content.startswith('$colors'):
        for guild in client.guilds:
            if message.guild == guild:
                guildRoles = guild.roles
                await message.channel.send("List of availible colors:")
                roleList = ""
                for role in guildRoles:
                    if (role.name.startswith("color:")):
                      roleList = roleList + role.name[6:len(role.name)] + ", "
                roleList = roleList[0:len(roleList)-2]
                await message.channel.send(roleList)

    #used for adding colors to the role list

    if message.content.startswith('$addcolor'):
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
            await message.channel.send('invalid argument- please make sure request is in the form $addcolor '
                                       '*hex* *colorname*')

    #used for removing colors from the role list

    if message.content.startswith('$removecolor'):
        try:
            colorname = 'color:' + message.content[13:len(message.content)]
            role2get = get_role_with_name(colorname, message)
            if role2get is None:
                raise ValueError('color does not exist')
            if len(role2get.members) != 0:
                raise ValueError('cannot delete; color is currently in use')
            await role2get.delete()
            await message.channel.send('{} successfully deleted'.format(colorname))
        except ValueError:
            await message.channel.send('cannot delete; color is either currently in use or does not exist')
            return

    #calls on the weather API to return the weather of a designated city

    if message.content.startswith('$weather'):
        try:
            if len(message.content) == 8:
                raise ValueError
            weather = get_weather(message.content[9:len(message.content)])
            await message.channel.send("Weather data for {}, {}:".format(weather[4], weather[5]) + "\n" + weather[6] +
                                       " " + weather[3] + "\nTemperature: " + weather[0] + " °F\nPressure: " +
                                       weather[1] + " hPa\nHumidity: " + weather[2] + "%")

        except ValueError:
            await message.channel.send('error: city was not located')

    #gambles a certian amount of points (the number that follows the $gamble keyword)

    if message.content.startswith('$gamble'):
        try:
            points = gamble(message, int(message.content[8:len(message.content)]))
            print("gambled!")
            if points[0] == 0:
                await message.channel.send("You lost :(")
            if points[0] == 1:
                await message.channel.send("You won! :D")
            print("this is the finale...")
            await message.channel.send(message.author.name + " gambled " + str(points[2]) + " points and now has " + str(points[1]) + " points.")

        except ValueError:
            await message.channel.send("Error: User not found in gambling database")
        except AttributeError:
            await message.channel.send("Error: User does not have enough points to gamble")
        except:
            await message.channel.send("Invalid argument: Please format your message in the form $gamble *points*")

    #claim's a user's 100 daily points

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

    if message.content.startswith('$balance'):
        balance = checkBalance(message)
        if balance[0] == 0:
            await message.channel.send("You are not in the gambling system. Please type *$dailypoints* to begin gambling on this server.")
        elif balance[0] == 1:
            await message.channel.send(message.author.name + " currently has " + str(balance[1]) + " points.")




client.run(discord_api_key)

