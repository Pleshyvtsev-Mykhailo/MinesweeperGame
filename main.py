import pygame
import random
import argparse
import sys

CELL_SIZE = 40
MARGIN = 5
COLOR_HIDDEN = (192, 192, 192)
COLOR_REVEALED = (220, 220, 220)
COLOR_MINE = (255, 0, 0)
COLOR_FLAG = (0, 0, 255)
COLOR_TEXT = (0, 0, 0)
COLOR_BG = (128, 128, 128)


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0

    def toggle_flag(self):
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged

    def reveal(self):
        if self.is_flagged or self.is_revealed:
            return True
        self.is_revealed = True
        return not self.is_mine


class Board:
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.grid = [[Cell(x, y) for x in range(cols)] for y in range(rows)]
        self.mines_generated = False

    def generate_mines(self, first_click_x, first_click_y):
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)

            if not self.grid[y][x].is_mine and (x != first_click_x or y != first_click_y):
                self.grid[y][x].is_mine = True
                mines_placed += 1
        self.calculate_neighbors()
        self.mines_generated = True

    def calculate_neighbors(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x].is_mine:
                    continue
                count = 0
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.cols and 0 <= ny < self.rows:
                        if self.grid[ny][nx].is_mine:
                            count += 1
                self.grid[y][x].neighbor_mines = count

    def reveal_cell(self, x, y):
        if not (0 <= x < self.cols and 0 <= y < self.rows):
            return
        cell = self.grid[y][x]

        if cell.is_revealed or cell.is_flagged:
            return

        cell.reveal()

        if cell.neighbor_mines == 0 and not cell.is_mine:
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dx, dy in directions:
                self.reveal_cell(x + dx, y + dy)

    def check_win(self):
        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.grid[y][x]
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True


class MinesweeperGame:
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = Board(rows, cols, num_mines)

        pygame.init()
        self.width = cols * (CELL_SIZE + MARGIN) + MARGIN
        self.height = rows * (CELL_SIZE + MARGIN) + MARGIN
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minesweeper CI/CD")
        self.font = pygame.font.SysFont(None, 30)

        self.is_game_over = False
        self.is_win = False

    def draw(self):
        self.screen.fill(COLOR_BG)
        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.board.grid[y][x]
                rect = pygame.Rect(
                    MARGIN + x * (CELL_SIZE + MARGIN),
                    MARGIN + y * (CELL_SIZE + MARGIN),
                    CELL_SIZE, CELL_SIZE
                )

                if cell.is_revealed:
                    pygame.draw.rect(self.screen, COLOR_REVEALED, rect)
                    if cell.is_mine:
                        pygame.draw.circle(self.screen, COLOR_MINE, rect.center, CELL_SIZE // 3)
                    elif cell.neighbor_mines > 0:
                        text = self.font.render(str(cell.neighbor_mines), True, COLOR_TEXT)
                        text_rect = text.get_rect(center=rect.center)
                        self.screen.blit(text, text_rect)

                else:
                    pygame.draw.rect(self.screen, COLOR_HIDDEN, rect)
                    if cell.is_flagged:
                        pygame.draw.circle(self.screen, COLOR_FLAG, rect.center, CELL_SIZE // 4)

        if self.is_game_over:
            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            overlay.set_alpha(100)
            if self.is_win:
                overlay.fill((34, 139, 34))
                msg = "VICTORY!"
            else:
                overlay.fill((139, 0, 0))
                msg = "GAME OVER!"

            self.screen.blit(overlay, (0, 0))

            final_font = pygame.font.SysFont('Arial', 36, bold=True)
            text_surface = final_font.render(msg, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not self.is_game_over:
                x, y = event.pos
                grid_x = x // (CELL_SIZE + MARGIN)
                grid_y = y // (CELL_SIZE + MARGIN)

                if 0 <= grid_x < self.cols and 0 <= grid_y < self.rows:
                    if event.button == 1:
                        if not self.board.mines_generated:
                            self.board.generate_mines(grid_x, grid_y)

                        if not self.board.grid[grid_y][grid_x].is_flagged:
                            if self.board.grid[grid_y][grid_x].is_mine:
                                self.is_game_over = True

                                for row in self.board.grid:
                                    for c in row:
                                        if c.is_mine:
                                            c.is_revealed = True
                            else:
                                self.board.reveal_cell(grid_x, grid_y)
                                if self.board.check_win():
                                    self.is_game_over = True
                                    self.is_win = True

                    elif event.button == 3:
                        self.board.grid[grid_y][grid_x].toggle_flag()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.draw()

            if self.is_game_over:
                if self.is_win:
                    pygame.display.set_caption("Minesweeper - ПЕРЕМОГА!")
                else:
                    pygame.display.set_caption("Minesweeper - ПРОГРАШ!")

            clock.tick(30)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Гра Сапер на Pygame")
    parser.add_argument('--rows', type=int, default=10, help='Кількість рядків')
    parser.add_argument('--cols', type=int, default=10, help='Кількість стовпців')
    parser.add_argument('--mines', type=int, default=15, help='Кількість мін')

    args = parser.parse_args()

    if args.mines >= args.rows * args.cols:
        print("Помилка: кількість мін не може бути більшою або рівною кількості клітинок!")
        sys.exit(1)

    game = MinesweeperGame(args.rows, args.cols, args.mines)
    game.run()
