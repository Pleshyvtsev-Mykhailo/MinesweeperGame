CELL_SIZE = 40
MARGIN = 5
COLOR_HIDDEN = (192, 192, 192)
COLOR_REVEALED = (220, 220, 220)
COLOR_MINE = (255, 0, 0)
COLOR_FLAG = (0, 0, 255)
COLOR_TEXT = (0, 0, 0)
COLOR_BG = (128, 128, 128)

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
