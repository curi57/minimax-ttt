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
    elif winner_player == O:
        return -1
    

def minimax(board):  

    print("------------------------\n\n")

    #avaiable_actions = actions(board)
    #scores = []
    
    #player_turn = player(board)
    #next_player_turn = X if player_turn == O else X  
    #initial_move_evaluation = float('inf') if next_player_turn == X else float('-inf')
    #for action in avaiable_actions: 
    #    score = track_score(result(copy.deepcopy(board), action), next_player_turn, initial_move_evaluation) # result board from player turn move is being passed
    #    scores.append((action, score))

    avaiable_actions = actions(board)

    print(f"avaiable_actions: {avaiable_actions}")

    scores = []
    player_turn = player(board)

    print(f"player_turn: {player_turn}")
    for action in avaiable_actions:
        score = track_moves(board, action, player_turn, float('inf') if player_turn == X else float('-inf'))
        scores.append((action, score))

    
    optimal = None  
    for s in scores:
        (action, score) = s
        print(f"action {action} : {score}")
        if optimal is not None:
            (_, curr_optimal) = optimal
            if player_turn == X:
                if score >= curr_optimal: # sortir decisões com evaluations iguais
                    optimal = s
            elif player_turn == O:
                if score < curr_optimal:
                    optimal = s
        else:
            optimal = s
        
    if optimal is None:
        raise Exception("No action found")

    return optimal[0]


def track_moves(from_board, action, player_turn, curr_evaluation):
    
    result_board = result(from_board, action) # board resultante da action passada via parâmetro (jogador atual)
    avaiable_actions_from_result_board = actions(result_board) # actions disponíveis para o board resultante depois da jogada do jogador atual (essas actions estarão disponíveis 
    # para o próximo jogador)

    if not terminal(result_board):
        #next_player_turn = X if player_turn == O else X
        for avaiable_action in avaiable_actions_from_result_board:
            result_board_evaluation = track_moves(copy.deepcopy(result_board), avaiable_action, player_turn, curr_evaluation)
            return min(result_board_evaluation, curr_evaluation) if player_turn == X else max(result_board_evaluation, curr_evaluation)        
    else:
        terminal_evaluation = utility(result_board)
        print(f"terminal_evaluation: {terminal_evaluation}")

        return terminal_evaluation
    

def track_score(result_board, player_turn, move_evaluation):

    avaiable_actions_from_result_board = actions(result_board)
                                        
    for action in avaiable_actions_from_result_board:
        next_result_board = result(result_board, action)
        if not terminal(next_result_board):
            next_move_layer_evaluation = track_score(copy.deepcopy(next_result_board), player(next_result_board), move_evaluation)
            if player_turn == X:
                return min(next_move_layer_evaluation, move_evaluation)
            elif player_turn == O:
                return max(next_move_layer_evaluation, move_evaluation)
        else:
            return utility(result_board)
