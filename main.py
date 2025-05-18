#Migael du Preez sat with us did nothing, Andrew Kim, and Haruki Hirata 
import random,diceFaces
import time
import os

#VARS
UNDERLINE = '\033[4m'
RED = '\033[31m'
RESET = '\033[0m'
GREEN = '\033[32m'
BLUE = '\x1b[34m'
GOLD = "\033[38;5;220m"
maxRolls=3
currentRound=1
lengthScoreCard=0
gameHasEnded=False
colors = [196, 202, 208, 214, 220, 190, 46, 51, 21, 93, 129, 201]
#LISTS & DICTIONARIES
rollValues ={'1':100, '2':2, '3':3, '4':4, '5': 5, '6':60}
chips={'PC1':0, 'PC2':0, 'PC3':0} # we shbould prob change the names
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
        if input1.capitalize()=='Y' or input1.capitalize()=='N':
            return input1
        else:
            input1=input(f'Sorry, "{input1}" is invalid, please input "Y" or "N": ')

def checkDice(input1): #use to make sure input from player is either d1, d2, d3
    while True: #loop until input is d1 or d2 or d3
            # Normalize input
            cleaned = input1.replace(' ', '').upper()
    
            if cleaned == 'ALL':
                return 'ALL'
            
            # Split on commas after removing spaces
            parts = cleaned.split(',')

            # Allow combinations of D1, D2, D3 only
            valid_parts = {'D1', 'D2', 'D3'}
            if all(part in valid_parts for part in parts) and len(parts) == len(set(parts)):
                return ','.join(parts)  # Return cleaned and standardized version
            else:
                input1=input(f'Sorry, "{input1}" is invalid, please input "ALL" to reroll all the dice or specify which one (eg. "D1" or "D1 D2" or "D3,D1" etc): ')


