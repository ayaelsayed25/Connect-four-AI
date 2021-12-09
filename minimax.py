import math
from state import *

minimax_expansion = []


def minimax_play(current_state, k, maximizing, prune=False):
    global minimax_expansion
    minimax_expansion = [dict() for _ in range(k + 1)]
    max_eval, next_state = minimax(current_state, k, maximizing, prune)
    length = 0
    for level in minimax_expansion:
        length += len(level)
    board_expansion = ["None" for _ in range(length)]
    score_expansion = [-math.inf for _ in range(length)]
    minimax_expansion[k][current_state] = max_eval
    i = 0
    for j in range(k, -1, -1):
        for state, heuristic in minimax_expansion[j].items():
            if state.board != "":
                board_expansion[i] = state.board
                score_expansion[i] = heuristic
            i += 1
    return max_eval, next_state, board_expansion, score_expansion


def is_game_over(board):
    return '0' not in board


# prune, none
def minimax(state, k, maximizing, prune=False, alpha=-math.inf, beta=math.inf):
    if state is None:
        minimax_expansion[k][State("")] = -math.inf
        if maximizing:
            return math.inf, None
        else:
            return -math.inf, None
    if k == 0 or is_game_over(state.board):
        heuristic = state.heuristic()
        minimax_expansion[k][state] = heuristic
        return heuristic, state
    if maximizing:
        max_eval = -math.inf
        max_state = None
        children = state.construct_next_states(True)
        for child in children:
            temp, _ = minimax(child, k - 1, False, prune, alpha, beta)
            alpha = max(alpha, temp)
            if temp > max_eval:
                max_eval = temp
                max_state = child
            if prune and beta <= alpha:
                break
        minimax_expansion[k][state] = max_eval
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
        minimax_expansion[k][state] = min_eval
        return min_eval, min_state


# mama = "000000000000000000000000000000000000000000"
m, x, d, s = minimax_play(State("000000000000000000000000000000000000111111"), 5, True, True)
# for c in s:
#     print(c)
for c in d:
    print(c)
# # print(minimax(State("000011000002000000000000000000000000000000"), 2, True))
# i = 0
# j = 0
# for state, heuristic in minimax_expansion.items():
#     i += 1
#     print(state.board + " " + str(heuristic))
#     if i == pow(7, j):
#         j += 1
#         i = 0
#         print('\n')
