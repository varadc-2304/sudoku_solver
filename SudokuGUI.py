from sudokutools import valid, find_empty
from sys import exit
import pygame

pygame.init()

class Board:
    def __init__(self, window):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solvedBoard = None  # Solved board will be generated after input
        self.tiles = [
            [Tile(self.board[i][j], window, i * 60, j * 60) for j in range(9)]
            for i in range(9)
        ]
        self.window = window

    def draw_board(self):
        for i in range(9):
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    pygame.draw.line(
                        self.window,
                        (0, 0, 0),
                        (j // 3 * 180, 0),
                        (j // 3 * 180, 540),
                        4,
                    )
                if i % 3 == 0 and i != 0:
                    pygame.draw.line(
                        self.window,
                        (0, 0, 0),
                        (0, i // 3 * 180),
                        (540, i // 3 * 180),
                        4,
                    )
                self.tiles[i][j].draw((0, 0, 0), 1)
                if self.tiles[i][j].value != 0:
                    self.tiles[i][j].display(
                        self.tiles[i][j].value, (21 + j * 60, 16 + i * 60), (0, 0, 0)
                    )
        pygame.draw.line(
            self.window,
            (0, 0, 0),
            (0, (i + 1) // 3 * 180),
            (540, (i + 1) // 3 * 180),
            4,
        )

    def deselect(self, tile):
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j] != tile:
                    self.tiles[i][j].selected = False

    def redraw(self, keys):
        self.window.fill((255, 255, 255))
        self.draw_board()
        for i in range(9):
            for j in range(9):
                if self.tiles[j][i].selected:
                    self.tiles[j][i].draw((50, 205, 50), 4)
        pygame.display.flip()

    def visualSolve(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        empty = find_empty(self.board)
        if not empty:
            return True
        for nums in range(9):
            if valid(self.board, (empty[0], empty[1]), nums + 1):
                self.board[empty[0]][empty[1]] = nums + 1
                self.tiles[empty[0]][empty[1]].value = nums + 1
                pygame.time.delay(63)
                self.redraw({})
                if self.visualSolve():
                    return True
                self.board[empty[0]][empty[1]] = 0
                self.tiles[empty[0]][empty[1]].value = 0
                pygame.time.delay(63)
                self.redraw({})
        return False

class Tile:
    def __init__(self, value, window, x1, y1):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x1, y1, 60, 60)
        self.selected = False

    def draw(self, color, thickness):
        pygame.draw.rect(self.window, color, self.rect, thickness)

    def display(self, value, position, color):
        font = pygame.font.SysFont("lato", 45)
        text = font.render(str(value), True, color)
        self.window.blit(text, position)

def main():
    screen = pygame.display.set_mode((540, 590))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Sudoku Solver")

    font = pygame.font.SysFont("Bahnschrift", 40)
    text = font.render("Input Puzzle", True, (0, 0, 0))
    screen.blit(text, (175, 245))
    pygame.display.flip()

    board = Board(screen)
    selected = (-1, -1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].selected = False
                    board.visualSolve()
                elif selected != (-1, -1):
                    row, col = selected
                    if event.key == pygame.K_BACKSPACE:
                        board.tiles[row][col].value = 0
                        board.board[row][col] = 0
                    elif event.unicode.isdigit() and int(event.unicode) != 0:
                        num = int(event.unicode)
                        board.tiles[row][col].value = num
                        board.board[row][col] = num
                    selected = (-1, -1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // 60, pos[0] // 60
                selected = (row, col)
                
        board.redraw({})

main()
pygame.quit()
