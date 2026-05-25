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