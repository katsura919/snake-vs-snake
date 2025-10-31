import pygame
import random
from .constants import *

class Food:
    def __init__(self):
        self.position = self.generate_position()
    
    def generate_position(self):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return (x, y)
    
    def respawn(self, snake1_body, snake2_body=None):
        while True:
            self.position = self.generate_position()
            if snake2_body is None:
                # Single player mode
                if self.position not in snake1_body:
                    break
            else:
                # Two player mode
                if (self.position not in snake1_body and 
                    self.position not in snake2_body):
                    break
    
    def draw(self, screen):
        x = self.position[0] * GRID_SIZE
        y = self.position[1] * GRID_SIZE
        pygame.draw.rect(screen, RED, (x, y, GRID_SIZE, GRID_SIZE))
        # Add a small highlight to make it look like an apple
        pygame.draw.rect(screen, (255, 100, 100), (x + 2, y + 2, GRID_SIZE - 4, GRID_SIZE - 4))