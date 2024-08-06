import pygame
import sys
import random

pygame.init()
pygame.font.init()

screen_width = 540
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Sudoku')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
LIGHT_GREY = (200, 200, 200)
LIGHT_ORANGE = (255, 165, 0)

FONT = pygame.font.Font(None, 40)
BUTTON_FONT = pygame.font.Font(None, 50)


class SudokuGenerator:
    def __init__(self, removed_cells, row_length=9):
        self.removed_cells = removed_cells
        self.row_length = row_length
        self.board = [[0] * row_length for _ in range(row_length)]
        self.box_length = 3

    def get_board(self):
        return [row[:] for row in self.board]

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) if num != 0 else '-' for num in row))
        print()

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return num not in [self.board[row][col] for row in range(self.row_length)]

    def valid_in_box(self, row_start, col_start, num):
        rows = (row_start // 3) * 3
        cols = (col_start // 3) * 3
        for r in range(rows, rows + 3):
            for c in range(cols, cols + 3):
                if num == self.board[r][c]:
                    return False
        return True

    def is_valid(self, row, col, num):
        return (
                self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(row, col, num)
        )

    def fill_box(self, row_start, col_start):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(self.box_length):
            for j in range(self.box_length):
                self.board[row_start + i][col_start + j] = nums.pop()

    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)

    def fill_remaining(self, row, col):
        if col >= self.row_length and row < self.row_length - 1:
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True

        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == (row // self.box_length) * self.box_length:
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def remove_cells(self):
        cells_to_remove = self.removed_cells
        while cells_to_remove > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_to_remove -= 1

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, 0)
        self.remove_cells()


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
    def __init__(self, screen, difficulty):
        self.screen = screen
        self.difficulty = difficulty
        self.board = self.generate_board()
        self.cells = [[Cell(self.board[i][j], i, j, screen) for j in range(9)] for i in range(9)]
        self.selected_cell = None
        self.original_board = [row[:] for row in self.board]

    def generate_board(self):
        generator = SudokuGenerator(removed_cells=self.get_removed_cells())
        generator.fill_values()
        return generator.get_board()

    def get_removed_cells(self):
        if self.difficulty == "easy":
            return 20
        elif self.difficulty == "medium":
            return 40
        elif self.difficulty == "hard":
            return 60
        return 20

    def is_valid(self, row, col, num):
        generator = SudokuGenerator(removed_cells=0)  # Create a temporary generator for validation
        return generator.is_valid(row, col, num)

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
                cell.selected = False
        self.cells[row][col].selected = True

    def click(self, x, y):
        if 0 <= x <= 540 and 0 <= y <= 540:
            row = y // 60
            col = x // 60
            return row, col
        return None

    def clear(self):
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].set_cell_value(0)
            self.cells[row][col].set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.is_valid(row, col, value):  # Check if the number is valid
                self.cells[row][col].set_cell_value(value)
                self.board[row][col] = value
                if self.is_full():
                    return True
            else:
                print("Invalid number placement!")
        return False

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def check_board(self):
        return self.is_valid()

    def reset_to_original(self):
        self.board = [[self.original_board[i][j] for j in range(9)] for i in range(9)]
        self.cells = [[Cell(self.board[i][j], i, j, self.screen) for j in range(9)] for i in range(9)]


