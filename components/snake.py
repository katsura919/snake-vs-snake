import pygame
from .constants import *

class Snake:
    def __init__(self, start_pos, color, head_color, player_name):
        self.body = [start_pos]
        self.direction = RIGHT
        self.grow = False
        self.color = color
        self.head_color = head_color
        self.player_name = player_name
        self.alive = True
    
    def move(self):
        if not self.alive:
            return
            
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Add new head
        self.body.insert(0, new_head)
        
        # Remove tail unless growing
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction):
        # Prevent snake from going back into itself
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def check_collision(self, other_snake=None):
        if not self.alive:
            return False
            
        head_x, head_y = self.body[0]
        
        # Check wall collision
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            return True
        
        # Check self collision
        if self.body[0] in self.body[1:]:
            return True
        
        # Check collision with other snake
        if other_snake and other_snake.alive:
            if self.body[0] in other_snake.body:
                return True
        
        return False
    
    def eat_food(self):
        self.grow = True
    
    def draw(self, screen):
        if not self.alive:
            return
            
        for i, segment in enumerate(self.body):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE
            
            if i == 0:  # Head
                pygame.draw.rect(screen, self.head_color, (x, y, GRID_SIZE, GRID_SIZE))
                # Draw eyes
                pygame.draw.circle(screen, WHITE, (x + 5, y + 5), 2)
                pygame.draw.circle(screen, WHITE, (x + 15, y + 5), 2)
            else:  # Body
                pygame.draw.rect(screen, self.color, (x, y, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, self.head_color, (x, y, GRID_SIZE, GRID_SIZE), 1)