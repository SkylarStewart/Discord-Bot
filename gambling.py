import random
import time

#gives 100 daily points to a user. If the user does not exists, creates a new data entry.

def givePoints(message):
    currentSeconds = int(time.time())
    author = message.author.id
    f = open("gamblers.txt")
    gamblers = f.readlines()

    gamblingArray = []
    for gambler in gamblers:
        gamblingArray.append(gambler.split(" "))

    foundGambler = False
    points = 0
    lineFound = 0
    currentTime = 0

    for gambler in gamblingArray:
        if author == int(gambler[0]):
            foundGambler = True
            points = int(gambler[1])
            currentTime = int(gambler[2])
            break

        lineFound += 1;
    f.close()
    f = open("gamblers.txt", 'w')

#differentiates between new and returning users (new users require appending to the gamblers array)
    if foundGambler == False:
        points += 100
        gamblers.append(str(message.author.id) + " " + str(points) + " " + str(currentSeconds)+"\n")
        f.writelines(gamblers)
        return [0, points]
    if foundGambler == True:
        if currentSeconds - currentTime >= 86400:
            points += 100
            gamblers[lineFound] = str(message.author.id) + " " + str(points) + " " + str(currentSeconds) + "\n"
            f.writelines(gamblers)
            return [1, points]
        elif currentSeconds - currentTime < 86400:
            f.writelines(gamblers)
            return [2, points]


#gambles X number of points. If you win, the points are doubled. If you lose, all gambled points are lost.

def gamble(message, pointsGambled):
    author = message.author.id
    f = open("gamblers.txt")
    gamblers = f.readlines()

    if len(gamblers) == 0:
        raise ValueError

    gamblingArray = []
    for gambler in gamblers:
        gamblingArray.append(gambler.split(" "))

    foundGambler = False
    points = 0
    lineFound = 0
    currentTime = 0

    for gambler in gamblingArray:
        if author == int(gambler[0]):
            foundGambler = True
            points = int(gambler[1])
            currentTime = int(gambler[2])
            break

        lineFound += 1;

    f.close()

    if pointsGambled > points:
        raise AttributeError

    if foundGambler == False:
        raise ValueError

    f = open("gamblers.txt", 'w')

    points -= pointsGambled
    rng = random.randint(0, 1)
    if rng == 0:
        gamblers[lineFound] = (str(author) + " " + str(points) + " " + str(currentTime) +"\n")
        f.writelines(gamblers)
        return [0, points, pointsGambled]

    if rng == 1:
        points += (pointsGambled * 2)
        gamblers[lineFound] = (str(author) + " " + str(points) + " " + str(currentTime) +"\n")
        f.writelines(gamblers)
        return [1, points, pointsGambled]

#checks the balance of a user

def checkBalance(message):
    author = message.author.id
    f = open("gamblers.txt", 'r')
    gamblers = f.readlines()

    gamblingArray = []
    for gambler in gamblers:
        gamblingArray.append(gambler.split(" "))

    points = -1
    for gamblers in gamblingArray:
        if author == int(gamblers[0]):
            points = int(gamblers[1])

    if points == -1:
        return [0, points]
    elif points != -1:
        return [1, points]



