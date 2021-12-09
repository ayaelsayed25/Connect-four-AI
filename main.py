from tkinter import *
from PIL import Image, ImageTk
from minimax import *
from state import *
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go

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
depth = 3
turn = 0  # 0 represents player turn and 1 represents commp turn
board = []
pruning = False
currentState = State("000000000000000000000000000000000000000000", -1)
board_expansion = []
score_expansion = []
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

def showGraph():
    # minmaxGraph = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
    #                20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
    #                39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
    #                59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,
    #                78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
    #                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
    #                20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
    #                39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
    #                59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,
    #                78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100
    #                ]
    nr_vertices = len(score_expansion)
    print(score_expansion)
    print(board_expansion)
    G = Graph.Tree(nr_vertices, 7)  # 2 stands for children number
    lay = G.layout('tree')

    position = {k: lay[k] for k in range(nr_vertices)}
    Y = [lay[k][1] for k in range(nr_vertices)]
    M = max(Y)

    es = EdgeSeq(G)  # sequence of edges
    E = [e.tuple for e in es]  # list of edges

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2 * M - position[k][1] for k in range(L)]
    Xe = []
    Ye = []
    for edge in E:
        Xe += [position[edge[0]][0], position[edge[1]][0], None]
        Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]

    def make_annotations(pos, text, font_size=10, font_color='rgb(250,250,250)'):
        L = len(pos)
        if len(text) != L:
            raise ValueError('The lists pos and text must have the same len')
        annotations = []
        for k in range(L):
            annotations.append(
                dict(
                    text=score_expansion[k],  # or replace labels with a different list for the text within the circle
                    x=pos[k][0], y=2 * M - position[k][1],
                    xref='x1', yref='y1',
                    font=dict(color=font_color, size=font_size),
                    showarrow=False)
            )
        return annotations

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe,
                             y=Ye,
                             mode='lines',
                             line=dict(color='rgb(210,210,210)', width=1),
                             hoverinfo='none'
                             ))
    fig.add_trace(go.Scatter(x=Xn[0:1],
                             y=Yn[0:1],
                             mode='markers',
                             name='bla',
                             marker=dict(symbol='circle-dot',
                                         size=50,
                                         color='#DB4551',  # '#DB4551',
                                         line=dict(color='rgb(50,50,50)', width=1)
                                         ),
                             text=board_expansion[0:1],
                             hoverinfo='text',
                             opacity=0.8
                             ))
    fig.add_trace(go.Scatter(x=Xn[1:],
                             y=Yn[1:],
                             mode='markers',
                             name='bla',
                             marker=dict(symbol='circle-dot',
                                         size=50,
                                         color="#00294F",  # '#DB4551',
                                         line=dict(color='rgb(50,50,50)', width=1)
                                         ),
                             text=board_expansion[1:],
                             hoverinfo='text',
                             opacity=0.8
                             ))

    axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                )

    fig.update_layout(title='Tree Expansion',
                      annotations=make_annotations(position, score_expansion),
                      font_size=12,
                      showlegend=False,
                      xaxis=axis,
                      yaxis=axis,
                      margin=dict(l=40, r=40, b=85, t=100),
                      hovermode='closest',
                      plot_bgcolor='rgb(248,248,248)'
                      )
    fig.show()


def showHint():
    global turn, depth, pruning
    if turn == 0:
        turn = 1
        changeDepth()
        maxEval, state = minimax(currentState, depth, False, pruning)
        depth = 3
        global hintRow, hintCol
        hintRow, hintCol = state.get_index()
        # highlight this cell for hint
        board[hintRow][hintCol]["image"] = hinttk
        turn = 0


