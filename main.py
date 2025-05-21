#Migael, Andrew, Haruki (a bit)
import random,diceFaces
import time
import os

#add logic for optimal bots, timing, formatting

#VARS
UNDERLINE = '\033[4m'
RED = '\033[31m'
RESET = '\033[0m'
GREEN = '\033[32m'
BLUE = '\x1b[34m'
GOLD = "\033[38;5;220m"
DARK_GRAY = "\033[1;30m"
PINK = '\x1b[38;5;13m'
maxRolls=3
currentRound=1
lengthScoreCard=0
gameHasEnded=False
colors = [196, 202, 208, 214, 220, 190, 46, 51, 21, 93, 129, 201]
#LISTS & DICTIONARIES
rollValues ={'1':100, '2':2, '3':3, '4':4, '5': 5, '6':60}
chips={'PC1':0, 'PC2':0, 'PC3':0}
playerRoll=[]
playerOrder=[1,2,3,4]
botRolls1=[]
botRolls2=[]
botRolls3=[]

#FUNCTIONS
def instructions():
    instructions_file = open('instructions.txt')
    for line in instructions_file:
        print(line.strip())
    
def checkInt(input1): #use to make sure input from player is an int and returns an int
    while True: #loop until input is int
        try:
            input1=int(input1)
            return input1
        except ValueError:
            input1=input(f'Sorry, "{input1}" is invalid, please input an integer: ')

def checkYN(input1): #use to make sure input from player is either a Y or N and returns it
    while True: #loop until input is Y or N
        if input1.upper()=='Y' or input1.upper()=='N':
            return input1.upper()
        else:
            input1=input(f'Sorry, "{input1}" is invalid, please input "Y" or "N": ')

def checkDice(input1): #use to make sure input from player is either d1, d2, d3
    while True: #loop until input is d1 or d2 or d3
            # Normalize input
            cleaned = input1.upper().replace(',',' ').split()
    
            if cleaned == ['ALL']:
                return 'ALL'

            # Allow combinations of D1, D2, D3 etc
            valid_parts = {'D1', 'D2', 'D3'}
            if all(part in valid_parts for part in cleaned) and len(cleaned) == len(set(cleaned)):
                return ','.join(cleaned)  # Return cleaned and standardized version
            else:
                input1=input(f'Sorry, "{input1}" is invalid, please input "ALL" to reroll all the dice or specify which one (eg. "D1" or "D1 D2" or "D3,D1" etc): ')


def rainbow_name(winner):
    start_time = time.time()
    duration = 2
    while True:
        if time.time() - start_time > duration:
            break
        for i in range(len(colors)):
            os.system('cls' if os.name == 'nt' else 'clear') # Clear screen to make the rainbow loop work
            color = f"\033[38;5;{colors[i % len(colors)]}m"
            print(f"{' '*(lengthScoreCard//2-(len(winner)+9)//2)}{GOLD}╔{'='*(len(winner)+8)}╗")
            print(f"{' '*(lengthScoreCard//2-(len(winner)+9)//2)}║{' '*(((len(winner)+8)//2)-(len(winner)//2))}{color}{winner}{GOLD}{' '*(((len(winner)+8)//2)-(len(winner)//2))}║")
            print(f"{' '*(lengthScoreCard//2-(len(winner)+9)//2)}{GOLD}╚{'='*(len(winner)+8)}╝{RESET}")
            time.sleep(0.1)
    scoreCard()
        

def endGameCheck(winner):#check if any player hits 0 points and wins
    global gameHasEnded
    if any(chips[player]<=0 for player in chips):
        scoreCard()
        rainbow_name(winner) 
        gameHasEnded=True


#GOT TO CHECK IF THERES MORE THAN 2 THAT ARE TIED | HAVE NOT IMPLEMENTED
def tieBreaker(pair1, pair2, isMax): #decide what to do at a tie
    #Coin flip which way it goes
    name1, points1 = pair1
    name2, points2 = pair2

    if points1!=points2: #if there is not a tie
        return name1 if ((points1 > points2) == bool(isMax)) else name2 #return the higher value if looking for higher, return lower if looking for lower
    else:
        return random.choice([name1, name2]) #random choice if they are the same

