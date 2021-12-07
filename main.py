from tkinter import *
#global vars
color1 = "red"
color2 = "grey"
# functions
def changeColor():
    global color1
    global color2
    color1,color2 = color2,color1
    lblPscore.config(fg=color1)
    lblCscore.config(fg=color2)
    playerScoreTxt.config(foreground=color1)
    compScoreTxt.config(foreground=color2)

# configure window
window = Tk()
window.title("Connect-four Game")
window.configure(background="black")
# buttons and texts

lblPscore = Label(window, text="Player Score", bg="black", fg=color1, font="none 12 bold")
lblPscore.grid(row=0, column=0, sticky=W)
playerScoreTxt=Text(window, width=15, height=3, foreground=color1, background="black", borderwidth=0, font="none 12 bold", padx=55)
playerScoreTxt.grid(row=1, column=0, sticky=W)
playerScoreTxt.insert(END, 0)
lblCscore = Label(window, text="Computer Score", bg="black", fg=color2, font="none 12 bold")
lblCscore.grid(row=0, column=1, sticky=W)
compScoreTxt=Text(window, width=15, height=3, foreground=color2, background="black", borderwidth=0, font="none 12 bold", padx=60)
compScoreTxt.grid(row=1, column=1, sticky=W)
compScoreTxt.insert(END, 0)
# window loop
window.mainloop()