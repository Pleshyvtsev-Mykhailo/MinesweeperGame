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
