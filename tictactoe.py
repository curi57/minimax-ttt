import copy


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
    #value = board[action[0]][action[1]]
    #if value != EMPTY:
        #raise Exception("This move has already been made")
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
    else:
        return -1
    

def minimax(board):

    print(f"initial board: {board}")
  
    avaiable_actions = actions(board)
    scores = []
    # can be optimized by findind a score equal to the number of possivel ending games
    for action in avaiable_actions: 
        score = track_score(result(copy.deepcopy(board), action), 0)
        print(f"board: {board},\n actions: {avaiable_actions},\n score: {score}")
        scores.append((action, score))
    
    optimal_action = None
    for s in scores:
        (action, score) = s 
        if optimal_action is not None:
            (_, curr_optimal_score) = optimal_action
            if score > curr_optimal_score:
                optimal_action = s
            
        optimal_action =  s
    
    if optimal_action is None:
        raise Exception("No action found")

    return optimal_action[0]
    

def track_score(result_board, curr_score):

    avaiable_actions_from_result_board = actions(result_board)
                                        
    for action in avaiable_actions_from_result_board:
        if not terminal(result(result_board, action)):
            curr_score = track_score(copy.deepcopy(result_board), curr_score)
        
        updated_score = curr_score + utility(result_board)
        print(updated_score)
        return updated_score 
