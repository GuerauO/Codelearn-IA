import pygame
from pygame.locals import *
from random import randint

XO   = "X" # determina qui juga
grid = [ [ None, None, None ], \
         [ None, None, None ], \
         [ None, None, None ] ] # representa el taulell
winner = None # determina el guanyador, si nhi ha
screenLock = False # determina si el joc s'ha acabat

def playCircles(board):
    global grid # guanyem acces a la variable globar grid

    if (emptySlots() == 0): return # si no podem jugar, no juguem

    r, c = attack(board) # intentem 'atacar' es a dir si hi ha cap
                         # jugada que ens faci guanyar directament la fem
    if (r == -1 and c == -1): # si no hem pogut atacar, defensem
        r, c = defend(board)  # si hi ha alguna jugada que fa que laltre guanyi, la bloquejem
    
    if (r == -1 and c == -1): # si no hem pogut ni atacar ni defensar, juguem random
        while (r == -1 or grid[r][c] != None):
            r = randint(0,2)
            c = randint(0,2)

    clickMatrix(r,c,board)

def defend(board):
    global grid # guanyem acces a la variable globar grid

    for i in range(3): 
        for j in range(3):
            if not (grid[i][j] is None): continue

            # si al posar x, x guanya, no el deixis, posa O
            grid[i][j] = 'X'
            
            if(gameWon(board, 'check')): # do not draw, only check
                grid[i][j] = None
                return (i, j)
            
            grid[i][j] = None
    # si no hem pogut defensar, al menys fem una jugada bona si podem
    # si el centre esta buit, agafem el centre
    if (grid[1][1] is None):
        return 1, 1
    # si es la segona jugada i ens han jugat al centre, agafem una cantonada
    # si agafessim un costat, hi ha una estrategia que ens fa perdre
    if (emptySlots() == 8):
        r = randint(0, 1)*2
        c = randint(0, 1)*2
        return (r, c)
    # si no es dona cap dels 3 casos dadalt, no juguem
    return (-1, -1)

def attack(board):
    global grid

    # si hi ha alguna jugada que ens fa guanyar, la fem
    for i in range(3): 
        for j in range(3):
            if not (grid[i][j] is None): continue

            # si al posar x, x guanya, no el deixis, posa O
            grid[i][j] = 'O'
            
            if(gameWon(board, 'check')): # do not draw, only check
                grid[i][j] = None
                return (i, j)
            
            grid[i][j] = None
    # sino, no juguem
    return (-1, -1)

# inizialitza la taula
def initBoard(ttt):
    # initialize the board and return it as a variable
    # ---------------------------------------------------------------
    # ttt : a properly initialized pyGame display variable

    # set up the background surface
    background = pygame.Surface (ttt.get_size())
    background = background.convert()
    background.fill ((250, 250, 250))

    # draw the grid lines
    # vertical lines...
    pygame.draw.line (background, (0,0,0), (100, 0), (100, 300), 2)
    pygame.draw.line (background, (0,0,0), (200, 0), (200, 300), 2)

    # horizontal lines...
    pygame.draw.line (background, (0,0,0), (0, 100), (300, 100), 2)
    pygame.draw.line (background, (0,0,0), (0, 200), (300, 200), 2)

    # return the board
    return background

# retorna el nombre de caselles buides
def emptySlots():
    global grid
    eS = 0
    for i in range(3):
        for j in range(3):
            if(grid[i][j] == None):
                eS += 1
    return eS

# dibuixa el missatge
def drawStatus (board):
    global XO, winner, screenLock
    if (screenLock): return;

    # determine the status message
    if (winner is None):
        if (emptySlots() == 0):
            message = "Empat!"
        else: message = ""
    else:
        message = winner + " ha guanyat!"
        
    # render the status message
    font = pygame.font.Font(None, 24)
    text = font.render(message, 1, (10, 10, 10))

    # copy the rendered message onto the board
    board.fill ((250, 250, 250), (0, 300, 300, 25))
    board.blit(text, (10, 300))

# dibuixa la taula
def showBoard (ttt, board):
    # redraw the game board on the display
    # ---------------------------------------------------------------
    # ttt   : the initialized pyGame display
    # board : the game board surface

    drawStatus (board)
    ttt.blit (board, (0, 0))
    pygame.display.flip()
    
