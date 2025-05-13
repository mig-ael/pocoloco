#Migael du Preez, Andrew Kim, and Haruki sat with us did nothing
import random,diceFaces
intro = input('Welcome to PocoLoco!\nWould you like to read the instructions? (y/n) ')
if intro.capitalize()=='Y':
    #print instrutions here
    print('hi')

name = input('What is your name? ')
chipStart = input('How many chips do you want everyone to start with? ')
chips={'PC1':chipStart, 'PC2':chipStart, 'PC3':chipStart}
chips[name] = 10

while True:
    rollValues ={'1':100, '2':2, '3':3, '4':4, '5': 5, '6':60}
    
    playerRoll1=[]
    playerRoll1.append(random.randint(1,6))*3
    print(playerRoll1)
