from indexing import *


class State:
    board = ""
    computer_heuristic_score = 0
    human_heuristic_score = 0
    human_score = 0
    computer_score = 0
    player_move = -1

    def __init__(self, board, player_move):
        self.board = board
        self.player_move = player_move

    def game_play(self, column):
        self.board[self.first_empty_index(column)] = '2'

    def get_index(self):
        return self.player_move % board_height, self.player_move // board_height

    # TODO Think again
    def calculate_score_heuristic(self, computer, human, distance):
        if human == 0:
            self.computer_heuristic_score += pow(10, computer) - distance * pow(10, computer) // board_height
        elif computer == 0:
            self.human_heuristic_score += pow(10, human) - distance * pow(10, human) // board_height

    def first_empty_index(self, column):
        empty_index = column
        for j in range(column, column + board_height):
            if self.board[empty_index] != '0':
                empty_index += 1
        if empty_index == column + board_height:
            return -1
        return empty_index

    def first_empty_row(self, column):
        index = self.first_empty_index(column)
        return index % board_height

    def construct_next_states(self, computer_turn):
        states = []
        for i in range(0, board_width * board_height, board_height):
            empty_index = self.first_empty_index(i)
            if empty_index != -1:
                board = self.board
                if computer_turn:
                    board[empty_index] = '1'
                else:
                    board[empty_index] = '2'
                states.append(State(board, empty_index))
            else:
                states.append(None)

    def heuristic(self):
        self.board_visitor(self.connect_four)
        return self.computer_heuristic_score - self.human_heuristic_score

    def calculate_distance(self, index):
        distance = 0
        while index != -1 and self.board[index] == '0':
            distance += 1
            index = down(index)
        return distance

    def connect_four(self, i, direction):
        temp, index = i
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
                    distance += self.calculate_distance(index)
                index = direction(index)
            temp = direction(temp)
            self.calculate_score_heuristic(computer, human, distance)

    def count_fours(self, i, direction):
        temp, index = i
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
            if human == 0 and computer == 4:
                self.computer_score += 1
            elif human == 4 and computer == 0:
                self.human_score += 1

    def calculate_score(self):
        self.board_visitor(self.count_fours)
        return self.computer_score, self.human_score

    def board_visitor(self, visitor):
        # horizontally
        for i in range(0, board_height):
            visitor(i, right)
        # vertically
        for i in range(0, board_width):
            visitor(i, up)
        #  Diagonally
        for i in range(0, board_height - 3):
            visitor(i, up_right)
        for i in range(0, (board_width - 3) * board_height, board_height):
            visitor(i, up_right)