# calcula la posicio clickada de la matriu
# a partir de les posicions del mouse
def boardPos (mouseX, mouseY):
    # given a set of coordinates from the mouse, determine which board space
    # (row, column) the user clicked in.
    # ---------------------------------------------------------------
    # mouseX : the X coordinate the user clicked
    # mouseY : the Y coordinate the user clicked

    # determine the row the user clicked
    if (mouseY < 100):
        row = 0
    elif (mouseY < 200):
        row = 1
    else:
        row = 2

    # determine the column the user clicked
    if (mouseX < 100):
        col = 0
    elif (mouseX < 200):
        col = 1
    else:
        col = 2

    # return the tuple containg the row & column
    return (row, col)

# dibuixa la X o la O corresponent
def drawMovement (board, boardRow, boardCol, Piece):
    # determine the center of the square
    centerX = ((boardCol) * 100) + 50
    centerY = ((boardRow) * 100) + 50

    # draw the appropriate piece
    if (Piece == 'O'):
        pygame.draw.circle (board, (0,0,0), (centerX, centerY), 24, 2)
    else:
        pygame.draw.line (board, (0,0,0), (centerX - 22, centerY - 22), \
                         (centerX + 22, centerY + 22), 2)
        pygame.draw.line (board, (0,0,0), (centerX + 22, centerY - 22), \
                         (centerX - 22, centerY + 22), 2)

    # mark the space as used
    grid [boardRow][boardCol] = Piece

# processa els clicks a la pantalla
def clickBoard(board):
    global grid, XO, screenLock
    if (screenLock): return;
    
    (mouseX, mouseY) = pygame.mouse.get_pos()
    (row, col) = boardPos(mouseX, mouseY)

    clickMatrix(row, col, board)

# processa els nous moviments, tant per click com per IA

def clickMatrix(fila, columna, tauler):
    global grid, XO, screenLock # screenLock --> GameOver
    if(screenLock == True):     #if(screenLock): return
        return
    
    if((grid[fila, columna] == 'X'), (grid[fila][columna] == 'O')):
        return
    
    drawMovement(tauler, fila, columna, XO)
    
    if(XO == 'X'):
        XO = 'O'
        
        screenLock = gameWon(tauler, 'draw')
        playCircles(tauler)
    else:
        XO = 'X'
        
        screenLock = gameWon(tauler, 'draw')
        
        
def gameWon(tauler, mode):
    global grid, winner, screenLock # winner = guanyador i screenLock = gameOver
    if(screenLock): return
    
    for fila in range(3):
        if((grid[fila][0] == grid[fila][1] == grid[fila][2])and(grid[fila][0] is not None)):
            
            if(mode == 'draw'):
                winner = grid[fila][0]
                pygame.draw.line(tauler, (255, 0, 0), (0, (fila +1)*100 -50), (300, (fila + 1)*100 -50), 2)
            
            return True
        
    for col in range(3):
        if((grid[0][col] == grid[1][col] == grid[2][col])and(grid[0][col] is not None)):
           
            if(mode == 'draw'):
                winner = grid[0][col]
                pygame.draw.line(tauler, (255, 0, 0), ((col +1)*100 -50, 0), ((col +1)*100 -50), 300, 2)
            
            return True
    
    if((grid[0][0] == grid[1][1] == grid[2][2]) and (grid[0][0] != None)):
       if(mode == 'draw'):
           winner = grid[0][0]
           pygame.draw.line(tauler, (255, 0, 0), (50, 50), (250, 250), 2)
       return True    
           
           
    if((grid[0][2] == grid[1][1] == grid[2][0]) and (grid[1][1] != None)):
        if(mode == 'draw'):
            winner = grid[1][1]
            pygame.draw.line(tauler, (255, 0, 0), (50, 250), (50, 250), 2)
        
        return True

    
    return False    
           

def main(): 
    global screenLock # screenLock = gameOver

    pygame.init()
    
    ttt = pygame.display.set_mode((300,325))
    pygame.display.set_caption('3 en Ratlla')

    tauler = initBoard(ttt)

    running = 1
    
    while running ==1:
        if(drawStatus(tauler)):
            for event in pygame.event.get():
                if(event.type is QUIT):
                    running = 0
                elif event.type is MOUSEBUTTONDOWN:
                    if(screenLock == False):
                        clickBoard(tauler)
        
                
                screenLock = gameWon(tauler, 'draw')
                
                
                drawStatus(tauler)
                
                showBoard(ttt, tauelr)
        
    
if __name__ == '__main___': main()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    