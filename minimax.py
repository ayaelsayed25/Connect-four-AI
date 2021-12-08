import math

minimax_expansion = {}


def is_game_over(board):
    return '0' not in board


def minimax(state, k, maximizing):
    if k == 0 or is_game_over(state.board):
        heuristic = state.heuristic()
        minimax_expansion[state] = heuristic
        return heuristic, state
    if maximizing:
        max_eval = -math.inf
        max_state = None
        children = state.construct_next_states(False)
        for child in children:
            if child is not None:
                temp, _ = minimax(child, k - 1, False)
                if temp > max_eval:
                    max_eval = temp
                    max_state = child
        minimax_expansion[state] = max_eval
        return max_eval, max_state

    else:
        min_eval = math.inf
        min_state = None
        children = state.construct_next_states(True)
        for child in children:
            if child is not None:
                temp, _ = minimax(child, k - 1, True)
                if temp < min_eval:
                    min_eval = temp
                    min_state = child
        minimax_expansion[state] = min_eval
        return min_eval, min_state
