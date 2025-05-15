#Migael du Preez, Andrew Kim, and Haruki Hirata sat with us did nothing
import random

#VARS
UNDERLINE = '\033[4m'
RED = '\033[31m'
RESET = '\033[0m'
GREEN = '\033[32m'
BLUE = '\x1b[34m'
maxRolls= 3
currentRound=1
lengthScoreCard=0
#LISTS & DICTIONARIES
rollValues ={'1':100, '2':2, '3':3, '4':4, '5': 5, '6':60}
chips={'PC1':0, 'PC2':0, 'PC3':0} # we shbould prob change the names
playerRoll=[]
playerOrder=[1,2,3,4]



#FUNCTIONS
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


def rollOrder(): #randomly decideds which order players roll dice in each round 
    random.shuffle(playerOrder)
    return playerOrder

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
        playerRoll.extend([random.randint(1,6),random.randint(1,6),random.randint(1,6)])
        print("ROLLS:",playerRoll) #replace later with actual dice faces and should we total it up for players or have them calculate and only we calc once they accept it?
        print(f'You have {BLUE}{tempRolls}{RESET} rolls left.') if tempRolls!=1 else print(f'You have {BLUE}{tempRolls}{RESET} roll left.')

    return tempRolls+1

def scoreCard(): #Displays score after each round
    print('+' + '-' * lengthScoreCard + '+')
    print('|',end=' ')
    for key, value in sorted(chips.items(), key=lambda item: item[1], reverse=True):
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
    #gameloop here
    gameLoop()
    return currentRound+1

def gameLoop():
    global maxRolls
    #Based on the roll order using index of chips items, let each player roll (simulate for bots)
    print('player order:', playerOrder) # change to names
    for i in range(4): #LOOP THROUGH ALL PLAYERS, SIMULATE NPCS HERE
        if playerOrder[i-1]==4: #run until players turn
            #PLAYER'S TURN
            print("It is your turn!")
            maxRolls=roll3(maxRolls)
            print(f"Your final roll: {playerRoll}")
            

    



#START
intro = input('Welcome to PocoLoco!\nWould you like to read the instructions? (Y/N) ')
if checkYN(intro)=='Y':
    #print instrutions here
    print('instructions filler') #maybe do a .txt file here and we do the open() thing?
name = input('What is your name? ')
chipStartInput = input('How many chips do you want everyone to start with? ')

#add player and set chip starting ammount
chipStart=checkInt(chipStartInput)
for chip in chips:
    chips[chip]=chipStart
chips[name]=chipStart

#need this after the name var maybe not idk we gotta move this or optimize
lengthScoreCard = len(name) + (len(str(chipStart)) * 4) + 30


for i in range(7): #similuate 7 rounds for now
    currentRound =newRound(currentRound)
