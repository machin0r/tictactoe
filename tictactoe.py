import random


class TicTacToe:
    def __init__(self, num_games, training_games):
        self.num_games = num_games
        self.training_games = training_games
        self.cur_game_num = 0

        self.the_board = {'1': ' ', '2': ' ', '3': ' ',
                          '4': ' ', '5': ' ', '6': ' ',
                          '7': ' ', '8': ' ', '9': ' '}
        # Chars of the same that fill these positions win
        self.solutions = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7],
                          [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
        self.scoreboard = {}

        # This dict is for temporary storage of the posiitons chosen each game
        self.AI1_placement_temp = {'0': '', '1': '', '2': '',
                                   '3': '', '4': '', '5': '',
                                   '6': '', '7': '', '8': ''}

        # This dictionary stores the weighting of each position
        # choice for each turn
        # Higher numbers indicated that this choice is more likely
        # to win the game
        self.AI1_full_weighting = {'0': {'1': 0, '2': 0, '3': 0,
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
    def print_board(self, board):
        print(board['1'] + '|' + board['2'] + '|' + board['3'])
        print('-+-+-')
        print(board['4'] + '|' + board['5'] + '|' + board['6'])
        print('-+-+-')
        print(board['7'] + '|' + board['8'] + '|' + board['9'])

    # This function resets the dictionary holding the game board
    def setup(self):
        for key in sorted(self.the_board.keys()):
            self.the_board[key] = ' '
        for key in sorted(self.AI1_placement_temp.keys()):
            self.AI1_placement_temp[key] = ''

    # Handles the end of the game
    #  +1 to score, if there is a winner
    #  If not an AI game ask user for another game
    # If it is AI vs. Computer, continues the tournament unti self.num_games
    def game_over(self, cur_player, player1, player2, game_mode,
                  switch_player, cur_game_num, winner):
        cur_game_num += 1
        switch_player = not switch_player
        if winner:  # If game wasn't a tie, +1 to winner's score
            self.scoreboard[cur_player] += 1
        elif game_mode == 1 or game_mode == 2:  # Asks the user to play again
            print("Game over! The winner is " + cur_player + "!")
            print("Current score:")
            for k, v in self.scoreboard.items():
                print(k, ':', v)
            print("Play again? Y/N?")
            if input().upper() == "Y":
                if game_mode == 1:  # Checks if restarting a 1 or 2 player game
                    self.single_player(player1, player2, switch_player,
                                       cur_game_num)
                elif game_mode == 2:
                    self.two_player(player1, player2, switch_player,
                                    cur_game_num)
            else:
                exit()
        return cur_game_num, switch_player

    # This is for two humans to play against each other
    def two_player(self, player1, player2, switch_player, cur_game_num):
        self.setup()
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
            self.print_board(self.the_board)
            print("It is " + cur_player + "'s go, you are " +
                  players[cur_player] + ". Where do you want to go?")
            move = input()
            # Add move to board if legal
            if self.the_board[move] == ' ':
                self.the_board[move] = players[cur_player]
                count += 1
            else:
                print("Already taken")
                continue
            # Checks each solution against the board after a turn has been
            # taken to see if it is a winning move
            for sol in self.solutions:
                if (self.the_board[str(sol[0])] == self.the_board[str(sol[1])]
                        == self.the_board[str(sol[2])] == players[cur_player]):
                    self.print_board(self.the_board)
                    winner = True
                    cur_game_num = self.game_over(cur_player, player1, player2,
                                                  game_mode, switch_player,
                                                  cur_game_num, winner)
                    return cur_game_num, switch_player
            if cur_player == player1:  # Flips who the current player is
                cur_player = player2
            else:
                cur_player = player1
        winner = False
        cur_game_num = self.game_over(cur_player, player1, player2, game_mode,
                                      switch_player, cur_game_num, winner)
        return cur_game_num, switch_player

    def single_player(self, player1, player2, switch_player, cur_game_num):
        self.setup()
        game_mode = 1
        # Creates a copy of the board for the computer to pick from,
        # deletes the places that the user and computer have used
        comp_board = self.the_board.copy()
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
            self.print_board(self.the_board)

            if cur_player == player2:
                print("It is " + cur_player + "'s go, they are " +
                      players[cur_player] + ".")
                print("Computer is thinking",  end="\r")
                print("Computer is thinking.",  end="\r")
                print("Computer is thinking..",  end="\r")
                print("Computer is thinking...")
                # Get a random selection where the computer can place
                square, value = random.choice(list(comp_board.items()))
                self.the_board[square] = players[cur_player]
                del comp_board[square]
                count += 1
            else:
                print("It is " + cur_player + "'s go, you are " +
                      players[cur_player] + ". Where do you want to go?")
                move = input()
                if self.the_board[move] == ' ':
                    self.the_board[move] = players[cur_player]
                    count += 1
                    del comp_board[move]
                else:
                    print("Already taken")
                    continue
            for sol in self.solutions:
                if (self.the_board[str(sol[0])] == self.the_board[str(sol[1])]
                        == self.the_board[str(sol[2])] == players[cur_player]):
                    winner = True
                    cur_game_num = self.game_over(cur_player, player1, player2,
                                                  game_mode, switch_player,
                                                  cur_game_num, winner)
                    return cur_game_num, switch_player
            if cur_player == player1:
                cur_player = player2
            else:
                cur_player = player1
        winner = False
        cur_game_num = self.game_over(cur_player, player1, player2, game_mode,
                                      switch_player, cur_game_num, winner)
        return cur_game_num, switch_player

    def AI_training(self, player1, player2, switch_player, cur_game_num):
        cur_game_num = cur_game_num
        self.setup()
        square = 0
        game_mode = 0
        # Creates a copy of the board for the computer to pick from,
        # deletes the places that the user and computer have used
        comp_board = self.the_board.copy()
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
                square, value = random.choice(list(comp_board.items()))
                self.AI1_placement_temp[str(count)] = square
            elif cur_player == player2:
                square, value = random.choice(list(comp_board.items()))
            self.the_board[square] = players[cur_player]
            del comp_board[square]
            count += 1

            for sol in self.solutions:
                if (self.the_board[str(sol[0])] == self.the_board[str(sol[1])]
                        == self.the_board[str(sol[2])] == players[cur_player]):
                    # If player1 won, +3 to each of the moves played this game
                    # If player1 lost, -1 to each of the moves played this game
                    if cur_player == player1:
                        for key in self.AI1_placement_temp:
                            if self.AI1_placement_temp[key] != '':
                                self.AI1_full_weighting[key][self.AI1_placement_temp[key]] += 3
                    else:
                        for key in self.AI1_placement_temp:
                            if self.AI1_placement_temp[key] != '':
                                self.AI1_full_weighting[key][self.AI1_placement_temp[key]] -= 1
                    winner = True
                    cur_game_num, switch_player = self.game_over(cur_player,
                                                                 player1,
                                                                 player2,
                                                                 game_mode,
                                                                 switch_player,
                                                                 cur_game_num,
                                                                 winner)
                    return cur_game_num, switch_player
            # Switch player turn
            if cur_player == player1:
                cur_player = player2
            else:
                cur_player = player1
        # If a draw, +1 to each of the moves played in this game
        for key in self.AI1_placement_temp:
            if self.AI1_placement_temp[key] != '':
                self.AI1_full_weighting[key][self.AI1_placement_temp[key]] += 1
        winner = False
        cur_game_num, switch_player = self.game_over(cur_player, player1,
                                                     player2, game_mode,
                                                     switch_player,
                                                     cur_game_num, winner)
        return cur_game_num, switch_player

    def AI_players(self, player1, player2, switch_player, cur_game_num):
        cur_game_num = cur_game_num
        self.setup()
        square = 0
        game_mode = 0
        # Creates a copy of the board for the computer to pick from,
        # deletes the places that the user and computer have used
        comp_board = self.the_board.copy()
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
                AI1_test = self.AI1_full_weighting[str(count)]
                AI1_placement_weighting_sorted = sorted(AI1_test.items(),
                                                        key=lambda x: -x[1])
                # Iterates through the highest weighted positions,
                # picking the first that is free on the board
                for pos in AI1_placement_weighting_sorted:
                    if self.the_board[pos[0]] == ' ':
                        square = pos[0]
                        break
                self.AI1_placement_temp[str(count)] = square
            elif cur_player == player2:
                square, value = random.choice(list(comp_board.items()))
            self.the_board[square] = players[cur_player]
            del comp_board[square]
            count += 1

            for sol in self.solutions:
                if (self.the_board[str(sol[0])] == self.the_board[str(sol[1])]
                        == self.the_board[str(sol[2])] == players[cur_player]):
                    # If player1 won, +3 to each of the moves played this game
                    # If player1 lost, -1 to each of the moves playedthis game
                    if cur_player == player1:
                        for key in self.AI1_placement_temp:
                            if self.AI1_placement_temp[key] != '':
                                self.AI1_full_weighting[key][self.AI1_placement_temp[key]] += 3
                    else:
                        for key in self.AI1_placement_temp:
                            if self.AI1_placement_temp[key] != '':
                                self.AI1_full_weighting[key][self.AI1_placement_temp[key]] -= 1
                    winner = True
                    cur_game_num, switch_player = self.game_over(cur_player,
                                                                 player1,
                                                                 player2,
                                                                 game_mode,
                                                                 switch_player,
                                                                 cur_game_num,
                                                                 winner)
                    return cur_game_num, switch_player
            # Switch player turn
            if cur_player == player1:
                cur_player = player2
            else:
                cur_player = player1
        # If a draw, +1 to each of the moves played in this game
        for key in self.AI1_placement_temp:
            if self.AI1_placement_temp[key] != '':
                self.AI1_full_weighting[key][self.AI1_placement_temp[key]] += 1
        winner = False
        cur_game_num, switch_player = self.game_over(cur_player, player1,
                                                     player2, game_mode,
                                                     switch_player,
                                                     cur_game_num, winner)
        return cur_game_num, switch_player

    def saveWeightings(self, filename):
        with open(filename, 'w') as f:
            for key, value in self.AI1_full_weighting.items():
                f.write('%s:%s\n' % (key, value))


def main():
    TicTacToeGame = TicTacToe(1000, 10000)  # (num_games, training_games):
    switch_player = False
    cur_game_num = 0
    print("AI Game [0], Single player [1] or two player [2]?")
    game_selection = input()
    if game_selection == "0":
        player1 = "Computer1"
        player2 = "Computer2"
        TicTacToeGame.scoreboard[player1] = 0
        TicTacToeGame.scoreboard[player2] = 0
        TicTacToeGame.AI_training(player1, player2, switch_player,
                                  cur_game_num)
    elif game_selection == "1":
        print("Player 1")
        player1 = input("Enter the name : ")
        print("\n")
        player2 = "Computer"
        TicTacToeGame.scoreboard[player1] = 0
        TicTacToeGame.scoreboard[player2] = 0
        TicTacToeGame.single_player(player1, player2, switch_player,
                                    cur_game_num)
    elif game_selection == "2":
        print("Player 1")
        player1 = input("Enter the name : ")
        print("\n")
        print("Player 2")
        player2 = input("Enter the name : ")
        print("\n")
        TicTacToeGame.scoreboard[player1] = 0
        TicTacToeGame.scoreboard[player2] = 0
        TicTacToeGame.two_player(player1, player2, switch_player, cur_game_num)
    # This trains the model with random selections to
    # learn what choices are the best to use
    while (game_selection == '0' and
            cur_game_num < TicTacToeGame.training_games):
        cur_game_num, switch_player = TicTacToeGame.AI_training(player1,
                                                                player2,
                                                                switch_player,
                                                                cur_game_num)
    cur_game_num = 0
    TicTacToeGame.scoreboard[player1] = 0
    TicTacToeGame.scoreboard[player2] = 0
    # This plays the trained model against a CPU that random selects
    while game_selection == '0' and cur_game_num < TicTacToeGame.num_games:
        cur_game_num, switch_player = TicTacToeGame.AI_players(player1,
                                                               player2,
                                                               switch_player,
                                                               cur_game_num)
    print("Game over!")
    print("Current score:")
    for k, v in TicTacToeGame.scoreboard.items():
        print(k, ':', v)
    print("--------------------------------------------------------------")
    print(TicTacToeGame.AI1_full_weighting)
    print("-----------------------------------")
    TicTacToeGame.saveWeightings("myfile.txt")


if __name__ == '__main__':
    main()
