#Migael du Preez, Andrew Kim, and Haruki Hirata sat with us did nothing
import random

#VARS
UNDERLINE = '\033[4m'
RED = '\033[31m'
RESET = '\033[0m'
GREEN = '\033[32m'
maxRolls= 3
currentRound=1
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

def rollOrder(): #randomly decideds which order players roll dice in each round
    
    random.shuffle(playerOrder)
    return playerOrder
def roll3(): #when all 3 dies are rolled together
    playerRoll=[]
    playerRoll.extend([random.randint(1,6),random.randint(1,6),random.randint(1,6)])
    return playerRoll

def scoreCard(): #Displays score after each round
    lengthScoreCard = len(name) + (len(str(chipStart)) * 4) + 30
    print('\n+' + '-' * lengthScoreCard + '+')
    print('|',end=' ')
    for key, value in sorted(chips.items(), key=lambda item: item[1], reverse=True):
        if key==name:
            print(f'{GREEN}|{key}: {value}|{RESET}', end=' ')
        else:
            print(f'|{key}: {value}|', end=' ')
    print('|')
    print('+' + '-' * lengthScoreCard + '+')
def newRoundCard(currentRound): #perfect box to fit new round box it
    print('\n+'+'-'*(len(str(currentRound))+8)+'+')
    print(f'| {RED}Round {currentRound}{RESET} |')
    print('+'+'-'*(len(str(currentRound))+8)+'+')
def newRound(currentRound): #We should prob loop this everytime newRound happens
    newRoundCard(currentRound)
    #gameloop here
    gameLoop()
    scoreCard()
    return currentRound+1

def gameLoop():
    #Based on the roll order using index of chips items, let each player roll (simulate for bots)
    print('\nroll order:',rollOrder())
    



#START
intro = input('Welcome to PocoLoco!\nWould you like to read the instructions? (y/n) ')
if intro.capitalize()=='Y':
    #print instrutions here
    print('instructions filler') #maybe do a .txt file here and we do the open() thing?
name = input('What is your name? ')
chipStartInput = input('How many chips do you want everyone to start with? ')


chipStart=checkInt(chipStartInput)
for chip in chips:
    chips[chip]=chipStart
chips[name]=chipStart


for i in range(3):
    currentRound =newRound(currentRound)
