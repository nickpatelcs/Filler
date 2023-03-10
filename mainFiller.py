from cmu_graphics import *
import random
import string

#OOP requirement
#creates a player class that takes a name upon initialization
#holds a list for the squares that are controlled
#holds a variable for the number of squares they control
#would allow for easier implementation of a 2+ player version
class Player:
    def __init__(self, name):
        self.squares = []
        self.name = name
        self.score = len(self.squares)
        
    def __repr__(self):
        return len(self.squares)
        
    def addSquares(self,row,col):
        #player lists contain tuples of the (row,col) for each square they control
        self.squares.append((row,col))
        self.score = len(self.squares)
        
        
def onAppStart(app):
    #initializes the game
    app.counter = 0
    app.player1,app.player2 = Player('default'), Player('default')
    app.rows = 7
    app.cols = 8
    app.boardWidth = 300*(8/7)
    app.boardLeft = 200-app.boardWidth/2    
    app.boardHeight = 300
    app.boardTop = 175-app.boardHeight/2 
    app.cellBorderWidth = 2
    app.board = [[[None] for i in range(app.cols)] for i in range(app.rows)]
    app.starting = True
    #initializes both player1 and player2 using the custom names from above
    app.name = 1
    app.message = ''
    
    #app.turn is an alias of the list of whoevers turn it is
    app.turn = app.player1
    
    app.colors = ['deepSkyBlue', rgb(255,250,0), rgb(59,59,59), rgb(220,40,100), rgb(116,89,168), rgb(161,245,79)]
    createBoard(app)
    app.notPlayable = [app.board[6][0], app.board[0][7]]
    app.animate = 0
    app.size = getCellSize(app)[0]
    app.click = 0
    app.over = False
    app.up = False
    
#assigns each cell a color, ensuring no colors are adjacent to each other
def createBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            color = app.colors[random.randrange(0,6)]
            while not searchSurrounding(app,row,col,color):
                color = app.colors[random.randrange(0,6)]
                
            if col == 0 and row == 6:
                while color == app.board[0][7]:
                    color = app.colors[random.randrange(0,6)]
            app.board[row][col] = color
            
#searches neighboring cells (not diagonals) and checks if they are the same color as the cell parameter
def searchSurrounding(app,row,col,color):
    index = [-1, 1]
    
    for i in index:
        try:
            if app.board[row+i][col] == color and row+i>-1:
                return False
                
            if app.board[row][col+i] == color and col+i>-1:
                return False
        except:
            continue
    return True
    
#draws all necessary graphics (persistent object graphics)
def redrawAll(app):
    #bolds the label for whoever's turn it is
    if app.turn == app.player1:
        isBold = True
    else:
        isBold = False
        
    
    if app.over:
        if app.player1.score != app.player2.score:
            drawLabel(f'{app.turn.name} wins!', 200, 12, size=25, bold = True)
        else:
            app.turn.squares = app.player1.squares + app.player2.squares
            drawLabel(f'Tie game!', 200, 12, size=25, bold = True)
    else:
        drawLabel(f'{app.turn.name}\'s Turn!', 200, 12, size=25, bold = True)
    drawLabel(f'{app.player1.name}: {app.player1.score}', 29, 12, size=16,align='left', bold = isBold)
    drawLabel(f'{app.player2.name}: {app.player2.score}', 371, 12, size=16, align='right', bold = not isBold)
    
    #draws gradient rectangles behind the main grid, so that there appears to be a shadow on the left and bottom side
    drawRect(361, 315, 20, 20, fill = gradient('lightgrey', 'white', start = 'left-top'), opacity =100)
    drawRect(app.boardLeft+app.boardWidth, app.boardTop, 10, app.boardHeight, fill = gradient('lightgrey', 'white', start = 'left'))
    drawRect(app.boardLeft, app.boardTop+app.boardHeight, app.boardWidth, 10, fill = gradient('lightgrey', 'white', start = 'top'))
    
    #draws the main grid
    drawBoard(app)
    
    #calls drawcell again for squares that are controlled by a player, this ensures that 
    #animated tiles are drawn overtop of the grid while they grow
    for row in range(app.rows):
        for col in range(app.cols):
            if (row,col) in app.turn.squares:
                drawCell(app,row,col)
    
    #draws the selection squares at the bottom
    drawSquares(app)
    
    #draws a transparent square over the canvas, so colors appear more pastel
    drawRect(0, 0, 400, 400, fill = 'white', opacity = 15)
    
    drawStart(app)
    
#draws the textbox for names at the start, and hides everything else with a white rectangle
#fades away once names are entered
def drawStart(app):
    drawRect(0,0,400,400,fill=gradient('lightCyan', 'paleTurquoise',start = 'top'), opacity = 100-app.counter*2)
    drawRect(200-275/2, 200-100/2, 275,100, fill = gradient('white', 'whitesmoke',start = 'top'), borderWidth = 4, border = 'black', opacity = 100-app.counter*2)
    drawLabel(f'Enter Player {app.name}\'s Name:', 200, 170, size=20, opacity = 100-app.counter*2)
    drawRect(200-225/2, 200-30/2, 225,30, fill = 'white', borderWidth = 2, border = 'black', opacity = 100-app.counter*2)
    drawLabel(app.message, 210-225/2, 215-30/2, align='left', size = 15, opacity = 100-app.counter*2)
    
    
