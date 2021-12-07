board_width = 7
board_height = 6


class State:
    board = ""

    def __init__(self, board):
        self.board = board

    def right(self, index):
        if index // board_height == board_width - 1:
            return -1
        return self.board[index + board_height]

    def left(self, index):
        if index < board_height:
            return -1
        return self.board[index - board_height]

    def up(self, index):
        if index % board_height == board_height - 1:
            return -1
        return self.board[index + 1]

    def down(self, index):
        if index % board_height == 0:
            return -1
        return self.board[index - 1]

    def up_left(self, index):
        if index < board_height or index % board_height == board_height - 1:
            return -1
        return self.board[index - board_height + 1]

    def up_right(self, index):
        if index % board_height == board_height - 1 or index // board_height == board_width - 1:
            return -1
        return self.board[index + board_height + 1]

    def down_left(self, index):
        if index % board_height == 0 or index < board_height:
            return -1
        return self.board[index - board_height - 1]

    def down_right(self, index):
        if index % board_height == 0 or index // board_height == board_width - 1:
            return -1
        return self.board[index + board_height - 1]

