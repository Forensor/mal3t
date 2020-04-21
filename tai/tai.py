import sqlite3
import random
from copy import deepcopy

# DATABASE CONNECTION [AND TABLE CREATION]

database = sqlite3.connect('TAI')
database_operation = database.cursor()

database_operation.execute("""CREATE TABLE IF NOT EXISTS moves(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                position TEXT,
                                movement TEXT,
                                result TEXT);""")

database_operation.execute("""CREATE TABLE IF NOT EXISTS games(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                pgn TEXT,
                                team TEXT,
                                result TEXT);""")
database.commit()

# GAME STATE

game_state = []
coords = ['a3', 'b3', 'c3', 'a2', 'b2', 'c2', 'a1', 'b1', 'c1']
turn = ''
cross_is_cpu = False
nought_is_cpu = False

# GAME HISTORY

game_positions = []
pgn = []

# TAI FUNCTIONS

def calc_moves(position):

    global coords

    possible_moves = []

    for i in range(9):
        if position[i] == 'N':
            possible_moves.append(coords[i])

    return possible_moves

def pick_best_move(position, list_of_moves):
    global game_positions
    global pgn

    winning_moves = []
    drawing_moves = []
    losing_moves = []
    unknown_moves = []

    for possible_move in list_of_moves:
        database_operation.execute("SELECT result FROM moves WHERE position=? AND movement=?;",
                                   (''.join(position), possible_move));

        if database_operation.fetchone() == 'win':
            winning_moves.append(possible_move)
        elif database_operation.fetchone() == 'draw':
            drawing_moves.append(possible_move)
        elif database_operation.fetchone() == 'lose':
            losing_moves.append(possible_move)
        else:
            unknown_moves.append(possible_move)

    move_to_make = ''
    if winning_moves:
        move_to_make = random.choice(winning_moves)
        update_result_in_database(game_positions[len(game_positions) - 3],
                                  pgn[len(pgn) - 2], 'win')
    elif unknown_moves:
        move_to_make = random.choice(unknown_moves)
    elif drawing_moves:
        move_to_make = random.choice(drawing_moves)
        update_result_in_database(game_positions[len(game_positions) - 3],
                                  pgn[len(pgn) - 2], 'draw')
    else:
        move_to_make = random.choice(losing_moves)
        update_result_in_database(game_positions[len(game_positions) - 3],
                                  pgn[len(pgn) - 2], 'lose')

    return move_to_make

def store_new_move_in_database(position, movement):
    database_operation.execute("SELECT id FROM moves WHERE position=? AND movement=?;",
                               (''.join(position), movement))
    on_database = database_operation.fetchone()

    if not on_database:
        database_operation.execute("INSERT INTO moves(position, movement, result) VALUES(?, ?, 'unknown');",
                                   (''.join(position), movement))
        database.commit()

def update_result_in_database(position, movement, result):
    database_operation.execute("UPDATE moves SET result=? WHERE position=? AND movement=?;",
                               (result, ''.join(position), movement))
    database.commit()

# BOARD FUNCTIONS

def move(movement):
    global game_state
    global game_positions
    global pgn

    for i in range(9):
        if coords[i] == movement:
            store_new_move_in_database(game_state,
                                       movement)
            if turn == 'cross':
                game_state[i] = 'X'
            else:
                game_state[i] = 'O'
            game_positions.append(deepcopy(game_state)) # <- This gave me a headache
            pgn.append(movement)
            check_result()
            swap_turn()

# STATE FUNCTIONS

def swap_turn():
    global turn

    if turn == 'cross':
        turn = 'nought'
    else:
        turn = 'cross'