#draws the 6 colors as squares on the bottom, if a color cannot be selected it is drawn smaller
def drawSquares(app):
    for i in range(len(app.colors)):
        if app.colors[i] not in app.notPlayable:
            #shadow
            drawRect(app.boardLeft+i*61.1, 345, 50, 50, fill = gradient('lightgrey', 'white'))
            #square
            drawRect(app.boardLeft+i*61.1, 345, 45, 45, fill = app.colors[i])
            
        else:
            #shadow
            drawRect(app.boardLeft+i*61.1+25/2, 345+25/2, 28, 28, fill = gradient('lightgrey', 'white'))
            #square
            drawRect(app.boardLeft+i*61.1+25/2, 345+25/2, 25, 25, fill = app.colors[i])

#calls drawCell for each cell on the board
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

#draws each individual cell
def drawCell(app, row, col):
    #retrieves the top left xy coordinate, and the width and height
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    
    #uses a size variable so that the size can be animated if a square is selected
    if (row,col) in app.turn.squares and app.size!= cellWidth:
        size = app.size
        takeaway = cellWidth/2 - app.size/2
    else:
        size = cellWidth
        takeaway = 0
        
    #draws the cell
    if (row,col) not in app.turn.squares:
        drawRect(cellLeft+takeaway, cellTop+takeaway, size, size,
                fill=app.board[row][col], border=app.board[row][col],
                borderWidth=app.cellBorderWidth)
    
    #if the cell is controlled by the current player, it draws a white square ontop of it
    #with animated transparency to look like the cell is flashing
    if (row,col) in app.turn.squares:
        drawRect(cellLeft+takeaway, cellTop+takeaway, size, size,
                fill=app.board[row][col], border=app.board[row][col],
                borderWidth=app.cellBorderWidth)
        drawRect(cellLeft+takeaway-.5, cellTop+takeaway-.5, size+1, size+1,
                fill='white', opacity = app.animate)
        

#returns topleft x and y based on row and col
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

#returns cell Width and Height based on width and height of board
def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
    

def onKeyPress(app,key):
    #controls the name input field for the start
    if app.starting:
        if app.name == 1:
            typeFunction(app,key)
            if key == 'enter':
                app.name+=1
                app.player1=Player(app.message)
                app.player1.addSquares(6,0)
                app.message = ''
        else:
            typeFunction(app,key)
            if key == 'enter':
                app.player2=Player(app.message) 
                app.player2.addSquares(0,7)
                app.turn = app.player1
                app.starting = False

#changes app.message to the name being typed
def typeFunction(app,key):
    if key == 'backspace':
        app.message = app.message[:-1]
    if key == 'space':
        app.message += ' '
    elif key in string.ascii_letters:
        app.message += key
        
#function is called every step
def onStep(app):
    #controls animation for fading of textbox at the start
    if not app.starting and app.counter <= 49:
        app.counter += 1
        
    cellWidth, cellHeight = getCellSize(app)
    
    #controls whether the animated square is fading in or out
    if app.animate <= 0 or app.animate >= 60:
        app.up = not app.up
        
    if app.up:
        app.animate += 2.5
    else:
        app.animate -= 2.5
        
    #once a color is selected, animates an increase in size then decrease back to normal
    if app.click == 1:
        if app.size <= cellWidth + 20:
            app.size+=2
        else:
            app.click = 2
    if app.click == 2:
        if app.size >= cellWidth+2:
            app.size-=2
        else:
            app.click = 0
            app.size = cellWidth
            
            #changes player turn
            app.turn = app.player2 if app.turn == app.player1 else app.player1
            
    #if the two players control all of the board, game is over, winner is whoever has the most squares
    if app.player1.score + app.player2.score == 56 and not app.starting:
        app.turn = app.player1 if app.player1.score > app.player2.score else app.player2
        app.over = True
        
#based on x position, determines what color square was selected
def getColor(x):
    if 25 <= x <= 70:
        return 0
    if 86 <= x <= 131:
        return 1
    if 147 <= x <= 192:
        return 2
    if 208 <= x <= 253:
        return 3
    if 269 <= x <= 314:
        return 4
    if 331 <= x <= 376:
        return 5
        
def onMousePress(app,mouseX, mouseY):
    #determines if a color selection square has been clicked
    if 345 <= mouseY <= 390 and not app.over and not app.starting and app.click == 0: #prevents multiple clicks per turn
        app.delay = True
        color = getColor(mouseX)
        
        if color!= None:
            color = app.colors[color]
    
            if color not in app.notPlayable:
                #removes the first color from notPlayable, and appends the new color
                app.notPlayable.pop(0)
                app.notPlayable.append(color)
                
                #searches for all adjacent squares of the same color, and adds them to the player's list
                index = [-1, 1]
                for j in app.turn.squares:
                    row = j[0]
                    col = j[1]
                    app.board[row][col] = color
    
                    for i in index:
                        
                            #try and except are used to prevent index errors
                            try:
                                if app.board[row+i][col] == color and row+i>-1:
                                    if (row+i,col) not in app.turn.squares:
                                        app.turn.addSquares(row+i,col)
                            except:
                                pass
                            try:
                                if app.board[row][col+i] == color and col+i>-1:
                                    if (row,col+i) not in app.turn.squares:
                                        app.turn.addSquares(row,col+i)
                            except:
                                continue
                app.click = 1
                
                        
                        
                        
            
            

def main():
    runApp()

main()