def calculation(roll):
    if sorted(roll)==[4,5,6]: #POCO
        return 9999 #too high value to be reached otherwise
    elif len(set(roll))==1: #Three-of-a-kind
        # print(f'Three-of-a-kind! ({roll[0]})')
        return int(''.join(str(die) for die in roll)+(str(roll[0]))) #6666 or 5555 etc (too high to reach)
    elif sorted(roll)==[1,2,3]: #LOCO
        return 1000
    else:
        total = sum(rollValues.get(str(die), 0) for die in roll) #calculates points added up when not special
        return total

def pointAddition(): # calculate total ammount of points and convert to chips
    global botRolls1,botRolls2,botRolls3,playerRoll,chips, lengthScoreCard
    roundPoints['PC1']=calculation(botRolls1)
    roundPoints['PC2']=calculation(botRolls2)
    roundPoints['PC3']=calculation(botRolls3)
    roundPoints[name]=calculation(playerRoll) #player points
    roundScoreCard()
    sorted_players = sorted(roundPoints.items(), key=lambda x: x[1])
    #Loser
    loser=tieBreaker(sorted_players[0], sorted_players[1], isMax=0)
    #Winner
    winner=tieBreaker(sorted_players[2], sorted_players[3], isMax=1)

    winnerLoserCard('Winner: ',winner,lengthScoreCard)
    winnerLoserCard('Loser: ',loser,lengthScoreCard)
    print()
    print()

    # Determine base transfer amount
    if roundPoints[winner] == 9999:  # Poco
        transfer_amount = 4
    elif roundPoints[winner] in (6666, 5555, 4444, 3333, 2222, 1111):  # Three-of-a-kind
        transfer_amount = 3
    elif roundPoints[winner] == 1000:  # LoCo
        transfer_amount = 2
    else:
        transfer_amount = 1

    # Winner gives chips to loser
    chips[winner] -= transfer_amount
    chips[loser] += transfer_amount

    # Two middle players give the same amount to loser
    all_players = list(chips.keys())
    middle_players = [p for p in all_players if p != winner and p != loser]

    for player in middle_players: #transers middle players
        chips[player] -= transfer_amount
        chips[loser] += transfer_amount
    
    # Ensure no negative chip values
    for player in chips:
        if chips[player] < 0:
            chips[player] = 0

    # Check for game-ending condition
    for player in chips:
        if chips[player] == 0:
            endGameCheck(player)
            break  # stop checking once game has ended
    lengthScoreCard = len(name) + chipUpdate() + 30


def rollOrder(): #randomly decides which order players roll dice in each round 
    random.shuffle(playerOrder)
    return playerOrder

def isGoodRoll(roll): #check if bot should reroll
    return sorted(roll) in [[4,5,6], [1,2,3]] or len(set(roll)) == 1 or 1 in roll

def roll3Bot1(maxRolls):
    global botRolls1
    rolls_left = maxRolls
    rolls_used = 1
    botRolls1 = [random.randint(1, 6) for _ in range(3)]
    print(f"P1 Roll {rolls_used}: {botRolls1}")
    checkSpecial(botRolls1)
    diceFaces.getDiceFace(botRolls1)
    time.sleep(1)
    while rolls_left > 1 and not isGoodRoll(botRolls1):
        rolls_left -= 1
        rolls_used += 1
        botRolls1 = [random.randint(1, 6) for _ in range(3)]
        print(f"P1 Roll {rolls_used}: {botRolls1}")
        checkSpecial(botRolls1)
        diceFaces.getDiceFace(botRolls1)
        time.sleep(1)
    return botRolls1, rolls_used

def roll3Bot2(maxRolls):
    global botRolls2
    rolls_left = maxRolls
    rolls_used = 1
    botRolls2 = [random.randint(1, 6) for _ in range(3)]
    print(f"P2 Roll {rolls_used}: {botRolls2}")
    checkSpecial(botRolls2)
    diceFaces.getDiceFace(botRolls2)
    time.sleep(1)
    while rolls_left > 1 and not isGoodRoll(botRolls2):
        rolls_left -= 1
        rolls_used += 1
        botRolls2 = [random.randint(1, 6) for _ in range(3)]
        print(f"P2 Roll {rolls_used}: {botRolls2}")
        checkSpecial(botRolls2)
        diceFaces.getDiceFace(botRolls2)
        time.sleep(1)
    return botRolls2, rolls_used