class Board:
    def __init__(self, screen, difficulty):
        self.screen = screen
        self.difficulty = difficulty
        self.board = self.generate_board()
        self.cells = [[Cell(self.board[i][j], i, j, screen) for j in range(9)] for i in range(9)]
        self.selected_cell = None
        self.original_board = [row[:] for row in self.board]

    def generate_board(self):
        generator = SudokuGenerator(removed_cells=self.get_removed_cells())
        generator.fill_values()
        return generator.get_board()

    def get_removed_cells(self):
        if self.difficulty == "easy":
            return 20
        elif self.difficulty == "medium":
            return 40
        elif self.difficulty == "hard":
            return 60
        return 20

    def is_valid(self, row, col, num):
        generator = SudokuGenerator(removed_cells=0)  # Create a temporary generator for validation
        return generator.is_valid(row, col, num)

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
                cell.selected = False
        self.cells[row][col].selected = True

    def click(self, x, y):
        if 0 <= x <= 540 and 0 <= y <= 540:
            row = y // 60
            col = x // 60
            return row, col
        return None

    def clear(self):
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].set_cell_value(0)
            self.cells[row][col].set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.is_valid(row, col, value):  # Check if the number is valid
                self.cells[row][col].set_cell_value(value)
                self.board[row][col] = value
                if self.is_full():
                    return True
            else:
                print("Invalid number placement!")
        return False

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def check_board(self):
        return self.is_valid()

    def reset_to_original(self):
        self.board = [[self.original_board[i][j] for j in range(9)] for i in range(9)]
        self.cells = [[Cell(self.board[i][j], i, j, self.screen) for j in range(9)] for i in range(9)]


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.text_surf = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def game_start_screen():
    title_font = pygame.font.Font(None, 60)
    info_font = pygame.font.Font(None, 30)

    title_color = (50, 50, 50)
    info_color = (70, 70, 70)
    button_border_color = (0, 0, 0)

    title_text = title_font.render("Welcome to Sudoku!", True, BLACK)
    info_text = info_font.render("Click on a difficulty level to start!", True, BLACK)
    reset_info_text = info_font.render("Press 'r' to reset the game and 'e' to exit", True, BLACK)

    title_text_rect = title_text.get_rect(center=(screen_width // 2, 75))
    info_text_rect = info_text.get_rect(center=(screen_width // 2, 150))
    reset_info_text_rect = reset_info_text.get_rect(center=(screen_width // 2, screen_height - 30))

    easy_button = Button(170, 200, 200, 50, "Easy", GREEN, LIGHT_GREY)
    medium_button = Button(170, 300, 200, 50, "Medium", BLUE, LIGHT_GREY)
    hard_button = Button(170, 400, 200, 50, "Hard", RED, LIGHT_GREY)

    screen.fill(WHITE)

    pygame.draw.rect(screen, LIGHT_ORANGE, (0, 0, screen_width, 120))
    pygame.draw.rect(screen, LIGHT_ORANGE, (0, screen_height - 60, screen_width, 60))

    for button in [easy_button, medium_button, hard_button]:
        pygame.draw.rect(screen, button_border_color, button.rect, 3)

    screen.blit(title_text, title_text_rect)
    screen.blit(info_text, info_text_rect)

    easy_button.draw(screen)
    medium_button.draw(screen)
    hard_button.draw(screen)

    screen.blit(reset_info_text, reset_info_text_rect)

    running = True
    difficulty = None

    easy_button = Button(170, 200, 200, 50, "Easy", GREEN, LIGHT_GREY)
    medium_button = Button(170, 300, 200, 50, "Medium", BLUE, LIGHT_GREY)
    hard_button = Button(170, 400, 200, 50, "Hard", RED, LIGHT_GREY)

    running = True
    difficulty = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
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
    pygame.init()
    screen = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")

    game_state = "start"
    difficulty = None
    board = None

    while True:
        screen.fill(WHITE)

        if game_state == "start":
            difficulty = game_start_screen()
            game_state = "in_progress"

        elif game_state == "in_progress":
            if not board:
                board = Board(screen, difficulty)
            board.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked = board.click(pos[0], pos[1])
                    if clicked:
                        board.select(clicked[0], clicked[1])
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        board.sketch(event.key - pygame.K_0)
                    if event.key == pygame.K_RETURN:
                        if board.selected_cell:
                            row, col = board.selected_cell
                            cell = board.cells[row][col]
                            value = cell.sketched_value
                            if value != 0:
                                if board.place_number(value):
                                    game_state = "game_over"
                    if event.key == pygame.K_r:
                        board.reset_to_original()
                    if event.key == pygame.K_e:
                        pygame.quit()
                        sys.exit()

        elif game_state == "game_over":
            title_font = pygame.font.Font(None, 60)
            info_font = pygame.font.Font(None, 30)

            title_color = (50, 50, 50)
            info_color = (70, 70, 70)
            button_border_color = (0, 0, 0)


            screen.fill(WHITE)

            pygame.draw.rect(screen, LIGHT_ORANGE, (0, 0, screen_width, 120))
            pygame.draw.rect(screen, LIGHT_ORANGE, (0, screen_height - 60, screen_width, 60))

            font = pygame.font.Font(None, 74)
            text = font.render("You Win!", True, BLACK)
            screen.blit(text, (150, 250))
            pygame.display.update()
            pygame.time.wait(2000)  # Displays game over message for 2 seconds
            game_state = "start"  # Resets game

        pygame.display.update()



if __name__ == "__main__":
    main()