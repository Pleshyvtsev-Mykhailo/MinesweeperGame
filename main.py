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