def roll3Bot3(maxRolls):
    global botRolls3
    rolls_left = maxRolls
    rolls_used = 1
    botRolls3 = [random.randint(1, 6) for _ in range(3)]
    print(f"P3 Roll {rolls_used}: {botRolls3}")
    checkSpecial(botRolls3)
    diceFaces.getDiceFace(botRolls3)
    time.sleep(1)
    while rolls_left > 1 and not isGoodRoll(botRolls3):
        rolls_left -= 1
        rolls_used += 1
        botRolls3 = [random.randint(1, 6) for _ in range(3)]
        print(f"P3 Roll {rolls_used}: {botRolls3}")
        checkSpecial(botRolls3)
        diceFaces.getDiceFace(botRolls3)
        time.sleep(1)
    return botRolls3, rolls_used

def roll3(maxRolls): #when all 3 dice are rolled together, make it look nice
    global playerRoll
    playerRoll = [random.randint(1, 6) for _ in range(3)]
    print("You Rolled:")
    print(playerRoll)
    checkSpecial(playerRoll)
    diceFaces.getDiceFace(playerRoll)
    rolls_left = maxRolls
    rolls_used = 1
    while rolls_left > 1:
        print(f'You have {BLUE}{rolls_left-1}{RESET} roll{"s" if rolls_left-1 != 1 else ""} left.')
        if checkYN(input(f'{UNDERLINE}Would you like to roll again? (Y/N):{RESET} ')) == 'Y':
            rolls_left -= 1
            rolls_used += 1
            rerollers = checkDice(input(f'\n{UNDERLINE}Which would you like to reroll?{RESET}\nInput "ALL" to reroll all the dice or specify which one (eg. "D1" or "D1 D2" or "D3,D1" etc.): '))
            if rerollers == 'ALL':
                playerRoll = [random.randint(1, 6) for _ in range(3)]
            else:
                if 'D1' in rerollers:
                    playerRoll[0] = random.randint(1, 6)
                if 'D2' in rerollers:
                    playerRoll[1] = random.randint(1, 6)
                if 'D3' in rerollers:
                    playerRoll[2] = random.randint(1, 6)
            print("You Rolled:")
            diceFaces.getDiceFace(playerRoll)
        else:
            break
    return rolls_used

            

def scoreCard(): #Displays score after each round
    print('+' + '-' * lengthScoreCard + '+')
    print('|',end=' ')
    count=0
    for key, value in sorted(chips.items(), key=lambda item: item[1]):
        if key==name:
            print(f'{GREEN}|{key}: {value}|{RESET}', end=' ')
            count+=len(f'{GREEN}|{key}: {value}|{RESET} ')
        else:
            print(f'{DARK_GRAY}|{key}: {value}|{RESET}', end=' ')
            count+=len(f'{DARK_GRAY}|{key}: {value}|{RESET} ')

    gap=' '*(lengthScoreCard-count)
    print(f'{gap}|')
    print('+' + '-' * lengthScoreCard + '+')


