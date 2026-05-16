
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cmu_graphics_installer (1)', 'cmu_graphics_installer'))

from cmu_graphics import *
import random 
import copy
'''
    Features list & grading short cuts:
    - decision making logic in computerMove() starting from line 152
    - simulating the board before making a move starting from line 11
    - high score being recorded starting from line 127 
    - changing screens line 244
    - changing difficulty 244
    
    
'''
def simulateDrop(grid, col, piece):
    newGrid = copy.deepcopy(grid)
    for row in range(len(newGrid)-1, -1, -1):
        if newGrid[row][col] == 0:
            newGrid[row][col] = piece
            return newGrid
    return None



def checkWinOnSimulation(grid, piece):
    rows = len(grid)
    cols = len(grid[0])
    
    #horizontal 
    for r in range(rows):
        for c in range(cols - 3):
            if (grid[r][c] == piece and grid[r][c+1] == piece and grid[r][c+2] == piece and grid[r][c+3] == piece):
                return True
    # vertical 
    for c in range(cols):
        for r in range(rows - 3):
            if (grid[r][c] == piece and grid[r+1][c] == piece and grid[r+2][c] == piece and grid[r+3][c] == piece):
                return True
    #/
    for r in range(3, rows):
        for c in range(cols - 3):
            if (grid[r][c] == piece and grid[r-1][c+1] == piece and grid[r-2][c+2] == piece and grid[r-3][c+3] == piece):
                return True
    # \ 
    for r in range(Board.rows -3):
        for c in range(Board.cols - 3):
            if (grid[r][c] == piece and grid[r+1][c+1] == piece and grid[r+2][c+2] == piece and grid[r+3][c+3] == piece):
                return True 
            
        
    return False
def countStreak(grid, col, piece):
    newGrid = simulateDrop(grid, col, piece)
    if not newGrid:
        return 0 
    rows = len(newGrid)
    cols = len(newGrid[0])
    r = None
    for row in range(rows):
        if newGrid[row][col] != 0:
            r = row
            break     
    maxCount = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        # check forward
        nr, nc = r + dr, col +dc
        while 0 <= nr < rows and 0<=nc<cols and newGrid[nr][nc] == piece:
            count += 1
            nr += dr
            nc += dc
        #back 
        nr, nc = r - dr, col - dc
        while 0<=nr<rows and 0<=nc<cols and newGrid[nr][nc] == piece:
            count += 1
            nr -= dr
            nc -= dc
        maxCount = max(maxCount, count)
    return maxCount 
    
        
        

class Board:
    rows = 6
    cols = 8 
    
    def __init__(self):
        self.grid = [[0 for _ in range(Board.cols)] for _ in range(Board.rows)]
    def dropPiece(self, col, piece):
        for row in range(Board.rows-1, -1, -1):
            if self.grid[row][col] == 0:
                self.grid[row][col] = piece
                return True
        return False
    def getValidColumns(self):
        return [c for c in range(Board.cols) if self.grid[0][c] == 0]
    
    def checkWin(self, piece):
        #Horizontal Streak
        for r in range(Board.rows):
            for c in range(Board.cols - 3):
                if (self.grid[r][c] == piece) and (self.grid[r][c+1] == piece) and (self.grid[r][c+2] == piece) and (self.grid[r][c+3] == piece):
                    return True 
        #vertical
        for c in range(Board.cols):
            for r in range(Board.rows - 3):
                if (self.grid[r][c] == piece) and (self.grid[r+1][c] == piece) and (self.grid[r+2][c] == piece) and (self.grid[r+3][c] == piece):
                    return True
        #diagonal /
        for r in range(3, Board.rows):
            for c in range(Board.cols - 3):
                if (self.grid[r][c] == piece) and (self.grid[r-1][c+1] == piece) and (self.grid[r-2][c+2] == piece) and (self.grid[r-3][c+3] == piece):
                    return True 
        #diagonal \
        for r in range(Board.rows-3):
            for c in range(Board.cols-3):
                if (self.grid[r][c] == piece) and (self.grid[r+1][c+1] == piece) and (self.grid[r+2][c+2] == piece) and (self.grid[r+3][c+3] == piece):
                    return True
    
