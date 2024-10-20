"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None

winning_games = [
        [(0, 0), (0, 1), (0, 2)], 
        [(1, 0), (1, 1), (1, 2)], 
        [(2, 0), (2, 1), (2, 2)], 
        [(0, 0), (1, 0), (2, 0)], 
        [(0, 1), (1, 1), (2, 1)], 
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)], 
        [(0, 2), (1, 1), (2, 0)]]


def initial_state():  
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):  
    first_line_moves =  len([v for v in board[0] if v != EMPTY])
    second_line_moves = len([v for v in board[1] if v != EMPTY])
    third_line_moves = len([v for v in board[2] if v != EMPTY])

    if (first_line_moves + second_line_moves + third_line_moves) % 2 == 0:
        return X
    else:
        return O

def actions(board):  
    possible_actions = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.append((i, j))

    return possible_actions


def result(board, action):  
    (i, j) = action

    value = board[i][j]
    if value != EMPTY:
        raise Exception("this move has already been made")

    board[i][j] = player(board)


def winner(board):

    action_values = []
    no_empties = 0
    for game in winning_games:
        for action in game:
            (i, j) = action
            board_action = board[i][j]
            if board_action != EMPTY:
                action_values.append(board_action)
                no_empties += 1
        action_values_set = set(action_values)
        if no_empties == 3 and len(action_values_set) == 1:
            return action_values_set.pop()
        
        action_values.clear()
        no_empties = 0
                                                                     
    return None 



def terminal(board):
    
    is_completed = True 
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                is_completed = False
                break

    return is_completed or winner(board) is not None


def utility(board):  
    winner_player = winner(board)
    if winner_player is None:
        return 0
    elif winner_player == X:
        return 1
    else:
        return -1
    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
