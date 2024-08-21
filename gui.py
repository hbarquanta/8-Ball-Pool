import pygame
import math
from config import TABLE_HEIGHT, TABLE_WIDTH, GREEN, WHITE, BLACK, SLIDER_WIDTH, SLIDER_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, POCKET_RADIUS, pockets

class GameGUI:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
         # Load the carpet texture
        self.table_texture = pygame.image.load('carpet.png')
        
        # Resize the texture to fit the table dimensions
        self.table_texture = pygame.transform.scale(self.table_texture, (TABLE_WIDTH, TABLE_HEIGHT))
        
         # Load the wooden texture for the GUI background
        self.gui_texture = pygame.image.load('wood.png')  # Use the correct path to the wooden texture
        self.gui_texture = pygame.transform.scale(self.gui_texture, (TABLE_WIDTH, 100))  # Adjust the size as needed
   
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game.game_over:
                    mouse_x, mouse_y = event.pos
                    if 350 <= mouse_x <= 350 + BUTTON_WIDTH and 500 <= mouse_y <= 500 + BUTTON_HEIGHT:
                        self.game.reset_game()
                else:
                    self.game.handle_mouse_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                if not self.game.game_over:
                    self.game.handle_mouse_motion(event.pos)

    def render(self):
        # Draw the carpet texture as the background
        self.screen.blit(self.table_texture, (0, 0))
        # Draw the wooden texture for the GUI background
        self.screen.blit(self.gui_texture, (0, TABLE_HEIGHT))
        pygame.draw.rect(self.screen, BLACK, pygame.Rect(0, 0, 800, 400), 5)
        self.draw_pockets()
        self.draw_power_slider(self.screen, 50, 460, self.game.velocity_slider_value, 1000, "Power")
        
        if self.game.game_over:
            self.display_winner()
            self.draw_button(self.screen, TABLE_WIDTH // 2 - 75, TABLE_HEIGHT // 2 + 50, "Restart", width=150, height=50)
        else:
            if self.game.all_balls_stopped():
                self.draw_button(self.screen, 650, 440, "Shoot")
            self.draw_game_status(self.screen)
            for ball in self.game.balls:
                ball.draw(self.screen)
            if not self.game.shooting and self.game.all_balls_stopped():
                self.draw_cue()
                self.draw_dashed_line()
            self.display_potted_balls()

            if self.game.foul_occurred and self.game.foul_message_timer > 0:
                self.display_foul_message()
                self.game.foul_message_timer -= 1
            elif self.game.foul_message_timer <= 0:
                self.game.foul_occurred = False
        # Add the credits text
        font = pygame.font.Font(None, 24)
        credits_text = "github/hbarquanta, 2024"
        text_surface = font.render(credits_text, True, BLACK)
        text_rect = text_surface.get_rect(bottomright=(TABLE_WIDTH - 10, TABLE_HEIGHT + 100))
        self.screen.blit(text_surface, text_rect)
    
    def draw_power_slider(self, screen, x, y, value, max_value, label):
        segment_width = SLIDER_WIDTH // 4
        pygame.draw.rect(screen, (0, 255, 0), (x, y, segment_width * 2, SLIDER_HEIGHT))
        pygame.draw.rect(screen, (255, 255, 0), (x + segment_width * 2, y, segment_width, SLIDER_HEIGHT))
        pygame.draw.rect(screen, (255, 0, 0), (x + segment_width * 3, y, segment_width, SLIDER_HEIGHT))
        slider_pos = x + (value / max_value) * SLIDER_WIDTH
        pygame.draw.circle(screen, BLACK, (int(slider_pos), y + SLIDER_HEIGHT // 2), 8)
        font = pygame.font.Font(None, 24)
        text = font.render(label, True, BLACK)
        screen.blit(text, (x + SLIDER_WIDTH + 20, y))

    def draw_button(self, screen, x, y, text, width=BUTTON_WIDTH, height=BUTTON_HEIGHT):
        pygame.draw.rect(screen, BLACK, (x, y, width, height))
        font = pygame.font.Font(None, 30)
        label = font.render(text, True, WHITE)
        label_rect = label.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(label, label_rect)

    def draw_game_status(self, screen):
        font = pygame.font.Font(None, 24)
        status_text = f"Player {self.game.current_player}'s Turn"
        screen.blit(font.render(status_text, True, BLACK), (800 - 250, 400 + 10))
        if self.game.player1_type:
            screen.blit(font.render(f"Player 1: {self.game.player1_type.capitalize()}", True, BLACK), (50, 400 + 10))
        if self.game.player2_type:
            screen.blit(font.render(f"Player 2: {self.game.player2_type.capitalize()}", True, BLACK), (50, 400 + 30))

    def draw_pockets(self):
        for pocket in pockets:
            pygame.draw.circle(self.screen, BLACK, pocket, POCKET_RADIUS)

    def draw_cue(self):
        cue_ball = self.game.cue_ball
        angle = self.game.angle_slider_value
        retract = self.game.retract
        cue_x = cue_ball.position[0] - (100 - retract) * math.cos(math.radians(angle))
        cue_y = cue_ball.position[1] - (100 - retract) * math.sin(math.radians(angle))
        pygame.draw.line(self.screen, WHITE, cue_ball.position.astype(int), (int(cue_x), int(cue_y)), 3)

    def draw_dashed_line(self):
        cue_ball = self.game.cue_ball
        angle = self.game.angle_slider_value
        dash_length = 10
        dash_space = 5
        total_length = 0
        start_x, start_y = cue_ball.position
        angle_rad = math.radians(angle)
        while total_length < 350:
            end_x = start_x + dash_length * math.cos(angle_rad)
            end_y = start_y + dash_length * math.sin(angle_rad)
            pygame.draw.line(self.screen, WHITE, (int(start_x), int(start_y)), (int(end_x), int(end_y)), 2)
            start_x = end_x + dash_space * math.cos(angle_rad)
            start_y = end_y + dash_space * math.sin(angle_rad)
            total_length += dash_length + dash_space

    def display_winner(self):
        font = pygame.font.Font(None, 74)
        winner_text = f"Player {self.game.game_winner} Wins!"
        text_surface = font.render(winner_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(TABLE_WIDTH / 2, TABLE_HEIGHT / 2))
        self.screen.blit(text_surface, text_rect)

    def display_potted_balls(self):
     #font = pygame.font.Font(None, 24)
     
     # Offsets for Player 1 and Player 2
     #x_offset = 50
     y_offset_solids = TABLE_HEIGHT + 5
     y_offset_stripes = TABLE_HEIGHT + 30
     
     # Adjusted offsets for the potted balls to be next to the player info
     potted_ball_x_offset = 200
     
     # Display potted solid balls for both players
     solid_balls = [ball for ball in (self.game.potted_balls_player1 + self.game.potted_balls_player2) if ball.number < 8]
     for i, ball in enumerate(solid_balls):
         ball.draw_at_position(self.screen, (potted_ball_x_offset + (i * 30), y_offset_solids + 10))
     
     # Display potted striped balls for both players
     striped_balls = [ball for ball in (self.game.potted_balls_player1 + self.game.potted_balls_player2) if ball.number > 8]
     for i, ball in enumerate(striped_balls):
         ball.draw_at_position(self.screen, (potted_ball_x_offset + (i * 30), y_offset_stripes + 10))

    def display_foul_message(self):
        font = pygame.font.Font(None, 50)
        message = "Foul! Opponent's Turn"
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(TABLE_WIDTH / 2, TABLE_HEIGHT / 2 + 100))
        self.screen.blit(text_surface, text_rect)
