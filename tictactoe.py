import copy
from sys import float_info


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
    board[action[0]][action[1]] = player(board)
    return board


def winner(board):

    for game in winning_games:
        (i0, j0), (i1, j1), (i2, j2) = game 
        if board[i0][j0] == X and board[i1][j1] == X and board[i2][j2] == X:
            return X
        elif board[i0][j0] == O and board[i1][j1] == O and board[i2][j2] == O:
            return O
                                                                         
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
    

def minimax(board): # call minimax itself 
      
    optimal = track_board(board)
    return optimal[0] 
    
    
def track_board(board_state):
    
    player_turn = player(board_state) 

    actions_from_result_board_state = actions(board_state)
   
    # How to link an action to the optimal move?
    action_evaluation = (None, float('-inf') if player_turn == X else float('inf'))
    #linked_action = None 

    for action in actions_from_result_board_state:
        new_board_state = result(copy.deepcopy(board_state), action) 
        if not terminal(new_board_state):
            (_, next_evaluation) = track_board(new_board_state)
            if player_turn == X:
                if next_evaluation >= action_evaluation[1]:
                    action_evaluation = (action, next_evaluation)
            else:
                if next_evaluation <= action_evaluation[1]:
                    action_evaluation = (action, next_evaluation)

            #action_evaluation = max(track_board(new_board_state), action_evaluation) if player_turn == X else min(track_board(new_board_state), action_evaluation)   
        else:
            action_evaluation = (action, utility(new_board_state))
              
    return action_evaluation 
