'''
minimax.py: A quick and dirty implementation of the minimax algorithm
in python, along with a tic-tac-toe game
'''
__author__ = "Vlad Ianculescu"

import numpy as np

#The board and current player variables.
#The current variable takes values -1 and 1
#and the value 1 (human player) always starts
board = np.array([[0] * 3] * 3)
current = 1

#Reset the game
def reset():
    global board, current
    current = 1
    board = np.array([[0] * 3] * 3)

#Print the board
def printBoard():
    print("%s |%s |%s" % tuple(board[0]))
    print("%s |%s |%s" % tuple(board[1]))
    print("%s |%s |%s" % tuple(board[2]))

#Check to see if the game completed and who won
def check():
    '''
    Checks to see if the game completed and who won.
    :returns: The player who won (-1, 1), 2 if draw or 0 if the game is not over yet
    :warning: The function returns 2 when there is a draw and 0 when the game has not ended
    '''
    if 0 not in board:
        return 2

    #Get the sum of each row, column and diagonal
                          #Sum up each column
    res = np.concatenate((np.sum(board, axis = 0),
                          #Sum up each row
                          np.sum(board, axis = 1),
                          #Sum up the main diagonal
                          [np.sum(np.diag(board))],
                          #Sum up the secondary diagonal
                          [np.sum(np.diag(np.fliplr(board)))]))

    #Check to see if any of the players won. If any of the won,
    #one of the sums has to be a 3 or a -3
    if 3 in res:
        return 1
    elif -3 in res:
        return -1

    #Return 0 if the game has not ended yet
    return 0

#Parse the inut given by the player.
def parseInput(inp):
    '''
    Takes a string of the form '%n %n' and returns a tuple of ints.
    Also checks for the borders.
    If the input string is not in the correct format, None is returned
    '''
    try:
        res = int(inp.strip().split()[0]), int(inp.strip().split()[1])

        if res in [(x,y) for x in range(3) for y in range(3)]:
            return res
        return None

    except:
        return None

#Checks if the position is valid
def checkPos(m):
        x,y=m
        if board[x,y] == 0:
             return True
        return False

def place(pos):
    '''
    Checks and places the current player at the specified position. Returns True if
    successful, False otherwise.
    '''
    global current
    if checkPos(pos):
        board[pos[0],pos[1]] = current
        return True
    return False

#Play the game
def play():
    global current
    reset()

    while check() == 0:
        print("Player: %s" % ((3-current)//2,))
        print()
        printBoard()

        if current == 1:
            pos = input()
            pos = parseInput(pos)

            if pos == None:
                print("Please enter the input in the form: 'row column'")
                continue

            if not place(pos):
                print("The position is in use. Please try another one.")
                continue

        else:
            pos = minimax()
            board[pos[0],pos[1]] = -1
            
        current = -current

    if check() == 2:
        print("Draw!")
    else:
        print("Player %s wins!" % ((-check() + 3)//2))
    
    print(check() if check() != 2 else 0)

'''Utility functions for the minimax algorithm'''

#TODO: Optimize the algorithm, especially for the first iteration.
#Maybe try hashing some of the intermediate steps.

#Gets a list of the empty cells in the board
def getEmptyCells():
    global board
    return np.argwhere(board == 0)

#Method that is recursively called to find the best score at each step.
def mmhelper(player):
    global board, current

    #End case: check to see if the game is over
    #and return the score
    if check() != 0:
        if check() == 2:
            return 0
        else:
            return -check()

    #Step case: If the game is not over, loop over the empty cells
    #and recursively call the method. Return the min/max value according
    #to the current step.
    emptyCells = getEmptyCells()
    res = []

    for en in emptyCells:
        board[en[0], en[1]] = player
        res.append((mmhelper(-player), en)) 
        board[en[0], en[1]]=0

    #For the current player, return the max value
    if player == current:
        return max(res, key = lambda x: x[0])[0]
    #For the enemy, return the min value
    else:
        return min(res, key = lambda x: x[0])[0]

#The minimax method to find the best strategy for winning.
#Loop over the empty cells and call the mmhelper method.
#Add the results to an array and return the maximum.
def minimax():
    emptyCells = getEmptyCells()
    res = []
    
    for en in emptyCells:
        board[en[0], en[1]] = current
        res.append((mmhelper(-current), en))
        board[en[0], en[1]] = 0
        
    return max(res, key = lambda x: x[0])[1]

#Main method
if __name__ == "__main__":
    play()
