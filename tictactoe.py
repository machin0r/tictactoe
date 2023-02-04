import random
import sys
sys.setrecursionlimit(20000)

numGames = 7500

theBoard = {'1': ' ', '2': ' ', '3': ' ',
            '4': ' ', '5': ' ', '6': ' ',
            '7': ' ', '8': ' ', '9': ' '}
solutions = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9],
             [1, 5, 9], [3, 5, 7]]  # Chars of the same that fill these win
scoreboard = {}

# This dict is for temporary storage of the posiitons chosen each game
AI1_placement_temp = {'0': '', '1': '', '2': '',
                      '3': '', '4': '', '5': '',
                      '6': '', '7': '', '8': ''}

# This dictionary stores the weighting of each position choice for each turn
# Higher numbers indicated that this choice is more likely to win the game
AI1_full_weighting = {'0': {'1': 0, '2': 0, '3': 0,
                            '4': 0, '5': 0, '6': 0,
                            '7': 0, '8': 0, '9': 0},
                      '1': {'1': 0, '2': 0, '3': 0,
                            '4': 0, '5': 0, '6': 0,
                            '7': 0, '8': 0, '9': 0},
                      '2': {'1': 0, '2': 0, '3': 0,
                            '4': 0, '5': 0, '6': 0,
                            '7': 0, '8': 0, '9': 0},
                      '3': {'1': 0, '2': 0, '3': 0,
                            '4': 0, '5': 0, '6': 0,
                            '7': 0, '8': 0, '9': 0},
                      '4': {'1': 0, '2': 0, '3': 0,
                            '4': 0, '5': 0, '6': 0,
                            '7': 0, '8': 0, '9': 0},
                      '5': {'1': 0, '2': 0, '3': 0,
                            '4': 0, '5': 0, '6': 0,
                            '7': 0, '8': 0, '9': 0},
                      '6': {'1': 0, '2': 0, '3': 0,
                            '4': 0, '5': 0, '6': 0,
                            '7': 0, '8': 0, '9': 0},
                      '7': {'1': 0, '2': 0, '3': 0,
                            '4': 0, '5': 0, '6': 0,
                            '7': 0, '8': 0, '9': 0},
                      '8': {'1': 0, '2': 0, '3': 0,
                            '4': 0, '5': 0, '6': 0,
                            '7': 0, '8': 0, '9': 0}}


# This function creates the game board
def printBoard(board):
    print(board['1'] + '|' + board['2'] + '|' + board['3'])
    print('-+-+-')
    print(board['4'] + '|' + board['5'] + '|' + board['6'])
    print('-+-+-')
    print(board['7'] + '|' + board['8'] + '|' + board['9'])


# This function resets the dictionary holding the game board
def setup():
    for key in sorted(theBoard.keys()):
        theBoard[key] = ' '
    for key in sorted(AI1_placement_temp.keys()):
        AI1_placement_temp[key] = ''


# Displays winner, +1 to score, if not AI ask user for another game
# If it is AI vs. Computer, continues the tournament unti numGames is reached
def winner(cur_player, player1, player2, game_mode, switch_player, gameNo):
    gameNo = gameNo
    gameNo += 1
    switch_player = not switch_player
    if game_mode == 0 and gameNo < numGames:  # Restarts AI if < numGames
        scoreboard[cur_player] += 1
        AI_players(player1, player2, switch_player, gameNo)
    elif game_mode == 0:
        print("Game over!")
        scoreboard[cur_player] += 1
        print("Current score:")
        for k, v in scoreboard.items():
            print(k, ':', v)
        print("--------------------------------------------------------------")
        print(AI1_full_weighting)
        print("-----------------------------------")
    if game_mode == 1 or game_mode == 2:  # Asks the user to play again
        print("Game over! The winner is " + cur_player + "!")
        scoreboard[cur_player] += 1
        print("Current score:")
        for k, v in scoreboard.items():
            print(k, ':', v)
        print("Play again? Y/N?")
        if input().upper() == "Y":
            if game_mode == 1:  # Checks if restarting a 1 or 2 player game
                single_player(player1, player2, switch_player, gameNo)
            elif game_mode == 2:
                two_player(player1, player2, switch_player, gameNo)
        else:
            exit()
    else:
        print(AI1_full_weighting)
        exit()


