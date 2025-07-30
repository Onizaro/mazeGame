import numpy as np
import random
import os
import time
import keyboard
# set PYTHONWARNINGS=ignore to ignore warnings

##### basic funtions
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def createGrid(x):
    grid = np.zeros((x,x*3), dtype=object)
    return grid



def displayGrid(g):
    x,y = np.shape(g)
    f = g
    for i in range(x):
        for j in range(y):
            if (f[i][j]==0 ):
                print("█",end="")
            elif(f[i][j]==1):
                print(" ",end="")
            elif(f[i][j]==-1):
                print("@",end="")
        print('')



def updateGrid(g):
    height, width = g.shape

    # Initialiser tout en murs
    for i in range(height):
        for j in range(width):
            g[i][j] = 0

    def is_valid(x, y):
        return 0 < x < height-1 and 0 < y < width-1

    def carve(x, y):
        g[x][y] = 1
        directions = [(0,2), (0,-2), (2,0), (-2,0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and g[nx][ny] == 0:
                mx, my = x + dx//2, y + dy//2
                g[mx][my] = 1
                carve(nx, ny)

    # Lancer depuis une cellule impaire
    carve(1, 1)

    # Créer entrée et sortie
    for j in range(1, width, 2):
        if g[1][j] == 1:
            g[0][j] = 1
            break

    for j in range(width - 2, 0, -2):
        if g[height - 2][j] == 1:
            g[height - 1][j] = 1
            break


def move(m,g):
    x,y = np.shape(g)
    ax=0
    ay=0
    for i in range(x):
        for j in range(y):
            if (g[i][j]==-1):
                ax=i
                ay=j
    #1 up, 2 right, 3 down, 4 left
    if (m==1 and ax-1>0 and g[ax-1][ay]!=0):
        g[ax][ay]=1
        g[ax-1][ay]=-1

    if (m==3 and ax+1<x and g[ax+1][ay]!=0):
        g[ax][ay]=1
        g[ax+1][ay]=-1

    if (m==4 and ay-1>0 and g[ax][ay-1]!=0):
        g[ax][ay]=1
        g[ax][ay-1]=-1

    if (m==2 and ay+1<y and g[ax][ay+1]!=0):
        g[ax][ay]=1
        g[ax][ay+1]=-1


def gameFinished(g):
    if (g[-1][-2]==-1):
        return True
    else:
        return False



def startGame(g, level):
    clear_terminal()
    updateGrid(g)
    g[0][1] = -1  # position de départ du joueur

    size = g.shape[0]
    time_limit = size * 5
    start_time = time.time()

    while not gameFinished(g) and (time.time() - start_time < time_limit):
        clear_terminal()
        displayGrid(g)
        elapsed = int(time.time() - start_time)
        remaining = time_limit - elapsed
        print(f"\nTime remaining : {remaining} sec")
        print("Use the arrows to move (← ↑ → ↓). [ESC to leave]")

        moved = False
        while not moved:
            if keyboard.is_pressed("up"):
                move(1, g)
                moved = True
            elif keyboard.is_pressed("right"):
                move(2, g)
                moved = True
            elif keyboard.is_pressed("down"):
                move(3, g)
                moved = True
            elif keyboard.is_pressed("left"):
                move(4, g)
                moved = True
            elif keyboard.is_pressed("esc"):
                return False  # quitter le jeu
            time.sleep(0.05)  # évite que le CPU tourne en boucle trop vite

    clear_terminal()
    displayGrid(g)

    if gameFinished(g):
        print("\nCongratz, you won!")
    else:
        print("\nTime !!! You lost.")

    return True  # Partie jouée






#### main part
play = True

while(play):
    print("""
                          /$$
 /$$    | $$   /$$$$$    | $$       /$$$$$     /$$$$$     /$$    /$$    /$$$$$
| $$    | $$  /$$__  $$  | $$      /$$__  $$  /$$__  $$  | $$$  /$$$   /$$__  $$
| $$    | $$ | $$  \ $$  | $$     | $$  \__/ | $$  \ $$  | $$$$/$$$$  | $$  \ $$
| $$  $$$ $$ | $$$$$$$$  | $$     | $$       | $$  | $$  | $$ $$$ $$  | $$$$$$$$
|  $$$$ $$$/ | $$_____/  | $$     | $$       | $$  | $$  | $$___/ $$  | $$_____/
 \______/     \$$$$$$$$  | $$$$$$$ \$$$$$$$   \$$$$$$$   | $$   | $$   \$$$$$$$$
               \_______/ |_______/  \______/   \______/  |__/   |__/    \_______/
                              /$$
                             | $$      /$$$$$
                            /$$$$$$   /$$__  $$
                           |_  $$_/  | $$  \ $$
                             | $$    | $$  | $$
                             | $$    | $$  | $$
                             | $$$$$  \$$$$$$$
                             \_____/   \______/
              /$$                  /$$        /$$
             | $$        /$$$$    | $$       | $$         /$$  /$$
             | $$       /$$__ $$  | $$$$$$$  | $$$$$$$   | $$ | $$
             | $$      | $$  \ $$ | $$__  $$ | $$__  $$  | $$ | $$
             | $$      | $$  | $$ | $$  \ $$ | $$  \ $$  \ $$ $$
             | $$      | $$$$$$$$ | $$  | $$ | $$  | $$   \ $$$
             | $$$$$$$ |_____  $$ | $$$$$$$/ | $$$$$$$/    / $$
             |_______/       |__/ |_______/  |_______/    / $$

**********************************************************************************
**********************************************************************************
**********************************************************************************
          

          """)
    
    

    try:
        level = int(input("Please select the difficulty\n" \
    " - 1. easy\n" \
    " - 2. medium\n" \
    " - 3. hard\n"))
        if (level!=1 and level !=2 and level!=3):
            raise ValueError('A very specific bad thing happened.')
    except:
        print("Error while selecting the level, easy is the default level")

    if (level==3):
        g=createGrid(35)
    elif (level==2):
        g=createGrid(25)
    else :
        g=createGrid(15)

    if startGame(g, level) == False:
        pass  # ESC pressé = quitter le jeu

    # Après la partie, proposer de rejouer
    try:
        retry = int(input("\nReplay ?\n - 1. yes\n - 2. no\n "))
        if retry == 2:
            play = False
    except:
        play = False

    
      
       