def roundScoreCard():
    print()
    # Build the score line with color and without color for measuring
    score_line_colored = ""
    score_line_plain = ""
    for key, value in sorted(roundPoints.items(), key=lambda item: item[1], reverse=True):
        # Format special scores
        if value == 9999:
            display = "POCO"
        elif value == 1000:
            display = "LOCO"
        elif value in (6666, 5555, 4444, 3333, 2222, 1111):
            display = "3-OF-A-KIND"
        else:
            display = str(value)
        part = f'|{key}: {display}| '
        if key == name:
            score_line_colored += f'{GREEN}{part}{RESET}'
        else:
            score_line_colored += f'{DARK_GRAY}{part}{RESET}'
        score_line_plain += part
    score_line_colored = score_line_colored.rstrip()
    score_line_plain = score_line_plain.rstrip()

    # Calculate box width based on plain (visible) score line
    score_box_width = max(30, len(score_line_plain) + 2)  # +2 for padding

    # Center "ROUND SCORE" above the box
    label = "ROUND SCORE"
    label_line = ' ' * ((score_box_width // 2) - (len(label) // 2)) + f"{PINK}{label}{RESET}"
    print(label_line)
    print('+' + '-' * score_box_width + '+')
    print('| ' + score_line_colored + ' ' * (score_box_width - len(score_line_plain) - 2) + '|')
    print('+' + '-' * score_box_width + '+')

def newRoundCard(currentRound,lengthScoreCard): #box containing round number, centered above scorecared
    print(' '*(lengthScoreCard//2-(len(str(currentRound))+9)//2)+'+'+'-'*(len(str(currentRound))+8)+'+')
    print(' '*(lengthScoreCard//2-(len(str(currentRound))+9)//2)+f'| {RED}Round {currentRound}{RESET} |')
    print(' '*(lengthScoreCard//2-(len(str(currentRound))+9)//2)+'+'+'-'*(len(str(currentRound))+8)+'+')

def newRound(currentRound): #order of everything happening
    rollOrder()
    newRoundCard(currentRound,lengthScoreCard)
    scoreCard()
    time.sleep(3)
    gameLoop()
    return currentRound+1

def gameLoop():
    global maxRolls
    maxRolls = 3  # Reset at the start of each round

    for player in playerOrder:
        if player == 1:
            print(f"\n{DARK_GRAY}P1 TURN!{RESET}\nP1 Rolled:")
            botRolls1, rolls_used = roll3Bot1(maxRolls)
            maxRolls = rolls_used
        elif player == 2:
            print(f"\n{DARK_GRAY}P2 TURN!{RESET}\nP2 Rolled:")
            botRolls2, rolls_used = roll3Bot2(maxRolls)
            maxRolls = rolls_used
        elif player == 3:
            print(f"\n{DARK_GRAY}P3 TURN!{RESET}\nP3 Rolled:")
            botRolls3, rolls_used = roll3Bot3(maxRolls)
            maxRolls = rolls_used
        else:
            print(f"\n{GREEN}IT IS YOUR TURN!{RESET}")
            rolls_used = roll3(maxRolls)
            maxRolls = rolls_used

    pointAddition()


def chipUpdate(): #updates length of all the chips combined to use in the lengthScoreCard var
    global chips
    count=0
    chips_list=[]
    for item in chips:
        chips_list.append(item)
    
    for item in chips_list:
        count+=(len(str(chips[item])))
    return count

def checkSpecial(roll): #checks if the roll is 'POCO', 'LOCO', or 'THREE OF A KIND'. If it is, print accordingly in boxes. 
    if sorted(roll)==[4,5,6]:
        specialRollCard('PoCo!',lengthScoreCard)
    elif len(set(roll))==1:
        specialRollCard(f'3-OF-A-KIND!',lengthScoreCard)
    elif sorted(roll)==[1,2,3]:
        specialRollCard('LoCo!',lengthScoreCard)

def specialRollCard(specialRoll,lengthScoreCard): #box containing special roll, centered above dice
    print(' '*(lengthScoreCard//2-(len(specialRoll)+9)//2)+'+'+'-'*(len(specialRoll)+2)+'+')
    print(' '*(lengthScoreCard//2-(len(specialRoll)+9)//2)+f'| {PINK}{specialRoll}{RESET} |')
    print(' '*(lengthScoreCard//2-(len(specialRoll)+9)//2)+'+'+'-'*(len(specialRoll)+2)+'+')

def winnerLoserCard(status,player,lengthScoreCard): #box for winner/loser, centered at the end of every round
    card_width = len(status+player) + 4
    pad = (lengthScoreCard - card_width) // 2
    print(' ' * pad + '+' + '-' * (card_width - 2) + '+')
    print(' ' * pad + f'| {PINK}{status}{player}{RESET} |')
    print(' ' * pad + '+' + '-' * (card_width - 2) + '+')

   



#PROGRAM START
intro = input(f'{RESET}Welcome to PocoLoco!\nWould you like to read the instructions? (Y/N) ')
if checkYN(intro)=='Y':
    instructions()
name = input('What is your name? ')
chipStartInput = input('How many chips do you want everyone to start with? ')

#add player and set chip starting ammount
chipStart=checkInt(chipStartInput)
while chipStart<=0:
    chipStartInput=input('The chips to start with needs to be greater than 0: ')
    chipStart=checkInt(chipStartInput)

for chip in chips:
    chips[chip]=chipStart
chips[name]=chipStart

lengthScoreCard = len(name) + chipUpdate() + 30
roundPoints={'PC1':0, 'PC2':0, 'PC3':0, name:0} #indiv points every round, gets reset


while gameHasEnded==False: #keep looping through games until gameend func triggered
    currentRound=newRound(currentRound)