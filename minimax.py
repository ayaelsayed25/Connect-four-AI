import math
from state import *

minimax_expansion = {}


def minimax_play(current_state, k, maximizing, prune=False):
    minimax_expansion[current_state] = 0
    max_eval, next_state = minimax(current_state, k, maximizing, prune)
    minimax_expansion.popitem()
    board_expansion = ["" for _ in range(len(minimax_expansion))]
    score_expansion = [-math.inf for _ in range(len(minimax_expansion))]
    i = 0
    minimax_expansion[current_state] = max_eval
    for s, heuristic in minimax_expansion.items():
        if s is not None:
            board_expansion[i] = s.board
            score_expansion[i] = heuristic
        i += 1
    return max_eval, next_state, board_expansion, score_expansion


def is_game_over(board):
    return '0' not in board


# prune, none
def minimax(state, k, maximizing, prune=False, alpha=-math.inf, beta=math.inf):
    if k == 0 or is_game_over(state.board):
        heuristic = state.heuristic()
        # print(heuristic)
        minimax_expansion[state] = heuristic
        return heuristic, state
    if maximizing:
        max_eval = -math.inf
        max_state = None
        children = state.construct_next_states(True)
        for child in children:
            minimax_expansion[child] = max_eval
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
            minimax_expansion[child] = min_eval
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


mama = "000000000000000000000000000000000000000000"
minimax_play(State("000011000002000000000000000000000000000000"), 2, True)
# print(minimax(State("000011000002000000000000000000000000000000"), 2, True))
i = 0
j = 0
for state, heuristicc in minimax_expansion.items():
    i += 1
    print(state.board + " " + str(heuristicc))
    if i == pow(7, j):
        j += 1
        i = 0
        print('\n')
