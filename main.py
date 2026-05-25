import pygame
import random
import argparse
import sys

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
