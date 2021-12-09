board_width = 7
board_height = 6


def get_row(index):
    return index % board_height


def get_column(index):
    return index // board_height


def up_right(index):
    if get_row(index) == 0 or get_column(index) == board_width - 1:
        return -1
    return index + board_height - 1


def up_left(index):
    if get_row(index) == 0 or get_column(index) == 0:
        return -1
    return index - board_height - 1


def down(index):
    if get_row(index) == board_height - 1:
        return -1
    return index + 1


def up(index):
    if get_row(index) == 0:
        return -1
    return index - 1


def right(index):
    if get_column(index) == board_width - 1:
        return -1
    return index + board_height
