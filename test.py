import random,diceFaces
name='dog'
roundPoints={'PC1':5, 'PC2':3, 'PC3':1, name:6}


def tieBreaker(points1,points2,isMax): #decide what to do at a tie
    #Coin flip which way it goes
    if points1!=points2: #if there is not a tie
        if isMax==1: #1 is True
            return max(points1,points2)
        else:
            return min(points1,points2)
    else:
        return random.choice(points1,points2)
loser=tieBreaker(sorted(roundPoints)[0],sorted(roundPoints)[1],0)
winner=tieBreaker(sorted(roundPoints)[2],sorted(roundPoints)[3],1)

print(winner)
print(roundPoints[winner])
print()
print(loser)
print(roundPoints[loser])