# Determines what happens when a game is tied.
# If over numGames, the tournament is ended
def tie_game(cur_player, player1, player2, game_mode, switch_player, gameNo):
    gameNo = gameNo
    gameNo += 1
    switch_player = not switch_player
    if game_mode == 0 and gameNo < numGames:  # Restarts AI game if < numGames
        AI_players(player1, player2, switch_player, gameNo)
    elif game_mode == 0:
        print("Game Over!")
        scoreboard[cur_player] += 1
        print("Current score:")
        for k, v in scoreboard.items():
            print(k, ':', v)
        print("--------------------------------------------------------------")
        print(AI1_full_weighting)
        print("-----------------------------------")
    if game_mode == 1 or game_mode == 2:  # Asks the user to play again
        print("It's a tie!")
        print("Current score:")
        for k, v in scoreboard.items():
            print(k, ':', v)
        print("Play again? Y/N?")
        if input().upper() == "Y":
            if game_mode == 1:  # Check if 1 or 2 player
                single_player(player1, player2, switch_player, gameNo)
            elif game_mode == 2:
                two_player(player1, player2, switch_player, gameNo)
        else:
            exit()
    else:
        print(AI1_full_weighting)
        exit()


# This is for two humans to play against each other
def two_player(player1, player2, switch_player, gameNo):
    setup()
    game_mode = 2
    players = {}
    switch_player = switch_player
    if switch_player:
        players[player1] = 'O'
        players[player2] = 'X'
        cur_player = player2
    else:
        players[player1] = 'X'
        players[player2] = 'O'
        cur_player = player1
    count = 0

    while count < 9:
        printBoard(theBoard)
        print("It is " + cur_player + "'s go, you are " + players[cur_player] +
              ". Where do you want to go?")
        move = input()
        if theBoard[move] == ' ':
            theBoard[move] = players[cur_player]  # Adds move to board if legal
            count += 1
        else:
            print("Already taken")
            continue
        # Checks each solution against the board after a turn has been
        # taken to see if it is a winning move
        for sol in solutions:
            if (theBoard[str(sol[0])] == theBoard[str(sol[1])] ==
                    theBoard[str(sol[2])] == players[cur_player]):
                printBoard(theBoard)
                winner(cur_player, player1, player2, game_mode,
                       switch_player, gameNo)
        if cur_player == player1:  # Flips who the current player is
            cur_player = player2
        else:
            cur_player = player1
    tie_game(cur_player, player1, player2, game_mode, switch_player, gameNo)


def single_player(player1, player2, switch_player, gameNo):
    setup()
    game_mode = 1
    # Creates a copy of the board for the computer to pick from,
    # deletes the places that the user and computer have used
    compBoard = theBoard.copy()
    players = {}
    switch_player = switch_player
    if switch_player:
        players[player1] = 'O'
        players[player2] = 'X'
        cur_player = player2
    else:
        players[player1] = 'X'
        players[player2] = 'O'
        cur_player = player1
    count = 0

    while count < 9:
        printBoard(theBoard)

        if cur_player == player2:
            print("It is " + cur_player + "'s go, they are " +
                  players[cur_player] + ".")
            print("Computer is thinking",  end="\r")
            print("Computer is thinking.",  end="\r")
            print("Computer is thinking..",  end="\r")
            print("Computer is thinking...")
            # Get a random selection where the computer can place
            square, value = random.choice(list(compBoard.items()))
            theBoard[square] = players[cur_player]
            del compBoard[square]
            count += 1
        else:
            print("It is " + cur_player + "'s go, you are " +
                  players[cur_player] + ". Where do you want to go?")
            move = input()
            if theBoard[move] == ' ':
                theBoard[move] = players[cur_player]
                count += 1
                del compBoard[move]
            else:
                print("Already taken")
                continue
        for sol in solutions:
            if (theBoard[str(sol[0])] == theBoard[str(sol[1])] ==
                    theBoard[str(sol[2])] == players[cur_player]):
                winner(cur_player, player1, player2, game_mode,
                       switch_player, gameNo)
        if cur_player == player1:
            cur_player = player2
        else:
            cur_player = player1
    tie_game(cur_player, player1, player2, game_mode, switch_player, gameNo)


