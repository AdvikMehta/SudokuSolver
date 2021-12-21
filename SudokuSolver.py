# imports
import pygame
import os
import sys
from pygame import time

class Grid:
    grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def __init__(self, rows, cols, width, height, screen):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.grid[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.selected = False
        self.screen = screen
        self.model = None
        self.update_model()

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].value = val

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def draw(self, screen):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(screen, (0, 0, 0), (0, int(i * gap)), (self.width, int(i * gap)), thick)
            pygame.draw.line(screen, (0, 0, 0), (int(i * gap), 0), (int(i * gap), self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(screen)

    def solveGUI(self):
        self.update_model()
        find = findEmpty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if isValid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].drawChange(self.screen, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(25)

                if self.solveGUI():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].drawChange(self.screen, False)
                pygame.display.update()
                pygame.time.delay(25)

        return False

    def solve(self):
        self.update_model()
        find = findEmpty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if isValid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0
        return False

class Cube:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, screen):
        font = pygame.font.Font("menufont.ttf", 42)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128, 128, 128))
            screen.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 0))
            screen.blit(text, (int(x + (gap / 2 - text.get_width() / 2)), int(y + (gap / 2 - text.get_height() / 2))))

        if self.selected:
            pygame.draw.rect(screen, (255, 0, 0), (int(x), int(y), int(gap), int(gap), 3))

    def drawChange(self, screen, g=True):
        font = pygame.font.Font("menufont.ttf", 42)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(screen, (255, 255, 255), (int(x), int(y), int(gap), int(gap)))

        text = font.render(str(self.value), 1, (0, 0, 0))
        screen.blit(text, (int(x + (gap / 2 - text.get_width() / 2)), int(y + (gap / 2 - text.get_height() / 2))))
        if g:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(int(x), int(y), int(gap), int(gap), 3))
        else:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(int(x), int(y), int(gap), int(gap), 3))

    def set(self, val):
        self.value = val

def findEmpty(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return i, j
    return None

def isValid(grid, num, pos):
    # Check row
    for i in range(len(grid[0])):
        if grid[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(grid)):
        if grid[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if grid[i][j] == num and (i,j) != pos:
                return False

    return True

def redraw_window(screen, grid):
    screen.fill((255, 255, 255))
    font = pygame.font.Font("menufont.ttf", 22)
    userText = 'Fill the boxes, then press enter to solve the grid'
    textSurface = font.render(userText, True, (0, 0, 0))
    screen.blit(textSurface, (28, 555))
    # Draw grid and board
    grid.draw(screen)

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((543, 600))
    pygame.display.set_caption("Sudoku Solver")
    icon = pygame.image.load("sudoku.png")
    pygame.display.set_icon(icon)

    grid = Grid(9, 9, 540, 540, screen)
    key = None

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_0:
                    key = 0
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
                    grid.solveGUI()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = grid.click(pos)
                if clicked:
                    grid.select(clicked[0], clicked[1])
                    key = None

            if grid.selected and key is not None:
                grid.sketch(key)

        redraw_window(screen, grid)

        pygame.display.update()
        clock.tick(60)

main()
