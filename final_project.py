import pygame
import sys

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Sudoku")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

FONT = pygame.font.Font(None, 40)
BUTTON_FONT = pygame.font.Font(None, 50)

class Button:
    def __int__(self, text, x, y, width, height, color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = BUTTON_FONT.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center = self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        x = self.col * 60
        y = self.row * 60
        if self.selected:
            pygame.draw.rect(self.screen, RED, (x, y, 60, 60), 3)
        else:
            pygame.draw.rect(self.screen, BLACK, (x, y, 60, 60), 1)
        if self.value != 0:
            text = FONT.render(str(self.value), True, BLACK)
            self.screen.blit(text, (x + 20, y + 10))
        elif self.sketched_value != 0:
            text = FONT.render(str(self.sketched_value), True, GREY)
            self.screen.blit(text, (x + 5, y + 5))

class Board:
    def __init__(self,screen, board):
        self.screen = screen
        self.board = board
        self.cells = [[Cell(self.board[i][j], i ,j, screen) for j in range(9)] for i in range(9)]
        self.selected_cell = None

    def draw(self):
        for i in range(10):
            line_width = 1 if i % 3 != 0 else 3
            pygame.draw.line(self.screen, BLACK, (0, i * 60), (540, i * 60), line_width)
            pygame.draw.line(self.screen, BLACK, (i * 60, 0), (i * 60, 540), line_width)
        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        self.selected_cell = (row, col)
        for row_cells in self.cells:
            for cell in row_cells:
                cell.slected = False
        self.cells[row][col].selected = True

    def click(self, x, y):
        if x <= x <= 540 and 0 <= y <= 540:
            row = y//60
            col = x//60
            return row, col
        return None

    def clear(self):
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].set_cell_value(0)
            self.cells[row][col].set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell:
            row,col = self.selected_cell
            self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].set_cell_value(value)

def game_start_screen():
    easy_button = Button("Easy", 200, 200, 200, 50, GREEN)
    medium_button = Button("Medium", 200, 300, 200, 50, BLUE)
    hard_button = Button("Hard", 200, 400, 200, 50, RED)

    running = True
    difficulty = None

    while running:
        screen.fill(WHITE)
        easy_button.draw(screen)
        medium_button.draw(screen)
        hard_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if easy_button.is_clicked(pos):
                    difficulty = "easy"
                    running = False
                elif medium_button.is_clicked(pos):
                    difficulty = "medium"
                    running = False
                elif hard_button.is_clicked(pos):
                    difficulty = "hard"
                    running = False

        pygame.display.update()

    return difficulty

def main():
    difficulty = game_start_screen()
    if difficulty:
        board = [[0 for _ in range(9)] for _ in range(9)] #Placeholder: Replace with Demetrio=s board logic
        sudoku_board = Board(screen, board)
        running = True
        key = None

        while running:
            screen.fill(WHITE)
            sudoku_board.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked = sudoku_board.click(pos[0], pos[1])
                    if clicked:
                        sudoku_board.select(clicked[0], clicked[1])
                        key = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        key = 1
                    elif event.key == pygame.K_2:
                        key = 2
                    elif event.key == pygame.K_3:
                        key = 3
                    elif event.key == pygame.K_4:
                        key = 4
                    elif event.key == pygame.K_5:
                        key = 5
                    elif event.key == pygame.K_6:
                        key = 6
                    elif event.key == pygame.K_7:
                        key = 7
                    elif event.key == pygame.K_8:
                        key = 8
                    elif event.key == pygame.K_9:
                        key = 9
                    elif event.key == pygame.K_RETURN:
                        if sudoku_board.selected_cell and key:
                            sudoku_board.place_number(key)
                            key = None
            if sudoku_board.selected_cell and key:
                sudoku_board.sketch(key)

            pygame.display.update()

    else:
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    main()


