#Migael du Preez sat with us did nothing, Andrew Kim, and Haruki Hirata 
import random,diceFaces

#VARS
UNDERLINE = '\033[4m'
RED = '\033[31m'
RESET = '\033[0m'
GREEN = '\033[32m'
BLUE = '\x1b[34m'
maxRolls=3
currentRound=1
lengthScoreCard=0
gameHasEnded=False
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
    print(open('instructions.txt', 'r'))
    
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

def endGameCheck():#check if any player hits 0 points and wins
    global gameHasEnded
    if any(chips[player]<=0 for player in chips):
        print("GAME OVER") #PLACEHOLDER
    gameHasEnded=True

#GOT TO CHECK IF THERES MORE THAN 2 THAT ARE TIED HAVE NOT IMPLEMENTED
def tieBreaker(points1,points2,isMax): #decide what to do at a tie
    #Coin flip which way it goes
    if points1!=points2: #if there is not a tie
        if isMax==1: #1 is True
            return max(points1,points2)
        else:
            return min(points1,points2)
    else:
        return random.choice([points1,points2])

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
    global botRolls1,botRolls2,botRolls3,playerRoll
    roundPoints['PC1']=calculation(botRolls1)
    roundPoints['PC2']=calculation(botRolls2)
    roundPoints['PC3']=calculation(botRolls3)
    roundPoints[name]=calculation(playerRoll) #player points
    print(roundPoints)
    #Loser
    loser=tieBreaker(sorted(roundPoints)[0],sorted(roundPoints)[1],0)
    #Winner
    winner=tieBreaker(sorted(roundPoints)[2],sorted(roundPoints)[3],1)

    print('Winner:',winner,roundPoints[winner])
    print('Loser:',loser,roundPoints[loser])


    if roundPoints[winner]=='9999': #check if poco
        chips[winner]-=4
        chips[loser]+=4
    elif roundPoints[winner] in ('6666', '5555', '4444', '3333', '2222', '1111'): #check if three-of-a-kind
        chips[winner]-=3
        chips[loser]+=3
    elif roundPoints[winner]==1000: #chgeck if loco
        chips[winner]-=2
        chips[winner]+=2
    else:
        chips[winner]-=1
        chips[loser]+=1

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
    tempRolls=maxRolls
    while tempRolls>0: #roll until previous maxrolls
        
        if tempRolls!=maxRolls:
            rerollReq=input("Would you like to roll again? (Y/N) ")
            if checkYN(rerollReq)=='N':
                break
        tempRolls-=1
        playerRoll=[]
        playerRoll = [random.randint(1, 6) for _ in range(3)]
        print("You Rolled:",playerRoll) #replace later with actual dice faces and should we total it up for players or have them calculate and only we calc once they accept it?
        
        print(f'You have {BLUE}{tempRolls}{RESET} rolls left.') if tempRolls!=1 else print(f'You have {BLUE}{tempRolls}{RESET} roll left.')

    return tempRolls+1

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

def newRound(currentRound): #We should prob loop this everytime newRound happens
    rollOrder()
    newRoundCard(currentRound,lengthScoreCard)
    scoreCard()
    gameLoop()
    endGameCheck()
    return currentRound+1

def gameLoop():
    global maxRolls
    #Based on the roll order using index of chips items, let each player roll (simulate for bots)

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
            diceFaces.getDiceFace(playerRoll)
    pointAddition()
    
    

#START
intro = input('Welcome to PocoLoco!\nWould you like to read the instructions? (Y/N) ')
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


for i in range(7): #similuate 7 rounds for now (change to score hits 0 later)
    currentRound=newRound(currentRound)
