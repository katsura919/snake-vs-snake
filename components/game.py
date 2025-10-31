import pygame
import sys
import time
from .constants import *
from .snake import Snake
from .food import Food

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        
        # Game state management
        self.state = MENU
        self.game_mode = None
        self.selected_option = 0  # For menu navigation
        
        # Initialize game objects (will be set up when game starts)
        self.snake1 = None
        self.snake2 = None
        self.food = None
        
        # Game variables
        self.score1 = 0
        self.score2 = 0
        self.winner = None
        
        # Countdown variables
        self.countdown_start_time = None
        self.countdown_value = 3
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
    
    def setup_game(self):
        """Initialize game objects based on selected mode"""
        if self.game_mode == SINGLE_PLAYER:
            self.snake1 = Snake((GRID_WIDTH // 2, GRID_HEIGHT // 2), GREEN, DARK_GREEN, "Player")
            self.snake2 = None
            pygame.display.set_caption("Snake Game - Single Player")
        else:  # TWO_PLAYER
            self.snake1 = Snake((GRID_WIDTH // 4, GRID_HEIGHT // 2), GREEN, DARK_GREEN, "Player 1")
            self.snake2 = Snake((3 * GRID_WIDTH // 4, GRID_HEIGHT // 2), LIGHT_BLUE, DARK_BLUE, "Player 2")
            pygame.display.set_caption("Snake Game - Two Players")
        
        self.food = Food()
        self.score1 = 0
        self.score2 = 0
        self.winner = None
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.state == MENU:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % 2
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.selected_option == 0:
                            self.game_mode = SINGLE_PLAYER
                        else:
                            self.game_mode = TWO_PLAYER
                        self.start_countdown()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                
                elif self.state == COUNTDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = MENU
                
                elif self.state == GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.restart_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = MENU
                        self.selected_option = 0
                
                elif self.state == PLAYING:
                    # Player 1 controls
                    if self.game_mode == SINGLE_PLAYER:
                        # Single player uses arrow keys
                        if event.key == pygame.K_UP:
                            self.snake1.change_direction(UP)
                        elif event.key == pygame.K_DOWN:
                            self.snake1.change_direction(DOWN)
                        elif event.key == pygame.K_LEFT:
                            self.snake1.change_direction(LEFT)
                        elif event.key == pygame.K_RIGHT:
                            self.snake1.change_direction(RIGHT)
                    else:
                        # Two player mode
                        # Player 1 controls (WASD)
                        if event.key == pygame.K_w:
                            self.snake1.change_direction(UP)
                        elif event.key == pygame.K_s:
                            self.snake1.change_direction(DOWN)
                        elif event.key == pygame.K_a:
                            self.snake1.change_direction(LEFT)
                        elif event.key == pygame.K_d:
                            self.snake1.change_direction(RIGHT)
                        
                        # Player 2 controls (Arrow keys)
                        elif event.key == pygame.K_UP:
                            self.snake2.change_direction(UP)
                        elif event.key == pygame.K_DOWN:
                            self.snake2.change_direction(DOWN)
                        elif event.key == pygame.K_LEFT:
                            self.snake2.change_direction(LEFT)
                        elif event.key == pygame.K_RIGHT:
                            self.snake2.change_direction(RIGHT)
                    
                    if event.key == pygame.K_ESCAPE:
                        self.state = MENU
                        self.selected_option = 0
        return True
    
    def start_countdown(self):
        """Start the countdown before game begins"""
        self.state = COUNTDOWN
        self.countdown_start_time = time.time()
        self.countdown_value = 3
        self.setup_game()
    
    def update_countdown(self):
        """Update countdown timer"""
        current_time = time.time()
        elapsed = current_time - self.countdown_start_time
        
        if elapsed >= 1.0:  # Each second
            self.countdown_value -= 1
            self.countdown_start_time = current_time
            
            if self.countdown_value <= 0:
                self.state = PLAYING
    
    def update(self):
        if self.state == COUNTDOWN:
            self.update_countdown()
        elif self.state == PLAYING:
            # Move snakes
            self.snake1.move()
            if self.snake2:
                self.snake2.move()
            
            # Check if snakes ate food
            if self.snake1.alive and self.snake1.body[0] == self.food.position:
                self.snake1.eat_food()
                self.score1 += 10
                if self.game_mode == SINGLE_PLAYER:
                    self.food.respawn(self.snake1.body, [])
                else:
                    self.food.respawn(self.snake1.body, self.snake2.body)
            elif self.snake2 and self.snake2.alive and self.snake2.body[0] == self.food.position:
                self.snake2.eat_food()
                self.score2 += 10
                self.food.respawn(self.snake1.body, self.snake2.body)
            
            # Check collisions
            if self.game_mode == SINGLE_PLAYER:
                # Single player - only check wall and self collision
                if self.snake1.check_collision():
                    self.state = GAME_OVER
                    self.winner = None  # No winner in single player
            else:
                # Two player mode
                snake1_collision = self.snake1.check_collision(self.snake2)
                snake2_collision = self.snake2.check_collision(self.snake1)
                
                # Apply collision results
                if snake1_collision:
                    self.snake1.alive = False
                if snake2_collision:
                    self.snake2.alive = False
                
                # Check if game is over
                if not self.snake1.alive and not self.snake2.alive:
                    self.state = GAME_OVER
                    if self.score1 > self.score2:
                        self.winner = "Player 1"
                    elif self.score2 > self.score1:
                        self.winner = "Player 2"
                    else:
                        self.winner = "Tie"
                elif not self.snake1.alive:
                    self.state = GAME_OVER
                    self.winner = "Player 2"
                elif not self.snake2.alive:
                    self.state = GAME_OVER
                    self.winner = "Player 1"
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == MENU:
            self.draw_menu()
        elif self.state == COUNTDOWN:
            self.draw_countdown()
        elif self.state == PLAYING:
            self.draw_game()
        elif self.state == GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Draw the main menu"""
        # Title
        title_text = self.large_font.render("SNAKE GAME", True, GREEN)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)
        
        # Menu options
        options = ["1 Player", "2 Players"]
        for i, option in enumerate(options):
            color = YELLOW if i == self.selected_option else WHITE
            option_text = self.font.render(option, True, color)
            option_rect = option_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 50))
            self.screen.blit(option_text, option_rect)
        
        # Instructions
        instruction_text = self.small_font.render("Use UP/DOWN arrows to navigate, ENTER to select", True, GRAY)
        instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150))
        self.screen.blit(instruction_text, instruction_rect)
    
    def draw_countdown(self):
        """Draw the countdown overlay on top of the game"""
        # First draw the game background
        self.draw_game()
        
        # Create a semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)  # Semi-transparent
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Show selected mode
        mode_text = "Single Player" if self.game_mode == SINGLE_PLAYER else "Two Players"
        mode_display = self.font.render(f"Mode: {mode_text}", True, WHITE)
        mode_rect = mode_display.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(mode_display, mode_rect)
        
        # Show countdown with larger, more prominent text
        if self.countdown_value > 0:
            countdown_text = self.large_font.render(str(self.countdown_value), True, YELLOW)
            countdown_rect = countdown_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            
            # Add a shadow effect for better visibility
            shadow_text = self.large_font.render(str(self.countdown_value), True, BLACK)
            shadow_rect = shadow_text.get_rect(center=(WINDOW_WIDTH // 2 + 3, WINDOW_HEIGHT // 2 + 3))
            self.screen.blit(shadow_text, shadow_rect)
            self.screen.blit(countdown_text, countdown_rect)
        else:
            go_text = self.large_font.render("GO!", True, GREEN)
            go_rect = go_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            
            # Add shadow for "GO!" text too
            shadow_text = self.large_font.render("GO!", True, BLACK)
            shadow_rect = shadow_text.get_rect(center=(WINDOW_WIDTH // 2 + 3, WINDOW_HEIGHT // 2 + 3))
            self.screen.blit(shadow_text, shadow_rect)
            self.screen.blit(go_text, go_rect)
        
        # Show controls
        if self.game_mode == SINGLE_PLAYER:
            controls_text = self.small_font.render("Use Arrow Keys to move", True, WHITE)
        else:
            controls_text = self.small_font.render("Player 1: WASD | Player 2: Arrow Keys", True, WHITE)
        controls_rect = controls_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        self.screen.blit(controls_text, controls_rect)
    
    def draw_game(self):
        """Draw the actual game"""
        # Draw grid lines
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))
        
        # Draw game objects
        if self.food:
            self.food.draw(self.screen)
        if self.snake1:
            self.snake1.draw(self.screen)
        if self.snake2:
            self.snake2.draw(self.screen)
        
        # Draw scores and controls
        if self.game_mode == SINGLE_PLAYER:
            score_text = self.font.render(f"Score: {self.score1}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            
            controls_text = self.small_font.render("Arrow Keys to move | ESC for menu", True, WHITE)
            self.screen.blit(controls_text, (10, WINDOW_HEIGHT - 30))
        else:
            score1_text = self.font.render(f"Player 1: {self.score1}", True, GREEN)
            score2_text = self.font.render(f"Player 2: {self.score2}", True, LIGHT_BLUE)
            self.screen.blit(score1_text, (10, 10))
            self.screen.blit(score2_text, (10, 50))
            
            controls1_text = self.small_font.render("Player 1: WASD", True, WHITE)
            controls2_text = self.small_font.render("Player 2: Arrow Keys", True, WHITE)
            self.screen.blit(controls1_text, (WINDOW_WIDTH - 150, 10))
            self.screen.blit(controls2_text, (WINDOW_WIDTH - 150, 30))
    
    def draw_game_over(self):
        """Draw the game over screen"""
        # Game over title
        game_over_text = self.large_font.render("GAME OVER!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 120))
        self.screen.blit(game_over_text, game_over_rect)
        
        if self.game_mode == SINGLE_PLAYER:
            # Single player final score
            final_score_text = self.font.render(f"Final Score: {self.score1}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            self.screen.blit(final_score_text, final_score_rect)
        else:
            # Two player results
            if self.winner == "Tie":
                winner_text = self.font.render("It's a Tie!", True, YELLOW)
            else:
                winner_text = self.font.render(f"{self.winner} Wins!", True, YELLOW)
            winner_rect = winner_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
            self.screen.blit(winner_text, winner_rect)
            
            score1_text = self.font.render(f"Player 1: {self.score1}", True, GREEN)
            score2_text = self.font.render(f"Player 2: {self.score2}", True, LIGHT_BLUE)
            score1_rect = score1_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            score2_rect = score2_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
            self.screen.blit(score1_text, score1_rect)
            self.screen.blit(score2_text, score2_rect)
        
        # Instructions
        restart_text = self.font.render("SPACE to play again | ESC for menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        self.screen.blit(restart_text, restart_rect)
    
    def restart_game(self):
        """Restart the current game mode"""
        self.start_countdown()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            
            # Adjust FPS based on game state
            if self.state == PLAYING:
                self.clock.tick(10)  # Slower for gameplay
            else:
                self.clock.tick(60)  # Faster for menus and countdown
        
        pygame.quit()
        sys.exit()