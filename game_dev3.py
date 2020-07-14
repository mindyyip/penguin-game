import math, random, time, copy
from tkinter import *
import sys, os
from PIL import Image, ImageTk

tag = 0
count = 0
score = 0
lives = 3
loops = 0
limit = 425
interval = 10
maximum = 0
class Cons():
    #-------variables + constants-------
    bgFile = "background.png"
    bg2File = "instructions.png"
    penguin = "pg_ice_bkt.png"
    fish = "fish.png"
    w = 1000   #width
    h = 1200    #height
    ch = int(h*2/3)
    charw = 125
    charh = 200
    fw = 70
    fh = 50

class Fish:
    def __init__(self, canvas, x_loc, y_loc):
        global tag
        self.x = x_loc
        self.y = y_loc
        self.xend = self.x + Cons.fw
        self.canvas = canvas
        self.tag = "fish" + str(tag)
        tag += 1
        self.fishig = ImageTk.PhotoImage(Image.open(Cons.fish).convert("RGBA").resize((Cons.fw,Cons.fh), Image.ANTIALIAS))
        self.fish = self.canvas.create_image(self.x, self.y , anchor=NW, image=self.fishig, tag=self.tag)
        self.alive = True

    def move_fish(self):
        global dist, score, count, lives, limit, interval, loops, maximum
        self.canvas.move(self.tag,0,1)
        self.y += 1
        count += 1
        if count == limit:
            if maximum < 3:
                start_fish(self.canvas)
                maximum += 1
            if loops == 3:
                loops = 0
                if limit > 460:
                    limit -= interval
            loops += 1
            count = 0


        if self.y >= 330+Cons.charh-Cons.fh: #498 penguin
            if self.y > 600:
                self.canvas.delete(self.tag)
                lives -= 1
                maximum -= 1
                self.alive = False;
                updateLives(self.canvas)

            if self.x >= dist and self.xend <= dist + Cons.charw:
                score += 100
                self.alive = False;
                updateScore(self.canvas)
                self.canvas.delete(self.tag)
                maximum -= 1
        if lives and self.alive:
            self.canvas.after(10, self.move_fish)
        elif not lives:
            self.canvas.create_text(Cons.w /2, Cons.ch/2,
                text="Game Over with score {0}".format(score), font=("Courier", 24), fill="black")


class Penguin:
    def __init__(self, canvas, x_loc, y_loc):
        global dist
        self.x = x_loc
        dist = self.x
        self.y = y_loc
        self.canvas = canvas
        self.w = Cons.charw
        self.h = Cons.charh
        self.ig = ImageTk.PhotoImage(Image.open(Cons.penguin).convert("RGBA").resize((self.w,self.h), Image.ANTIALIAS))
        self.mainI = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.ig)

        self.canvas.bind_all("<Key>", self.movePenguin)

    def movePenguin(self, event):
        global dist

        key = event.keysym
        keyRight = True
        if key == "Right" and self.x < (Cons.w - 120):
            self.x += 10
            dist += 10
            self.canvas.move(self.mainI, 10, 0)
        elif key == "Left" and self.x > 0:
            self.x -= 10
            dist -= 10
            self.canvas.move(self.mainI, -10, 0)

def updateLives(canvas):
        canvas.delete("lives")
        canvas.create_text(100, 20,
        text="Lives: {0}".format(lives), fill="black", font=("Courier", 24), tag="lives")
def updateScore(canvas):
    canvas.delete("score")
    canvas.create_text(Cons.w - 110, 20,
    text="Score: {0}".format(score), fill="black", font=("Courier", 24), tag="score")

def start_fish(canvas):
    pos = random.randint(20, Cons.w-80)
    fish = Fish(canvas, pos, 30)
    fish.move_fish()

def restart(canvas):
    global score, lives
    score = 0
    lives = 3
    updateLives(canvas)
    updateScore(canvas)

def help_screen(canvas):
    root2 = Toplevel()
    root2.title('Help Instructions')
    root2.resizable(False,False)
    bg2_image = ImageTk.PhotoImage(Image.open(Cons.bg2File).resize((300,300), Image.ANTIALIAS))
    canvas2 = Label(root2,width=300,height=300, image=bg2_image)
    canvas2.place(x=0, y=0, relwidth=1, relheight=1)
    canvas.image=bg2_image
    canvas2.pack()

def addButton(parent, txt, location):
    button = Button(parent, text=txt, width=20, padx="2m", pady="2m")
    button.pack(side=location)
    return button

def main():
    root = Tk()
    root.title("Penguin Game")
    root.resizable(False,False)

    #-------canvas set up-----
    main_frame = Frame(root, width=Cons.w, height=Cons.h)
    canvas = Canvas(root, width=Cons.w, height=Cons.ch)
    canvas.pack(side=TOP)

    #-----------background------------
    bg_image = ImageTk.PhotoImage(Image.open(Cons.bgFile).resize((Cons.w,Cons.ch), Image.ANTIALIAS))
    bg = canvas.create_image(0,0,anchor=NW, image = bg_image)


    #-------button set up----------------------------
    button_frame = Frame(main_frame)
    button_frame.pack(side=BOTTOM)
    start_button = addButton(button_frame, "Restart", LEFT)
    start_button.configure(command=lambda:restart(canvas))
    help_button = addButton(button_frame, "Help", RIGHT)
    help_button.configure(command=lambda:help_screen(canvas))

    global score, lives
    canvas.create_text(Cons.w - 110, 20,
        text="Score: {0}".format(score), fill="black", font=("Courier", 24), tag="score")
    canvas.create_text(100, 20,
        text="Lives: {0}".format(lives), fill="black", font=("Courier", 24), tag="lives")

    penguin = Penguin(canvas, 250, 498)
    seconds = 8000

    #----------- fish--------------
    start_fish(canvas)
    main_frame.pack()
    root.mainloop()

# Driver code
if(__name__=="__main__"):
	main()