class Game:
    def __init__(self, app, difficulty):
        self.app = app
        self.board = Board()
        self.currentPlayer = 1
        self.gameOver = False
        self.winner = None
        self.difficulty = difficulty # easy or hard
        
        
    def updateScore(self, winner):
        if winner == 1:
            self.app.score += 1
            self.app.highScore = max(self.app.score, self.app.highScore)
        
        
    def playerMove(self, col):
        if self.gameOver:
            return 
        if self.currentPlayer == 1:
            if self.board.dropPiece(col, 1): 
                if self.board.checkWin(1):
                    self.gameOver = True 
                    self.winner = 1
                    self.updateScore(1)
                else:
                    self.currentPlayer = 2
                    self.computerMove()
                    
                    
    def computerMove(self):
        if self.gameOver:
            return 
        
        valid = self.board.getValidColumns()
        if not valid:
            self.gameOver = True 
            return 
        #Logic incoporated 
        if self.difficulty == 'hard':
            for col in valid:
                newGrid = simulateDrop(self.board.grid, col, 2) 
                if newGrid != None and checkWinOnSimulation(newGrid, 2):
                    self.board.dropPiece(col, 2)
                    self.gameOver = True 
                    self.winner = 2
                    self.updateScore(2)
                    return 
                

        # try to block player from winning
        if self.difficulty == 'hard':
            for col in valid:
                newGrid = simulateDrop(self.board.grid, col, 1) 
                if newGrid != None and checkWinOnSimulation(newGrid, 1):
                    self.board.dropPiece(col, 2)
                    self.currentPlayer = 1
                    return 
                
        # block potential 3-row streak 
        if self.difficulty == 'hard':
            threatCols = []
            for col in valid:
                if countStreak(self.board.grid, col, 1) >= 3:
                    threatCols.append(col)
                if threatCols:
                    self.board.dropPiece(threatCols[0], 2)
                    self.currentPlayer = 1
                    return 
        
        
        # centermost column
        if self.difficulty == 'hard':
            center = Board.cols //2 
            bestCol = valid[0]
            
            for c in valid:
                if abs(c - center) < abs(bestCol - center):
                    bestCol = c
            self.board.dropPiece(bestCol, 2)
            if self.board.checkWin(2):
                self.gameOver = True 
                self.winner = 2
                self.updateScore(2)
            self.currentPlayer = 1
            
            
        if self.difficulty == 'easy':
            index = random.randint(0, len(valid) - 1)
            col = valid[index]
            self.board.dropPiece(col, 2)
            if self.board.checkWin(2):
                self.gameOver = True 
                self.winner = 2
            self.currentPlayer = 1
            
            
       
        
    def reset(self):
        self.board = Board()
        self.currentPlayer = 1
        self.gameOver = False
        self.winner = None

def onAppStart(app):
    app.width = 500
    app.height = 500
    app.padding = 30
    app.cellSize = 50
    app.rows = 6
    app.cols = 8
    app.game = Game(app, 'easy')
    app.score = 0 
    app.highScore = 0
    

def start_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = 'black')
    drawLabel('CONNECT 4', app.width//2, app.height//2 - 50, size = 70, bold = True, fill = 'midnightBlue', borderWidth = 2, border = 'white')
    drawLabel(f'High Score {app.highScore}', app.width//2, app.height//2 + 20, size = 40, fill = 'white')
    drawLabel('Press \'e\' for easy or \'d\' for difficult', app.width//2, app.height//2 + 80, size = 30, fill = 'white')
    
    
    
def start_onKeyPress(app, key):
    if key == 'e':
        app.game = Game(app, 'easy')
        setActiveScreen('game')
    elif key == 'd':
        app.game = Game(app, 'hard')
        setActiveScreen('game')



def game_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = 'black')
    drawRect(50, 50, 400, 375, fill = 'midnightBlue', border = 'navy')
    drawLabel('CONNECT 4', app.width//2, 465, size = 70, bold = True, fill = 'midnightBlue', borderWidth = 2, border = 'white')
    #drawRect(60, 375, 100, 35, fill = 'black', border = 'white')
    drawLabel('Click \'r\' to reset', app.width//2, 370, fill = 'white', size = 25)
    drawLabel('Click \'s\' to check score', app.width//2, 395, fill = 'white', size = 25)
    #drawLabel('Reset',110, 390, size = 20, fill = 'white', bold = True)

    for r in range(app.rows):
        for c in range(app.cols):
            x = app.padding + c * app.cellSize 
            y = app.padding + r * app.cellSize
            drawCircle(x + 45, y + 45, app.cellSize/2 -5, fill = 'white')
    for r in range(app.rows):
        for c in range(app.cols):
            piece = app.game.board.grid[r][c]
            if piece == 1:
                color = 'red'
            elif piece == 2:
                color = 'gold'
            elif piece == 0:
                continue 
            x = app.padding + c * app.cellSize 
            y = app.padding + r * app.cellSize
            drawCircle(x + 45, y + 45, app.cellSize/2 -5, fill = color, border = 'black', borderWidth = 2)

    if app.game.gameOver:
        winner = 'Player' if app.game.winner == 1 else 'Computer'
        color = 'red' if app.game.winner == 1 else 'gold'
    
        drawLabel(f'{winner} wins!', app.width//2, app.height//2, size = 60, bold = True, fill = color, border = 'black')

def game_onMousePress(app, mouseX, mouseY):
    if app.game.gameOver:
        return 
    col = (mouseX - 50) // app.cellSize
    if 0 <= col < app.cols:
       app.game.playerMove(col)
        
def game_onKeyPress(app, keys):
    if 'r' in keys:
        app.game.reset()
    if 's' in keys:
        setActiveScreen('start')

def main():

    runAppWithScreens(initialScreen = 'start')
main()
### Your code goes here; if it contains a call to
### runApp(), use the "CPCS Mode" starter code instead.
cmu_graphics.run()
