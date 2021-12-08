from indexing import *

computer_score = 0
human_score = 0


# TODO Think again
def calculate_score(computer, human, distance):
    global computer_score, human_score
    if human == 0:
        computer_score += pow(10, computer) - distance * pow(10, computer) // board_height
        return computer_score, 0
    elif computer == 0:
        human_score += pow(10, human) - distance * pow(10, human) // board_height
        return 0, human_score


class State:
    board = ""

    def __init__(self, board):
        self.board = board

    def heuristic(self):
        global computer_score, human_score
        computer_score, human_score = 0, 0
        # horizontally
        for i in range(0, board_height):
            self.connect_four(i, right)
        # vertically
        for i in range(0, board_width):
            self.connect_four(i, up)
        #  Diagonally
        for i in range(0, board_height - 3):
            self.connect_four(i, up_right)
        for i in range(0, (board_width - 3) * board_height, board_height):
            self.connect_four(i, up_right)
        return computer_score - human_score

    # def horizontal_count(self,start):
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
            calculate_score(computer, human, distance)
