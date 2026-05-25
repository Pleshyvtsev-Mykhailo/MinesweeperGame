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