def play(col):
    global turn, depth, currentState, pruning,board_expansion, score_expansion, hintRow, hintCol
    # human's turn
    if turn == 0:
        # print(col)
        # print(currentState.board)
        firstEmptyRow = currentState.first_empty_row(col)
        print(firstEmptyRow)
        # if the position is valid
        if firstEmptyRow != -1:
            warning.delete("1.0", END)
            row = firstEmptyRow
            if board[row][col]["image"] == hinttk:
                board[hintRow][hintCol]["image"] = playertk
                hintRow = None
                hintCol = None
            elif hintCol != None and hintRow != None:
                board[hintRow][hintCol]["image"] = tkImg
                hintRow = None
                hintCol = None
            # should check for the right cell col only not row
            # change the board and add player's move
            board[row][col]["image"] = playertk
            window.update()
            # print(currentState.board)
            # print(currentState.player_move)
            currentState.game_play(col)
            playerScoreTxt.delete("1.0", END)
            # update the score
            compScore, pScore = currentState.calculate_score()
            playerScoreTxt.insert(END, str(pScore))
            window.update()
            turn = 1
            # computer's turn
            changeDepth()
            # call minimax
            maxEval, currentState, board_expansion, score_expansion = minimax_play(currentState, depth, True, pruning)

            # print(currentState.board)
            # print(currentState.player_move)
            depth = 3
            r, c = currentState.get_index()
            # add comp's move to the board
            board[r][c]["image"] = comptk
            compScoreTxt.delete("1.0", END)
            # update the score
            compScore, pScore = currentState.calculate_score()
            compScoreTxt.insert(END, str(compScore))
            window.update()
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
lblPscore = Label(window, text="Player Score", bg="#d4c3e7", fg="#4d5054", font="none 17 bold")
lblPscore.grid(row=1, column=0, sticky=W)
playerScoreTxt = Text(window, width=15, height=3, foreground="#4d5054", borderwidth=0, font="none 17 bold", padx=55,
                      background="#d4c3e7")
playerScoreTxt.grid(row=2, column=0, sticky=W)
playerScoreTxt.insert(END, "0")
lblCscore = Label(window, text="Computer Score", bg="#d4c3e7", fg="#4d5054", font="none 17 bold")
lblCscore.grid(row=1, column=1, sticky=W)
compScoreTxt = Text(window, width=15, height=3, foreground="#4d5054", background="#d4c3e7", borderwidth=0,
                    font="none 17 bold", padx=60)
compScoreTxt.grid(row=2, column=1, sticky=W)
compScoreTxt.insert(END, "0")
# depth
Label(window, text="Depth:", bg="#d4c3e7", fg="#4d5054", font="none 15 bold").grid(row=3, column=0, sticky=W)
depthText = Text(window, width=8, height=1, foreground="black", background="white", borderwidth=0, font="none 15 bold")
depthText.grid(row=3, column=1, sticky=W)
# show graph button
graphBtn = Button(window, text="Show State Graph", width=15, background="#2487fb", foreground="white",
                  font="none 15 bold", command=showGraph)
graphBtn.grid(row=4, column=0, sticky=W, padx=50)
# hint button
hintBtn = Button(window, text="Show Hint", width=15, background="#2487fb", foreground="white", font="none 15 bold",
                 command=showHint)
hintBtn.grid(row=5, column=0, sticky=W, padx=50)
# exit btn
exitBtn = Button(window, text="Exit Game", width=15, background="#2487fb", foreground="white", font="none 15 bold",
                 command=exitGame)
exitBtn.grid(row=6, column=0, sticky=W, padx=50)
# pruning button
pruningBtn = Button(window, text="Enable Pruning", width=15, background="#2487fb", foreground="white",
                    font="none 15 bold", command=changePruning)
pruningBtn.grid(row=7, column=0, sticky=W, padx=50)
# warning
warning = Text(window, width=20, height=2, foreground="black", background="#d4c3e7", borderwidth=0, font="none 15 bold")
warning.grid(row=8, column=0, sticky=W, padx=50)
# board
for i in range(2, 8):
    arr = []
    for j in range(2, 9):
        btn = Button(window, image=tkImg, width=100, height=100, background="#f5f3f3",
                     command=lambda col=j - 2: play(col), border=2)
        btn.grid(row=i, column=j)
        arr.append(btn)
    board.append(arr)
turn = 1
# computer's turn
changeDepth()
# call minimax
maxEval, currentState, board_expansion, score_expansion = minimax_play(currentState, depth, True, pruning)
depth = 3
r, c = currentState.get_index()
# add comp's move to the board
board[r][c]["image"] = comptk
compScoreTxt.delete("1.0", END)
# update the score
compScore, pScore = currentState.calculate_score()
compScoreTxt.insert(END, str(compScore))
window.update()
turn = 0
# window loop
window.mainloop()
