import random
import math

#create a human player
class HumanPlayer:
    def __init__(self, letter):
        self.letter = letter

    def getMove(self, game):
        valSquare = False
        val = None
        #create a while loop till the square gets occupied
        while not valSquare:
            square = input(f"{self.letter}'s turn. Input(0-8): ")
            try:
                val = int(square)
                #check the square is empty or not if empty set the square to occupied otherwise raise error
                if val not in game.availableMoves():
                    raise ValueError
                valSquare = True
            except ValueError:
                print("Invalid Input")
        return val

#create computer player(easy)
class ComputerPlayer1:
    def __init__(self, letter):
        self.letter = letter

    def getMove(self, game):
        #randomly choose from available moves
        square = random.choice(game.availableMoves())
        return square

#create computer player(hard)
class ComputerPlayer2:
    def __init__(self, letter):
        self.letter = letter

    def getMove(self, game):
        #first move choose randomly and other moves using minimax algorithm
        if len(game.availableMoves()) == 9:
            square = random.choice(game.availableMoves())
        else:
            square = self.miniMax(game, self.letter)["position"]
        return square

    def miniMax(self, game, player):
        maxPlayer = self.letter
        if player == "X":
            otherPlayer = "O"
        else:
            otherPlayer = "X"
        #check previous move is winner or tie
        if game.currWinner == otherPlayer:
            return {"position" : None, "score" : 1 * (game.numEmptySquares()+1) if otherPlayer == maxPlayer else (-1) * (game.numEmptySquares()+1)}
        elif not game.emptySquares():
            return {"position" : None, "score" : 0}
        #initialize max and min
        if player == maxPlayer:
            best = {"position" : None, "score" : -math.inf}
        else:
            best = {"position" : None, "score" : math.inf}
        #loop using for loop to make move
        for possibleMove in game.availableMoves():
            #loop recursively to reach the depth node
            game.makeMove(possibleMove, player)
            simScore = self.miniMax(game, otherPlayer)
            #undo the move for other possible moves
            game.table[possibleMove] = " "
            game.currWinner = None
            simScore["position"] = possibleMove
            #make changes in dictionary if needed which is maximalize and minimalize
            if maxPlayer == player:
                if simScore["score"] > best["score"]:
                    best = simScore
            else:
                if simScore["score"] < best["score"]:
                    best = simScore
        return best

#create the base (game)
class TicTacToe:
    def __init__(self):
        self.table = [" " for i in range(9)]
        self.currWinner = None
    #create the table 
    def printTable(self):
        a = [self.table[i*3:(i+1)*3] for i in range(3)]
        for row in a:
            print("| " + " | ".join(row) + " |")
    #create the number table
    def printNumTable(self):
        a = [[str(j) for j in range(i*3, (i+1)*3)] for i in range(3)]
        for row in a:
            print("| " + " | ".join(row) + " |")
    #return the squares which have " "
    def availableMoves(self):
        moves = []
        for i, e in enumerate(self.table):
            if e == " ":
                moves.append(i)
        return moves
    #return True if any squares is empty or False
    def emptySquares(self):
        return " " in self.table
    #return number of empty squares
    def numEmptySquares(self):
        return self.table.count(" ")
    #to check winner or not
    def winner(self, square, letter):
        #to check rows
        rowInd = square // 3
        row = self.table[rowInd*3:(rowInd+1)*3]
        if all([a == letter for a in row]):
            return True
        #to check columns
        colInd = square % 3
        col = [self.table[colInd+(i*3)] for i in range(3)]
        if all([a == letter for a in col]):
            return True
        #to check diagonals
        if square % 2 == 0:
            diag1 = [self.table[i] for i in (0, 4, 8)]
            if all([a == letter for a in diag1]):
                return True
            diag2 = [self.table[i] for i in (2, 4, 6)]
            if all([a == letter for a in diag2]):
                return True
        return False
    #check and make a move
    def makeMove(self, square, letter):
        if self.table[square] == " ":
            self.table[square] = letter
            #check the winner and if true set the winner to current letter
            if self.winner(square, letter):
                self.currWinner = letter
            return True
        return False

def play(game, xPlayer, oPlayer, printGame=True):
    if printGame:
        game.printNumTable()
    #initialize letter to X
    letter = "X"
    while game.emptySquares():
        #get the move from respective players
        if letter == "O":
            square = oPlayer.getMove(game)
        else:
            square = xPlayer.getMove(game)
        
        if game.makeMove(square, letter):
            if printGame:
                print(f"{letter} makes a move to {square}")
                game.printTable()
                print()

        if game.currWinner:
            if printGame:
                print(f"{letter} wins!")
            return letter
        
        if letter == "X":
            letter = "O"
        else:
            letter = "X"

    if printGame:
        print("It\'s a tie")

def main():
    print("Welcome to Tic Tac Toe!\n1. Play Human vs Human\n2. Play Human vs Computer(Easy)\n3. Play Human vs Computer(Hard)\n")
    choice = int(input("Enter your choice: "))
    print(" ")
    if choice == 1:
        game = TicTacToe()
        xPlayer = HumanPlayer("X")
        oPlayer = HumanPlayer("O")
        play(game, xPlayer, oPlayer, printGame=True)
    elif choice == 2:
        game = TicTacToe()
        xPlayer = HumanPlayer("X")
        oPlayer = ComputerPlayer1("O")
        play(game, xPlayer, oPlayer, printGame=True)
    elif choice == 3:
        game = TicTacToe()
        oPlayer = HumanPlayer("O")
        xPlayer = ComputerPlayer2("X")
        play(game, xPlayer, oPlayer, printGame=True)
    else:
        print("Invalid Input")

main()