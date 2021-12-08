def down_right(index):
    if index % board_height == 0 or index // board_height == board_width - 1:
        return -1
    return index + board_height - 1


def up_right(index):
    if index % board_height == board_height - 1 or index // board_height == board_width - 1:
        return -1
    return index + board_height + 1


def down_left(index):
    if index % board_height == 0 or index < board_height:
        return -1
    return index - board_height - 1


def up_left(index):
    if index < board_height or index % board_height == board_height - 1:
        return -1
    return index - board_height + 1


def down(index):
    if index % board_height == 0:
        return -1
    return index - 1


board_width = 7
board_height = 6


def up(index):
    if index % board_height == board_height - 1:
        return -1
    return index + 1


def left(index):
    if index < board_height:
        return -1
    return index - board_height


def right(index):
    if index // board_height == board_width - 1:
        return -1
    return index + board_height



