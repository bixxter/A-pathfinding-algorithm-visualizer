import pygame
import sys
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os

#window init---
width = 600
height = 600
screen = pygame.display.set_mode((width, height))


class Spot:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None
        self.obs = False
        self.closed = False
        self.value = 1

    def show(self, color, st):
        if self.closed == False :
            pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
            pygame.display.update()

    def path(self, color, st):
        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
        pygame.display.update()
    def addNeighbors(self, grid):
        i = self.i
        j = self.j
        if i < cols-1 and grid[self.i + 1][j].obs == False:
            self.neighbors.append(grid[self.i + 1][j])
        if i > 0 and grid[self.i - 1][j].obs == False:
            self.neighbors.append(grid[self.i - 1][j])
        if j < row-1 and grid[self.i][j + 1].obs == False:
            self.neighbors.append(grid[self.i][j + 1])
        if j > 0 and grid[self.i][j - 1].obs == False:
            self.neighbors.append(grid[self.i][j - 1])
#grid init
cols = 100
row = 100
grid = [0 for i in range(cols)]
openSet = []
closedSet = []
w = width / cols
h = height / row
cameFrom = []
d_h = 2
#colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (220, 220, 220)
#create 2d array
for i in range(cols):
    grid[i] = [0 for i in range(row)]

#create Spots
for i in range(cols):
    for j in range(row):
        grid[i][j] = Spot(i, j)
#
start = grid[1][1]
end = grid [10][10]
# SHOW RECT
for i in range(cols):
    for j in range(row):
        grid[i][j].show((255, 0, 255), 1)
def onsubmit():
    global start
    global end
    st = startBox.get().split(',')
    ed = endBox.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    window.quit()
    window.destroy()
window = Tk()
label = Label(window, text='Star point(x,y): ')
startBox = Entry(window)
label1 = Label(window, text='End poin(x,y): ')
endBox = Entry(window)
var = IntVar()
showPath = ttk.Checkbutton(window, text='Show steps:', onvalue=1, offvalue=0, variable=var)
submit = Button(window, text='Start', command=onsubmit)
submit.grid(columnspan=2, row=4)
showPath.grid(columnspan=2, row=3)
label1.grid(row=1, pady=3)
endBox.grid(row=1, column=1, pady=3)
startBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)


window.update()
mainloop()

start.show((0, 255, 162), 0)
end.show((255, 238, 0), 0)

pygame.init()
openSet.append(start)
def grid_pos(x):
    t = x[0]
    w = x[1]
    g1 = t // (width // cols)
    g2 = w // (height // row)
    return grid[g1][g2]
def mousePress(x):
    acess = grid_pos(x)
    if acess != start and acess != end:
        if acess.obs == False:
            acess.obs = True
            acess.show((255, 255, 255), 0)

done = False
while not done:
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                done = True
                break

for i in range(cols):
    for j in range(row):
        grid[i][j].addNeighbors(grid)

def heurisitic(n, e):
    d = math.sqrt((n.i - e.i)**2 + (n.j - e.j)**2) #Euclide method
    #d = max(abs(n.i - e.i), abs(n.j - e.j)) #Dioganal method
    #d = abs(n.i - e.i)+ abs(n.j - e.j) #Manhattan method
    return d
def main():
    end.show((255, 0, 127), 0)
    start.show((255, 8, 127), 0)
    if len(openSet) > 0:
        lowestIndex = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowestIndex].f:
                lowestIndex = i

        current = openSet[lowestIndex]
        if current == end:
            print('done', current.f)
            start.show((255,8,127),0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.show((0,0,255), 0)
                current = current.previous
            end.show((255, 8, 127), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Поиск завершен!', ('Программа завершила поиск, кратчайшая \n дистанция до цели в ' + str(temp) + ' блоках, \n Хотели бы вы перезапустить прорамму?'))
            if result == True:
                os.execl(sys.executable,sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()

        openSet.pop(lowestIndex)
        closedSet.append(current)

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            if neighbor not in closedSet:
                tempG = current.g + current.value
                if neighbor in openSet:
                    if neighbor.g > tempG:
                        neighbor.g = tempG
                else:
                    neighbor.g = tempG
                    openSet.append(neighbor)

            neighbor.h = heurisitic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor.previous == None:
                neighbor.previous = current
    if var.get():
        for i in range(len(openSet)):
            openSet[i].show(green, 0)

        for i in range(len(closedSet)):
            if closedSet[i] != start:
                closedSet[i].show(red, 0)
    current.closed = True

def sel():
    selection = "Value = " + str(int(var.get())//10) + 's'
    label.config(text = selection)
    root.quit()
    root.destroy()
root = Tk()
var = DoubleVar()
scale = Scale( root, variable = var )
scale.pack(anchor=CENTER)

button = Button(root, text="Speed of visualization", command=sel)
button.pack(anchor=CENTER)

label = Label(root)
label.pack()
mainloop()

while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    pygame.time.delay((int(var.get()))*10)

    main()
