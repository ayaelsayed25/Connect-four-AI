board_width = 7
board_height = 6


def up_right(index):
    if index % board_height == board_height - 1 or index // board_height == board_width - 1:
        return -1
    return index + board_height + 1


def down(index):
    if index % board_height == 0:
        return -1
    return index - 1


def up(index):
    if index % board_height == board_height - 1:
        return -1
    return index + 1


def right(index):
    if index // board_height == board_width - 1:
        return -1
    return index + board_height



