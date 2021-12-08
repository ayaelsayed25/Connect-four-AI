import math

minimax_expansion = {}


def is_game_over(board):
    return '0' not in board


# prune, none
def minimax(state, k, maximizing, prune=False, alpha=-math.inf, beta=math.inf):
    if k == 0 or is_game_over(state.board):
        heuristic = state.heuristic()
        minimax_expansion[state] = heuristic
        return heuristic, state
    if maximizing:
        max_eval = -math.inf
        max_state = None
        children = state.construct_next_states(True)
        # TODO Tree expansion
        for child in children:
            minimax_expansion[child] = max_state
        for child in children:
            if child is not None:
                temp, _ = minimax(child, k - 1, False, prune, alpha, beta)
                alpha = max(alpha, temp)
                if temp > max_eval:
                    max_eval = temp
                    max_state = child
                if prune and beta <= alpha:
                    break
        minimax_expansion[state] = max_eval
        return max_eval, max_state

    else:
        min_eval = math.inf
        min_state = None
        children = state.construct_next_states(False)
        for child in children:
            if child is not None:
                temp, _ = minimax(child, k - 1, True, prune, alpha, beta)
                beta = min(beta, temp)
                if temp < min_eval:
                    min_eval = temp
                    min_state = child
                if prune and beta <= alpha:
                    break
        minimax_expansion[state] = min_eval
        return min_eval, min_state
