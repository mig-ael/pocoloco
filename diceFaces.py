def getDiceFace(lst):


    diceTB15="+-------+\t"  
    dice12=  "|       |\t"   #last number is the layer number, dice are made of 5 layers, top and bottom the same
    dice232= "| O     |\t"
    dice4562="| O   O |\t"
    dice1353="|   O   |\t"
    dice243= "|       |\t"
    dice63=  "| O   O |\t"
    dice14=  "|       |\t"
    dice234= "|     O |\t"
    dice4564="| O   O |\t"
    dice_layers = {
        1: [dice12, dice1353, dice14],    #dictionaries of lists
        2: [dice232, dice243, dice234],
        3: [dice232, dice1353, dice234],
        4: [dice4562, dice243, dice4564],
        5: [dice4562, dice1353, dice4564],
        6: [dice4562, dice63, dice4564],
    }
    def print_dice_faces(lst):
        print(diceTB15 * 3)
        for i in range(3):
            line = ''
            for n in lst:
                line += dice_layers[n][i]
            print(line)
        print(diceTB15 * 3)
    print_dice_faces(lst)