#get rid of ts ts so bad
def rainbow_name(winner):
    while True:
        for i in range(len(colors)):
            #os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
            color = f"\033[38;5;{colors[i % len(colors)]}m"
            reset = "\033[0m"
            print(' '*(lengthScoreCard//2-(len(winner)+9)//2)+f'{GOLD}╔'+'='*(len(str(currentRound))+8)+'╗')
            print(f"{GOLD}║{RESET} {color} {winner}{reset}{GOLD}  ║{reset}")
            print(' '*(lengthScoreCard//2-(len(winner)+9)//2)+f'{GOLD}╚'+'='*(len(str(currentRound))+8)+'╝')

            time.sleep(0.1)

def endGameCheck(winner):#check if any player hits 0 points and wins
    global gameHasEnded
    if any(chips[player]<=0 for player in chips):
        scoreCard()
        print('FINAL WINNER',winner)
        #rainbow_name(winner) #PLACEHOLDER
        #ADD WHO HAS WON NICE MESSAGE @HARUKI
    gameHasEnded=True


#GOT TO CHECK IF THERES MORE THAN 2 THAT ARE TIED HAVE NOT IMPLEMENTED
def tieBreaker(pair1, pair2, isMax): #decide what to do at a tie
    #Coin flip which way it goes
    name1, points1 = pair1
    name2, points2 = pair2

    if points1!=points2: #if there is not a tie
        return name1 if ((points1 > points2) == bool(isMax)) else name2
    else:
        return random.choice([name1, name2])

def calculation(roll):
    if sorted(roll)==[4,5,6]: #POCO
        print('Poco!')
        return 9999 #too high value to be reached otherwise
    elif len(set(roll))==1: #Three-of-a-kind
        print(f'Three-of-a-kind ({roll[0]})')
        return int(''.join(str(die) for die in roll)+(str(roll[0]))) #6666 or 5555 etc (too high to reach)
    elif sorted(roll)==[1,2,3]: #LOCO
        print("LoCo!")
        return 1000
    else:
        total = sum(rollValues.get(str(die), 0) for die in roll) #calculates points added up when not special
        return total

def pointAddition(): # calculate total ammount of points and convert to chips
    global botRolls1,botRolls2,botRolls3,playerRoll,chips
    roundPoints['PC1']=calculation(botRolls1)
    roundPoints['PC2']=calculation(botRolls2)
    roundPoints['PC3']=calculation(botRolls3)
    roundPoints[name]=calculation(playerRoll) #player points
    print(roundPoints)
    sorted_players = sorted(roundPoints.items(), key=lambda x: x[1])
    #Loser
    loser=tieBreaker(sorted_players[0], sorted_players[1], isMax=0)
    #Winner
    winner=tieBreaker(sorted_players[2], sorted_players[3], isMax=1)

    print('Winner:',winner,roundPoints[winner])
    print('Loser:',loser,roundPoints[loser])

    # Determine base transfer amount
    if roundPoints[winner] == 9999:  # Poco
        print('POCO')
        transfer_amount = 4
    elif roundPoints[winner] in (6666, 5555, 4444, 3333, 2222, 1111):  # Three-of-a-kind
        print('THREE OF KIND')
        transfer_amount = 3
    elif roundPoints[winner] == 1000:  # LoCo
        print('LOCO')
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
    
    for player in chips: #so the player's points doesnt show as negative
        if chips[player] <= 0:
            endGameCheck(winner)
            chips[player] = 0

def rollOrder(): #randomly decideds which order players roll dice in each round 
    random.shuffle(playerOrder)
    return playerOrder


def roll3Bot1(maxRolls):
    global botRolls1
    tempRolls=maxRolls
    botRolls1 = [random.randint(1, 6) for _ in range(3)]
    tempRolls-=1
    return tempRolls + 1

def roll3Bot2(maxRolls):
    global botRolls2
    tempRolls=maxRolls
    botRolls2 = [random.randint(1, 6) for _ in range(3)]
    tempRolls-=1
    return tempRolls + 1

def roll3Bot3(maxRolls):
    global botRolls3
    tempRolls=maxRolls
    botRolls3 = [random.randint(1, 6) for _ in range(3)]
    tempRolls-=1
    return tempRolls + 1

def roll3(maxRolls): #when all 3 dies are rolled together, make it look nice
    global playerRoll
    rollAgain=0
    playerRoll=[]
    playerRoll = [random.randint(1, 6) for _ in range(3)]
    print("You Rolled:",playerRoll) #replace later with actual dice faces and should we total it up for players or have them calculate and only we calc once they accept it?
    diceFaces.getDiceFace(playerRoll)
    print(f'You have {BLUE}{maxRolls}{RESET} rolls left.') if maxRolls!=1 else print(f'You have {BLUE}{maxRolls}{RESET} roll left.')
    if checkYN(input('Would you like to roll again? (Y/N) '))=='Y':
        rollAgain==1
    
    for i in range(maxRolls):
        if rollAgain==1: #if rollAgain==1 then let them reroll
            rollAgain=0
            rerollers=checkDice('input "ALL" to reroll all the dice or specify which one eg. "D1" or "D1 D2" or "D3,D1" etc) ')
            if 'D1' in rerollers:
                playerRoll[0]=random.randint(1,6)
            if 'D2' in rerollers:
                playerRoll[1]=random.randint(1,6)
            if 'D3' in rerollers:
                playerRoll[2]=random.randint(1,6)
            else: 
                playerRoll = [random.randint(1, 6) for _ in range(3)]
            
            maxRolls-=1
    return maxRolls

            


def scoreCard(): #Displays score after each round
    print('+' + '-' * lengthScoreCard + '+')
    print('|',end=' ')
    for key, value in sorted(chips.items(), key=lambda item: item[1]):
        if key==name:
            print(f'{GREEN}|{key}: {value}|{RESET}', end=' ')
        else:
            print(f'|{key}: {value}|', end=' ')
    print('|')
    print('+' + '-' * lengthScoreCard + '+\n')

def newRoundCard(currentRound,lengthScoreCard): #perfect box to fit new round box it and centered above scorecared (andrew check the math here)
    print(' '*(lengthScoreCard//2-(len(str(currentRound))+9)//2)+'+'+'-'*(len(str(currentRound))+8)+'+')
    print(' '*(lengthScoreCard//2-(len(str(currentRound))+9)//2)+f'| {RED}Round {currentRound}{RESET} |')
    print(' '*(lengthScoreCard//2-(len(str(currentRound))+9)//2)+'+'+'-'*(len(str(currentRound))+8)+'+')

def newRound(currentRound): #order of everything happening
    rollOrder()
    newRoundCard(currentRound,lengthScoreCard)
    scoreCard()
    gameLoop()
    return currentRound+1

def gameLoop():
    global maxRolls
    #Based on the roll order using index of chips items, let each player roll (simulate for bots)
    maxRolls=3
    print('player order:', playerOrder) # change to names

    for player in playerOrder:
        if player==1:
            print("P1 turn")
            maxRolls=roll3Bot1(maxRolls)
            print(botRolls1)
            diceFaces.getDiceFace(botRolls1)
        elif player==2:
            print("P2 turn")
            maxRolls=roll3Bot2(maxRolls)
            print(botRolls2)
            diceFaces.getDiceFace(botRolls2)
        elif player==3:
            print("P3 turn")
            maxRolls=roll3Bot3(maxRolls)
            print(botRolls3)
            diceFaces.getDiceFace(botRolls3)
        else:
            print("It is your turn!")
            maxRolls=roll3(maxRolls)
            
    pointAddition()
    
    

#START
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

#need this after the name var maybe not idk we gotta move this or optimize
lengthScoreCard = len(name) + (len(str(chipStart)) * 4) + 30
roundPoints={'PC1':0, 'PC2':0, 'PC3':0, name:0} #indiv points every round, gets reset


while gameHasEnded==False: #keep looping through games until gameend func triggered
    currentRound=newRound(currentRound)
