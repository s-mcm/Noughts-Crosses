import random


# Starts/restarts the game when the program is launched/the game has ended
def play_game():
    global board_data
    global done_moves
    moves = 0
    game_over = False
    computer_difficulty = 1  # 1 = Easy. 2 = Medium. 3 = Hard

    print("Do you want to play against a computer?")
    play_computer = check_yes_no()
    # Checks computer difficulty
    if play_computer:
        computer_difficulty = check_computer_difficulty()

    while True:
        # If statement checks if the computer is enabled and if it would be the computers turn
        # moves % 2 == 1 only returns true every other move
        if play_computer and moves % 2 == 1:
            if computer_difficulty == 1:
                pos = computer_move_dumb()
            elif computer_difficulty == 2:
                pos = computer_move_medium()
            else:
                pos = computer_move_smart()
            print(f"Computer places {marker[1]} at position {pos}!")
        else:
            # Use get_position function to return a valid position
            pos = get_position(moves)

        # Set valid position to X (cross) or O (nought)
        # Moves modulo 2 means only the remainder of moves / 2 is given
        # If the remainder is 1 we know that the marker is an O
        board_data[pos - 1] = marker[moves % 2]

        # Print board with correct board data
        print_board(board_data)

        # Counts the amount of moves, when 9 is reached and no win condition is over, end the game
        moves += 1

        # If statement that uses the return of check_win and moves > 9 to see if the game is over
        if moves >= 9:
            print("Draw! Resetting board...")
            moves = 0
            board_data = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
            done_moves.clear()
            game_over = True
        elif check_win(board_data):
            print(f"{marker[(moves + 1) % 2]} wins! Resetting board...")
            moves = 0
            board_data = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
            done_moves.clear()
            game_over = True

        if game_over:
            print("Would you like to play again?")
            if check_yes_no():
                # Runs if the user wants to play again
                game_over = False
                print("Do you want to play against a computer?")
                play_computer = check_yes_no()
                # Checks computer difficulty
                if play_computer:
                    computer_difficulty = check_computer_difficulty()
                print_board(board_pos_ref)
                continue
            else:
                # Runs if the user wants to quit
                print("Good game!")
                break


# The following function print the current board to the command window
def print_board(board):
    print(f"\n\n\n {board[0]} | {board[1]} | {board[2]}\n"
          f"---|---|---\n"
          f" {board[3]} | {board[4]} | {board[5]}\n"
          f"---|---|---\n"
          f" {board[6]} | {board[7]} | {board[8]}\n")


# Return a valid location for the user to place a marker
def get_position(moves):
    while True:
        try:
            pos = int(input(f"Input a position for {marker[moves % 2]} to be placed: "))
        except ValueError:
            # Runs when a non-integer value is given
            print("Please enter a valid location between 1 and 9.")
            continue
        if pos < 1 or pos > 9:
            # Runs when an invalid position is given (lower than 1, higher than 9)
            print("Please enter a valid location between 1 and 9.")
            continue
        elif board_data[pos - 1] != " ":
            # Runs when the desired position is already taken (invalid move)
            print("Please enter a location that is not already taken!")
            continue
        else:
            # Valid position given, the loop can be exited
            break
    return pos


# Checks if the any of the players have won the game. Return true if player has won
def check_win(board):
    # Check if any row has a win condition
    if board[0] != " " and board[0] == board[1] == board[2]:  # row 1
        return True
    elif board[3] != " " and board[3] == board[4] == board[5]:  # row 2
        return True
    elif board[6] != " " and board[6] == board[7] == board[8]:  # row 3
        return True

    # Check if any column has a win condition
    if board[0] != " " and board[0] == board[3] == board[6]:  # column 1
        return True
    elif board[1] != " " and board[1] == board[4] == board[7]:  # column 2
        return True
    elif board[2] != " " and board[2] == board[5] == board[8]:  # column 3
        return True

    # Check if any diagonal has a win condition
    if board[0] != " " and board[0] == board[4] == board[8]:  # top left diagonal
        return True
    elif board[2] != " " and board[2] == board[4] == board[6]:  # top right diagonal
        return True

    return False


# Used to validate the input of yes or no
def check_yes_no():
    while True:
        user_input = input("Please input Y/N: ")
        if user_input.casefold() in {'y', 'yes'}:
            # Runs and returns true when yes is given
            return True
        elif user_input.casefold() in {'n', 'no'}:
            # Runs and returns false when no is given
            return False
        else:
            # Runs when the an invalid input is given (not yes or no)
            print("Error, you need to input Y/Yes/N/No")
            continue


# Validate computer difficulty
def check_computer_difficulty():
    while True:
        try:
            difficulty = int(input(f"Please input 1 for easy difficulty, "
                                   f"2 for medium difficulty or 3 for hard difficulty: "))
        except ValueError:
            # Runs when a non-integer value is given
            print("Please enter a valid number between 1 and 3.")
            continue
        if difficulty < 1 or difficulty > 3:
            # Runs when an invalid position is given (lower than 1, higher than 9)
            print("Please enter a valid number between 1 and 3.")
            continue
        else:
            # Valid position given, the loop can be exited
            break
    return difficulty


# Moves in any random valid position
def computer_move_dumb():
    while True:
        for i in range(9):
            random_move = random.randint(1, 9)
            if random_move not in done_moves:
                # If the move is not on the list, add it to the list to prevent the computer from to using it again
                done_moves.append(random_move)
        if board_data[random_move - 1] != " ":
            # Runs when the desired position is already taken (invalid move)
            continue
        else:
            # Valid position given, the loop can be exited
            break
    return random_move


# 50/50 chance between moving randomly and calculating a move
def computer_move_medium():
    if bool(random.getrandbits(1)):
        return computer_move_smart()
    else:
        return computer_move_dumb()


# Calculates the best move to make in this order: Computer win > Player win > Centre > Corner > Side
def computer_move_smart():
    valid_moves = []
    # Checks if the computer has any winning moves, if one is found return that position
    for i in range(9):
        if board_data[i] == " " and test_computer_move(i, 1):
            valid_moves.append(i)
    # Checks if there are any valid moves. If so, select one randomly
    if valid_moves:
        return random.choice(valid_moves) + 1

    # Checks if the player has any winning moves
    for i in range(9):
        if board_data[i] == " " and test_computer_move(i, 0):
            valid_moves.append(i)
    if valid_moves:
        return random.choice(valid_moves) + 1

    # Checks if the centre (pos 5) is open
    if board_data[4] == " ":
        return 4 + 1

    # Checks if any corners are open
    for i in [0, 2, 6, 8]:
        if board_data[i] == " ":
            valid_moves.append(i)
    if valid_moves:
        return random.choice(valid_moves) + 1

    # Checks if any sides are open
    for i in [1, 3, 5, 7]:
        if board_data[i] == " ":
            valid_moves.append(i)
    if valid_moves:
        return random.choice(valid_moves) + 1


# Checks if the move being given will win. Returns true if the move wins the game
def test_computer_move(test_pos, marker_index):
    # Gets a copy of the board
    board_data_copy = []
    for x in board_data:
        board_data_copy.append(x)

    # Edit the board copy with the new potential move
    board_data_copy[test_pos] = marker[marker_index]
    # Check the new potential with check_win
    if check_win(board_data_copy):
        return True
    else:
        return False


# Program main starts from here, feel free to edit it.
marker = ["X", "O"]
board_data = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
board_pos_ref = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
done_moves = []
print(f"Welcome to Noughts And Crosses. You will be {marker[0]}'s. These are the board positions: ")
print_board(board_pos_ref)
play_game()