def AI_players(player1, player2, switch_player, gameNo):
    gameNo = gameNo
    setup()
    square = 0
    game_mode = 0
    # Creates a copy of the board for the computer to pick from,
    # deletes the places that the user and computer have used
    compBoard = theBoard.copy()
    players = {}
    switch_player = switch_player
    if switch_player:
        players[player1] = 'O'
        players[player2] = 'X'
        cur_player = player2
    else:
        players[player1] = 'X'
        players[player2] = 'O'
        cur_player = player1

    count = 0
    while count < 9:
        # Gets the computer selection.
        # If player1, sorts the weighting list for this turn
        # and picks the highest weighted option.
        # player2 is picked randomly
        if cur_player == player1:
            AI1_test = AI1_full_weighting[str(count)]
            AI1_placement_weighting_sorted = sorted(AI1_test.items(),
                                                    key=lambda x: -x[1])
            # Iterates through the highest weighted positions,
            # picking the first that is free on the board
            for pos in AI1_placement_weighting_sorted:
                if theBoard[pos[0]] == ' ':
                    square = pos[0]
                    break
            AI1_placement_temp[str(count)] = square
        elif cur_player == player2:
            square, value = random.choice(list(compBoard.items()))
        theBoard[square] = players[cur_player]
        del compBoard[square]
        count += 1

        for sol in solutions:
            if (theBoard[str(sol[0])] == theBoard[str(sol[1])] ==
                    theBoard[str(sol[2])] == players[cur_player]):
                # If player1 won, +3 to each of the moves played in this game
                # If player1 lost, -1 to each of the moves played in this game
                if cur_player == player1:
                    for key in AI1_placement_temp:
                        if AI1_placement_temp[key] != '':
                            AI1_full_weighting[key][AI1_placement_temp[key]] += 3
                else:
                    for key in AI1_placement_temp:
                        if AI1_placement_temp[key] != '':
                            AI1_full_weighting[key][AI1_placement_temp[key]] -= 1
                winner(cur_player, player1, player2, game_mode,
                       switch_player, gameNo)
        # Switch player turn
        if cur_player == player1:
            cur_player = player2
        else:
            cur_player = player1
    # If a draw, +1 to each of the moves played in this game
    for key in AI1_placement_temp:
        if AI1_placement_temp[key] != '':
            AI1_full_weighting[key][AI1_placement_temp[key]] += 1
    tie_game(cur_player, player1, player2, game_mode, switch_player, gameNo)


def main():
    switch_player = False
    print("AI Game [0], Single player [1] or two player [2]?")
    game_selection = input()
    if game_selection == "0":
        player1 = "Computer1"
        player2 = "Computer2"
        gameNo = 0
        scoreboard[player1] = 0
        scoreboard[player2] = 0
        AI_players(player1, player2, switch_player, gameNo)
    elif game_selection == "1":
        print("Player 1")
        player1 = input("Enter the name : ")
        print("\n")
        player2 = "Computer"
        gameNo = 0
        scoreboard[player1] = 0
        scoreboard[player2] = 0
        single_player(player1, player2, switch_player, gameNo)
    elif game_selection == "2":
        print("Player 1")
        player1 = input("Enter the name : ")
        print("\n")
        print("Player 2")
        player2 = input("Enter the name : ")
        print("\n")
        gameNo = 0
        scoreboard[player1] = 0
        scoreboard[player2] = 0
        two_player(player1, player2, switch_player, gameNo)
    print("MAIN OVER")


if __name__ == '__main__':
    main()
