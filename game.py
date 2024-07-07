import pygame as pg
import random
import sys
import math

class Game2048(object):
    def __init__(self, ai, size=4):
        self.ai = ai
        self.size = size
        self.board = self.initBoard()
        self.generateNewNumber(2)
        self.colours = self.initColours()
        self.score = 0
        self.gameover = False

    def __str__(self):
        board = [f"{self.board[i]}" for i in range(self.size)]
        return "\n".join(board)

    def move(self, direction):
        def noRotation(board):
            return [[board[i][j] for j in range(self.size)] for i in range(self.size)]
        def rotateLeft(board):
            return [[board[j][i] for j in range(self.size)] for i in range(self.size)[::-1]]
        def rotateRight(board):
            return [[board[j][i] for j in range(self.size)[::-1]] for i in range(self.size)]
        def flip(board):
            return [[board[i][j] for j in range(self.size)[::-1]] for i in range(self.size)[::-1]]

        before = {"r" : flip,
                  "u" : rotateLeft,
                  "d" : rotateRight,
                  "l" : noRotation}
        after = {"r" : flip,
                 "u" : rotateRight,
                 "d" : rotateLeft,
                 "l" : noRotation}

        newBoard = before[direction](self.board)
        #Now all of them should be heading left
        possibleMoves = [(i, j) for i in range(self.size) for j in range(1, self.size)]
        affected = list()
        for i, j in possibleMoves:
            n = newBoard[i][j]
            m = newBoard[i][j - 1]
            if m == 0 or (m == n and (i, j) not in affected):
                newBoard[i][j] = 0
                newBoard[i][j - 1] = n + m
                if m == n:
                    self.score += n * 2
                    affected.append((i, j))
            if m == 0 and j - 1 != 0:
                possibleMoves.append((i, j - 1))
        
        newBoard = after[direction](newBoard)
        if newBoard != self.board:
            self.board = newBoard
            self.generateNewNumber()
        else:
            self.ai.aiDidBadMove(self.score)
    def initColours(self):
        r = [201,235,234,226,223,191,215,228,228,228,228,228]
        g = [194,229,226,182,156,34,105,208,208,208,208,208]
        b =[180,218,201,123,101,10,63,98,98,98,98,98]
        return [(r[i], g[i], b[i]) for i in range(len(r))]

    def initBoard(self):
        board = [[0] * self.size for i in range(self.size)]
        return board

    def generateNewNumber(self, times=1):
        empty = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == 0]
        if len(empty) == 0:
            self.gameover = True
        for time in range(times):
            choice = empty.pop(random.randint(0, len(empty) - 1))
            n = random.randint(0, 9)
            i, j = choice
            self.board[i][j] = 4 if n == 0 else 2

    def updateSurfaces(self, x, y, font):
        surfaces = []
        boxsize = x
        surfaces.append((pg.Surface((boxsize, boxsize)), (0, y - boxsize), (183,174,160)))

        surfaces.append((pg.Surface((x / 4, x / 10)), (x / 2, x / 10), self.colours[0]))
        scorefont = pg.font.Font(None, 20)
        scoreText = scorefont.render(f"{self.score}", True, "white")
        scoreRect = scoreText.get_rect(center=(x * 5 / 8, x * 3 / 20))
        surfaces.append((scoreText, scoreRect, None))

        smallerbox = boxsize / (self.size + 1)
        outlineSize = smallerbox / (self.size + 1)
        for i in range(self.size):
            for j in range(self.size):
                n = self.board[j][i]
                m = 0 if n == 0 else int(math.log2(self.board[j][i]))
                box = pg.Surface((smallerbox, smallerbox))
                boxRect = ((smallerbox * i) + (outlineSize * (i + 1)), y - boxsize + (smallerbox * j) + (outlineSize * (j + 1)))
                boxColour = self.colours[m]
                surfaces.append((box, boxRect, boxColour))
                if n != 0:
                    text = font.render(f"{n}", True, "black")
                    textRect = text.get_rect(center=((smallerbox * i) + (outlineSize * (i + 1)) + (smallerbox / 2), y - boxsize + (smallerbox * j) + (outlineSize * (j + 1)) + (smallerbox / 2)))
                    surfaces.append((text, textRect, None))
        return surfaces

    def startGame(self, framerate=60):
        pg.init()
        x = 360
        y = 640
        font = pg.font.Font(None, 45)
        screen = pg.display.set_mode((x, y))
        clock = pg.time.Clock()
        surfaces = self.updateSurfaces(x, y, font)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    key = event.key
                    direction = "u" if pg.K_w == key else "l" if pg.K_a == key else "d" if pg.K_s == key else "r" if pg.K_d == key else None
                    if direction != None:
                        self.move(direction)
             
            screen.fill("white")
            newx, newy = pg.display.get_window_size()
            if x != newx or y != newy:
                x , y = newx, newy
                ratiox = 9
                ratioy = 16
                ratio = ratiox/ratioy
                if x/y > ratio:
                    fy = y // ratioy
                    x = fy * ratiox
                    y = fy * ratioy
                font = pg.font.Font(None, x // 8)
                screen = pg.display.set_mode((x, y))
            surfaces = self.updateSurfaces(x, y, font)

            # RENDER YOUR GAME HERE
            for surfaceInfo in surfaces:
                surface, offset, colour = surfaceInfo
                if colour != None:
                    surface.fill(colour)
                screen.blit(surface, offset)

            self.move(self.ai.chooseDirection(self.board))

            pg.display.flip()

            clock.tick(framerate)  # limits FPS to Number Set
        pg.quit()