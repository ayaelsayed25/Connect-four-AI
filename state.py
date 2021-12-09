from indexing import *


# Method to visit all Fours in the board Horizontally, Vertically, and Diagonally
def board_visitor(visitor):
    # horizontally
    for i in range(board_height - 1, -1, -1):
        visitor(i, right)
    # vertically
    for i in range(board_height - 1, board_width*board_height, board_height):
        visitor(i, up)
    # Diagonally
    for i in range(board_height - 2, board_height - 4, -1):
        visitor(i, up_right)
    for i in range(board_height - 1, (board_width - 2)*board_height-1, board_height):
        visitor(i, up_right)

    for i in range(board_height*board_width - 2, board_height*board_width - 4, -1):
        visitor(i, up_left)
    for i in range(board_height*board_width - 1, (board_width - 4)*board_height - 1, -board_height):
        visitor(i, up_left)


class State:
    board = ""
    computer_heuristic_score = 0
    human_heuristic_score = 0
    human_score = 0
    computer_score = 0
    player_move = -1

    def __init__(self, board, player_move=-1):
        self.board = board
        self.player_move = player_move

    # Add Human play to the current board
    def game_play(self, column):
        index = self.first_empty_index(column)
        self.board = self.board[:index] + '2' + self.board[index+1:]

    # Get Index of computer play
    def get_index(self):
        return get_row(self.player_move), get_column(self.player_move)

    # TODO Think again
    def calculate_score_heuristic(self, computer, human, distance):
        if human == 0:
            self.computer_heuristic_score += pow(10, computer) - distance * pow(10, computer) // 3
        elif computer == 0:
            self.human_heuristic_score += pow(10, human) - distance * pow(10, human) // board_height

    # Get First empty index in the Board string in specific row
    def first_empty_index(self, column):
        empty_index = column = column*board_height + board_height - 1
        for j in range(column, column - board_height, -1):
            if self.board[empty_index] != '0':
                empty_index -= 1
            else:
                break
        if empty_index == column - board_height - 1:
            return -1
        return empty_index

    # Get first empty row in the column
    def first_empty_row(self, column):
        index = self.first_empty_index(column)
        return get_row(index)

    def construct_next_states(self, computer_turn):
        states = []
        for i in range(0, board_width):
            # Get All possible plays for the computer and its states
            empty_index = self.first_empty_index(i)
            if empty_index != -1:
                board = self.board
                if computer_turn:
                    board = board[:empty_index] + '1' + board[empty_index+1:]
                else:
                    board = board[:empty_index] + '2' + board[empty_index+1:]
                states.append(State(board, empty_index))
            else:
                states.append(None)
        return states

    # Get State Heuristic score. Used in minimax algorithm
    def heuristic(self):
        board_visitor(self.connect_four)
        return self.computer_heuristic_score - self.human_heuristic_score

    # Calculate distance between the required squares to connect four and the last filled square in the column
    def calculate_distance(self, index):
        distance = 0
        while index != -1 and self.board[index] == '0':
            distance += 1
            index = down(index)
        return distance

    def connect_four(self, i, direction):
        temp = index = i
        while index != -1:
            index = temp
            human = 0
            computer = 0
            distance = 0
            for _ in range(0, 4):
                if self.board[index] == '1':
                    computer += 1
                elif self.board[index] == '2':
                    human += 1
                else:
                    distance += self.calculate_distance(down(index))
                index = direction(index)
            temp = direction(temp)
            if distance < 3:
                self.calculate_score_heuristic(computer, human, distance)

    def count_fours(self, i, direction):
        temp = i
        index = temp
        while index != -1:
            index = temp
            human = 0
            computer = 0
            for _ in range(0, 4):
                if self.board[index] == '1':
                    computer += 1
                elif self.board[index] == '2':
                    human += 1
                index = direction(index)
            temp = direction(temp)
            if computer == 4:
                self.computer_score += 1
            elif human == 4:
                self.human_score += 1

    def calculate_score(self):
        self.computer_score = self.human_score = 0
        board_visitor(self.count_fours)
        return self.computer_score, self.human_score
