from tkinter import *
from PIL import Image, ImageTk
import networkx as nx
import matplotlib.pyplot as plt
from minimax import *
from state import *

# configure window
window = Tk()
window.title("Connect-four Game")
bck = Image.open('./images/sunrise.jpg')
backgroundImg = ImageTk.PhotoImage(bck)
background_label = Label(window, image=backgroundImg)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
window.attributes("-fullscreen", True)
# window.wm_attributes('-transparentcolor', 'green')
# global vars
color1 = "#2487fb"
color2 = "grey"
depth = 3
turn = 0  # 0 represents player turn and 1 represents commp turn
board = []
pruning = False
currentState = State("000000000000000000000000000000000000000000", -1)
# player color icon
playerImg = Image.open('./images/pink.jpg')
playertk = ImageTk.PhotoImage(playerImg)
# empty cell icon
img = Image.open('./images/grey.png')
tkImg = ImageTk.PhotoImage(img)
# comp color icon
compImg = Image.open('./images/blue.jpg')
comptk = ImageTk.PhotoImage(compImg)
# hint img
hintImg = Image.open('./images/hg.png')
hinttk = ImageTk.PhotoImage(hintImg)
hintRow = 0
hintCol = 0


# functions
def changeColor():  # swap colors between player and computer
    global color1
    global color2
    color1, color2 = color2, color1
    lblPscore["fg"] = color1
    lblCscore["fg"] = color2
    playerScoreTxt["foreground"] = color1
    compScoreTxt["foreground"] = color2


def showGraph():
    G = nx.Graph()
    edges = [(1, 2), (1, 6), (1, 3), (2, 4), (2, 5), (2, 7),
             (6, 12), (6, 13), (6, 14), (6, "1201201201201201201201201201201201201201200")]

    G.add_edges_from(edges)
    nx.draw_networkx(G)
    plt.show()


def showHint():
    global turn, depth, pruning
    if turn == 0:
        turn = 1
        changeDepth()
        maxEval, state = minimax_play(currentState, depth, False, pruning)
        depth = 3
        global hintRow, hintCol
        hintRow, hintCol = state.get_index()
        # highlight this cell for hint
        board[hintRow][hintCol]["image"] = hinttk
        turn = 0


def play(col):
    global turn, depth, currentState, pruning
    # human's turn
    if turn == 0:
        firstEmptyRow = currentState.first_empty_row(col)
        # if the position is valid
        if firstEmptyRow != -1:
            warning.delete(0.0, END)
            if board[hintRow][hintCol]["image"] == hinttk:
                board[hintRow][hintCol]["image"] = tkImg
            # should check for the right cell col only not row
            # change the board and add player's move
            row = firstEmptyRow
            board[row][col]["image"] = playertk
            # print(currentState.board)
            # print(currentState.player_move)
            currentState.game_play(col)
            playerScoreTxt.delete(0.0, END)
            # update the score
            compScore, pScore = currentState.calculate_score()
            playerScoreTxt.insert(END, str(pScore))
            turn = 1
            # computer's turn
            changeDepth()
            # call minimax
            maxEval, currentState = minimax_play(currentState, depth, True, pruning)

            # print(currentState.board)
            # print(currentState.player_move)
            depth = 3
            r, c = currentState.get_index()
            # add comp's move to the board
            board[r][c]["image"] = comptk
            compScoreTxt.delete(0.0, END)
            # update the score
            compScore, pScore = currentState.calculate_score()
            compScoreTxt.insert(END, str(compScore))
            turn = 0
        else:
            warning.insert(END, "Wrong Play")


def exitGame():
    window.destroy()


def changeDepth():  # update the required depth from the text box
    global depth
    d = depthText.get("1.0", END).rstrip()
    if d != "":
        depth = int(d)


def changePruning():  # enable or disable pruning
    global pruning
    if pruning:
        pruning = False
        pruningBtn["text"] = "Enable Pruning"
    else:
        pruning = True
        pruningBtn["text"] = "Disable Pruning"


# buttons and texts
# scores
lblPscore = Label(window, text="Player Score", bg="#d4c3e7", fg=color1, font="none 15 bold")
lblPscore.grid(row=0, column=0, sticky=W)
playerScoreTxt = Text(window, width=15, height=3, foreground=color1, borderwidth=0, font="none 15 bold", padx=55,
                      background="#d4c3e7")
playerScoreTxt.grid(row=1, column=0, sticky=W)
playerScoreTxt.insert(END, "0")
lblCscore = Label(window, text="Computer Score", bg="#d4c3e7", fg=color2, font="none 15 bold")
lblCscore.grid(row=0, column=1, sticky=W)
compScoreTxt = Text(window, width=15, height=3, foreground=color2, background="#d4c3e7", borderwidth=0,
                    font="none 15 bold", padx=60)
compScoreTxt.grid(row=1, column=1, sticky=W)
compScoreTxt.insert(END, "0")
# depth
Label(window, text="Depth:", bg="#d4c3e7", fg="#2487fb", font="none 15 bold").grid(row=2, column=0, sticky=W)
depthText = Text(window, width=8, height=1, foreground="black", background="white", borderwidth=0, font="none 15 bold")
depthText.grid(row=2, column=1, sticky=W)
# show graph button
graphBtn = Button(window, text="Show State Graph", width=15, background="#2487fb", foreground="white",
                  font="none 15 bold", command=showGraph)
graphBtn.grid(row=3, column=0, sticky=W)
# hint button
hintBtn = Button(window, text="Show Hint", width=15, background="#2487fb", foreground="white", font="none 15 bold",
                 command=showHint)
hintBtn.grid(row=4, column=0, sticky=W)
# warning
warning = Text(window, width=20, height=2, foreground="black", background="#d4c3e7", borderwidth=0, font="none 15 bold")
warning.grid(row=5, column=0, sticky=W)
# exit btn
exitBtn = Button(window, text="Exit Game", width=12, background="#2487fb", foreground="white", font="none 15 bold",
                 command=exitGame)
exitBtn.grid(row=7, column=0, sticky=W)
# pruning button
pruningBtn = Button(window, text="Enable Pruning", width=15, background="#2487fb", foreground="white",
                    font="none 15 bold", command=changePruning)
pruningBtn.grid(row=6, column=0, sticky=W)
# board
for i in range(1, 7):
    arr = []
    for j in range(2, 9):
        btn = Button(window, image=tkImg, width=100, height=110, background="#f5f3f3",
                     command=lambda col=j - 2: play(col), border=2)
        btn.grid(row=i, column=j)
        arr.append(btn)
    board.append(arr)

# window loop
window.mainloop()