def check_result():
    """Little bit lazy ikr"""

    global game_state

    if ((game_state[0] == 'X' and
         game_state[1] == 'X' and
         game_state[2] == 'X')
        or
        (game_state[2] == 'X' and
         game_state[5] == 'X' and
         game_state[8] == 'X')
        or
        (game_state[6] == 'X' and
         game_state[7] == 'X' and
         game_state[8] == 'X')
        or
        (game_state[0] == 'X' and
         game_state[3] == 'X' and
         game_state[6] == 'X')
        or
        (game_state[2] == 'X' and
         game_state[4] == 'X' and
         game_state[6] == 'X')
        or
        (game_state[0] == 'X' and
         game_state[4] == 'X' and
         game_state[8] == 'X')
        or
        (game_state[1] == 'X' and
         game_state[4] == 'X' and
         game_state[7] == 'X')
        or
        (game_state[3] == 'X' and
         game_state[4] == 'X' and
         game_state[5] == 'X')
        ):
        end_game('cross')
    elif ((game_state[0] == 'O' and
         game_state[1] == 'O' and
         game_state[2] == 'O')
        or
        (game_state[2] == 'O' and
         game_state[5] == 'O' and
         game_state[8] == 'O')
        or
        (game_state[6] == 'O' and
         game_state[7] == 'O' and
         game_state[8] == 'O')
        or
        (game_state[0] == 'O' and
         game_state[3] == 'O' and
         game_state[6] == 'O')
        or
        (game_state[2] == 'O' and
         game_state[4] == 'O' and
         game_state[6] == 'O')
        or
        (game_state[0] == 'O' and
         game_state[4] == 'O' and
         game_state[8] == 'O')
        or
        (game_state[1] == 'O' and
         game_state[4] == 'O' and
         game_state[7] == 'O')
        or
        (game_state[3] == 'O' and
         game_state[4] == 'O' and
         game_state[5] == 'O')
        ):
        end_game('nought')
    elif 'N' not in game_state:
        end_game('noone')

def end_game(winning_team):
    global cross_is_cpu
    global nought_is_cpu
    global game_positions
    global pgn

    if winning_team == 'cross':
        print("CROSS WON!")
        if cross_is_cpu:
            store_game_in_database('cross', 'win')
            update_result_in_database(game_positions[len(game_positions) - 3],
                                      pgn[len(pgn) - 2], 'win')
        else:
            store_game_in_database('nought', 'lose')
            update_result_in_database(game_positions[len(game_positions) - 3],
                                      pgn[len(pgn) - 2], 'lose')
    elif winning_team == 'nought':
        print("NOUGHT WON!")
        if nought_is_cpu:
            store_game_in_database('nought', 'win')
            update_result_in_database(game_positions[len(game_positions) - 3],
                                      pgn[len(pgn) - 2], 'win')
        else:
            store_game_in_database('cross', 'lose')
            update_result_in_database(game_positions[len(game_positions) - 3],
                                      pgn[len(pgn) - 2], 'lose')
    else:
        print("DRAW")
        store_game_in_database('nought', 'draw')
        update_result_in_database(game_positions[len(game_positions) - 3],
                                  pgn[len(pgn) - 2], 'draw')
    print("GAME ENDED, PRESS ENTER TO START A NEW ONE...")
    input()
    new_game()

def store_game_in_database(team, result):
    global pgn

    database_operation.execute("INSERT INTO games(pgn, team, result) VALUES(?, ?, ?);",
                               (''.join(pgn), team, result))
    database.commit()

def new_game():

    global game_state
    global turn
    global cross_is_cpu
    global nought_is_cpu
    global game_positions
    global pgn

    print('Select gamemode:')
    print('1. [X] HUMAN vs TAI [O]')
    print('2. [X] TAI vs HUMAN [O]')
    print('3. [X] HUMAN vs HUMAN [O]')
    print('4. [X] TAI vs TAI [O]')

    gamemode = input()

    if gamemode == '1':
        cross_is_cpu = False
        nought_is_cpu = True
    elif gamemode == '2':
        cross_is_cpu = True
        nought_is_cpu = False
    elif gamemode == '3':
        cross_is_cpu = False
        nought_is_cpu = False
    else:
        cross_is_cpu = True
        nought_is_cpu = True

    game_state = ['N', 'N', 'N',
                  'N', 'N', 'N',
                  'N', 'N', 'N']
    turn = 'cross'
    game_positions = []
    pgn = []
    game_positions.append(deepcopy(game_state))

    while True:
        wait_for_move()

def print_board():
    global game_state

    for i in range(9):
        print('[' + game_state[i] + ']', end='')
        if (i + 1) % 3 == 0:
            print('')

def wait_for_move():
    global turn
    global cross_is_cpu
    global nought_is_cpu
    global game_state

    if turn == 'cross' and not cross_is_cpu:
        print_board()
        print('Move: ', end='')
        movement = input()
        move(movement)
    elif turn == 'cross' and cross_is_cpu:
        move(pick_best_move(game_state, calc_moves(game_state)))
    elif turn == 'nought' and not nought_is_cpu:
        print_board()
        print('Move: ', end='')
        movement = input()
        move(movement)
    elif turn == 'nought' and nought_is_cpu:
        move(pick_best_move(game_state, calc_moves(game_state)))

new_game()
