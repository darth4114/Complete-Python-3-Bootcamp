def display_board(board):
    print('\n'*100)
    print("   |   |   ")
    print(" " +board[7]+ " | " +board[8]+ " | " +board[9]+ " ")
    print("   |   |   ")
    print("------------")
    print("   |   |   ")
    print(" " +board[4]+ " | " +board[5]+ " | " +board[6]+ " ")
    print("   |   |   ")
    print("------------")
    print("   |   |   ")
    print(" " +board[1]+ " | " +board[2]+ " | " +board[3]+ " ")
    print("   |   |   ")

def player_input():
    marker = ''

    while not (marker == 'X' or marker == 'O'):
        marker = input('Player 1, please choose team X or O: ').upper()

    if marker == 'X':
        return ('X','O')
    else:
        return ('O','X')

def place_marker(board, marker, position):
    board[position] = marker
    return board

def win_check(board, mark):
    bot = board[1:4]
    mid = board[4:7]
    top = board[7:]

    if top[0] == mid[0] == bot[0] == mark:
        return True
    elif top[1] == mid[1] == bot[1] == mark:
        return True
    elif top[2] == mid[2] == bot[2] == mark:
        return True
    elif top[0] == top[1] == top[2] == mark:
        return True
    elif mid[0] == mid[1] == mid[2] == mark:
        return True
    elif bot[0] == bot[1] == bot[2] == mark:
        return True
    elif top[0] == mid[1] == bot[2] == mark:
        return True
    elif top[2] == mid[1] == bot[0] == mark:
        return True
    else:
        return False

import random

def choose_first():
    rand = random.randint(0,1)
    if rand == 0:
        return 'Player 1'
    else:
        return 'Player 2'

def space_check(board, position):
    return board[position] == ' '

def full_board_check(board):
    for i in range(1,10):
        if space_check(board, i):
            return False
    return True

def player_choice(board):
    position = 0

    while position not in [1,2,3,4,5,6,7,8,9] or not space_check(board, position):
        position = int(input('Choose your next position: (1-9) '))

    return position

def replay():
    return input('Do you want to play again? (y/n)').lower().startswith('y')


print('Welcome to Tic Tac Toe!')

while True:
    # Set the game up here
    theBoard = [' ']*10
    player1_marker, player2_marker = player_input()
    turn = choose_first()
    print(turn + ' will go first.')

    play_game = input('Are you ready to play? Enter Yes or No')

    if play_game.lower()[0] == 'y':
        game_on = True
    else:
        game_on = False

    while game_on:
        if turn == 'Player 1':
            #Player1's turn

            display_board(theBoard)
            position = player_choice(theBoard)
            place_marker(theBoard, player1_marker, position)

            if win_check(theBoard, player1_marker):
                display_board(theBoard)
                print('Congratulations! You have won the game!')
                game_on = False
            else:
                if full_board_check(theBoard):
                    display_board(theBoard)
                    print('The game is a draw!')
                    break
                else:
                    turn = 'Player 2'

        else:
        # Player2's turn.

            display_board(theBoard)
            position = player_choice(theBoard)
            place_marker(theBoard, player2_marker, position)

            if win_check(theBoard, player2_marker):
                display_board(theBoard)
                print('Player 2 has won!')
                game_on = False
            else:
                if full_board_check(theBoard):
                    display_board(theBoard)
                    print('The game is a draw!')
                    break
                else:
                    turn = 'Player 1'

            #pass

    if not replay():
        break
