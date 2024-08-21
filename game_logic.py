import random
import math
import numpy as np
from ball import Ball
from config import TABLE_WIDTH, TABLE_HEIGHT, POCKET_RADIUS, CUE_LENGTH, pockets

class Game:
    def __init__(self):
        self.running = True
        self.game_over = False
        self.current_player = 1  # Player 1 always starts
        self.player1_type = None
        self.player2_type = None
        self.game_winner = None
        self.velocity_slider_value = 0
        self.angle_slider_value = 0
        self.shooting = False
        self.retract = 0
        self.retract_speed = 20
        self.angle_fixed = False
        self.foul_occurred = False  # Track whether a foul occurred
        self.foul_message_timer = 0  # Timer for displaying the foul message
        self.potted_balls_player1 = []  # List to store potted balls for Player 1
        self.potted_balls_player2 = []  # List to store potted balls for Player 2
        self.balls = self.arrange_triangle(TABLE_WIDTH * 3 / 4, TABLE_HEIGHT / 2, 15)
        self.cue_ball = Ball([TABLE_WIDTH / 4, TABLE_HEIGHT / 2], color=(255, 255, 255))
        self.balls.append(self.cue_ball)

    def handle_potted_ball(self, ball):
        if ball in self.balls:
            self.balls.remove(ball)
            
            if ball == self.cue_ball:  # Cue ball potted
                print(f"Player {self.current_player} committed a foul by potting the cue ball!")
                self.foul_occurred = True
                self.foul_message_timer = 120  # Display foul for 2 seconds
                self.cue_ball = Ball([TABLE_WIDTH / 4, TABLE_HEIGHT / 2], color=(255, 255, 255))
                self.balls.append(self.cue_ball)  # Re-add the cue ball to the game
                self.switch_turn()
                return

            # Assign to the correct player and add to potted balls
            if ball.number < 8:  # Solids
                if self.current_player == 1:
                    self.potted_balls_player1.append(ball)
                else:
                    self.potted_balls_player2.append(ball)
            elif ball.number > 8:  # Stripes
                if self.current_player == 1:
                    self.potted_balls_player1.append(ball)
                else:
                    self.potted_balls_player2.append(ball)

            # Handle the black ball logic (win/loss conditions)
            if ball.number == 8:
                if self.player1_type and self.player2_type:
                    self.game_over = True
                    if (self.current_player == 1 and self.player1_type == "solids" and 
                        all(b.is_potted(pockets, POCKET_RADIUS) for b in self.potted_balls_player1)) or \
                       (self.current_player == 2 and self.player2_type == "solids" and 
                        all(b.is_potted(pockets, POCKET_RADIUS) for b in self.potted_balls_player2)):
                        self.game_winner = self.current_player
                    else:
                        self.game_winner = 2 if self.current_player == 1 else 1
                return  # End the game if the black ball is potted

            # Determine and assign player types after the first potted ball
            if self.player1_type is None and self.player2_type is None:
                if ball.number < 8:  # Player potted a solid
                    self.player1_type = "solids" if self.current_player == 1 else "stripes"
                    self.player2_type = "stripes" if self.current_player == 1 else "solids"
                else:  # Player potted a stripe
                    self.player1_type = "stripes" if self.current_player == 1 else "solids"
                    self.player2_type = "solids" if self.current_player == 1 else "stripes"
                print(f"Player 1: {self.player1_type}, Player 2: {self.player2_type}")

            # Check if the player potted the correct type of ball
            if (self.current_player == 1 and 
                ((self.player1_type == "solids" and ball.number < 8) or
                 (self.player1_type == "stripes" and ball.number > 8))) or \
               (self.current_player == 2 and 
                ((self.player2_type == "solids" and ball.number < 8) or
                 (self.player2_type == "stripes" and ball.number > 8))):
                # Continue the same player's turn if they potted the correct ball
                print(f"Player {self.current_player} potted the correct ball and continues playing.")
            else:
                # Switch turns if the wrong type was potted or no ball was potted
                self.switch_turn()

    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def arrange_triangle(self, start_x, start_y, ball_radius):
        colors = [(255, 255, 0), (0, 0, 255), (255, 0, 0), (128, 0, 128),
                  (255, 165, 0), (128, 0, 0), (0, 128, 0), (0, 0, 0),
                  (255, 255, 0), (0, 0, 255), (255, 0, 0), (128, 0, 128),
                  (255, 165, 0), (128, 0, 0), (0, 128, 0)]
        striped = [False] * 7 + [False] + [True] * 7
        positions = []
        for row in range(5):
            for col in range(row + 1):
                x_offset = row * ball_radius * (3 ** 0.5)
                y_offset = (2 * col - row) * ball_radius
                positions.append((start_x + x_offset, start_y + y_offset))
        random_indices = list(range(15))
        random.shuffle(random_indices)
        random_indices.remove(7)
        balls = []
        center_position = positions[4]
        balls.append(Ball(position=center_position, color=(0, 0, 0), number=8))
        i = 0
        for idx, pos in enumerate(positions):
            if pos == center_position:
                continue
            ball_color = colors[random_indices[i]]
            is_striped_ball = striped[random_indices[i]]
            ball_number = random_indices[i] + 1
            balls.append(Ball(position=pos, color=ball_color, is_striped=is_striped_ball, number=ball_number))
            i += 1
        return balls

    def update(self):
        if self.shooting:
            self.handle_shooting()
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                self.balls[i].handle_collision(self.balls[j])
        for ball in self.balls[:]:
            ball.move(1 / 60)
            if ball.is_potted(pockets, POCKET_RADIUS):
                self.handle_potted_ball(ball)
        if self.all_balls_stopped() and not self.game_over:
            if not any(ball.is_potted(pockets, POCKET_RADIUS) for ball in self.balls if ball != self.cue_ball):
                self.switch_turn()
            self.check_game_over()

    def check_game_over(self):
        if all(ball.number != 8 or ball.is_potted(pockets, POCKET_RADIUS) for ball in self.balls):
            if self.player1_type == "solids" and all(
                    ball.is_potted(pockets, POCKET_RADIUS) for ball in self.potted_balls_player1 if ball.number < 8):
                self.game_winner = 1
            elif self.player2_type == "stripes" and all(
                    ball.is_potted(pockets, POCKET_RADIUS) for ball in self.potted_balls_player2 if ball.number > 8):
                self.game_winner = 2
            self.game_over = True

    def handle_mouse_click(self, pos):
        mouse_x, mouse_y = pos
        
        if self.game_over:
            if (TABLE_WIDTH // 2 - 75) <= mouse_x <= (TABLE_WIDTH // 2 - 75) + 150 and \
               (TABLE_HEIGHT // 2 + 50) <= mouse_y <= (TABLE_HEIGHT // 2 + 50) + 50:
                self.reset_game()
                return  # Exit the method after resetting the game to avoid any further actions

        if 50 <= mouse_x <= 50 + 200 and 460 <= mouse_y <= 460 + 10:
            self.velocity_slider_value = (mouse_x - 50) / 200 * 1000
        elif 400 > mouse_y:
            dx = mouse_x - self.cue_ball.position[0]
            dy = mouse_y - self.cue_ball.position[1]
            self.angle_slider_value = math.degrees(math.atan2(dy, dx))
            self.angle_fixed = True
        elif self.all_balls_stopped() and self.angle_fixed and \
                650 <= mouse_x <= 650 + 100 and 440 <= mouse_y <= 440 + 30:
            self.shooting = True

    def handle_mouse_motion(self, pos):
        if not self.angle_fixed and self.all_balls_stopped():
            mouse_x, mouse_y = pos
            if 400 > mouse_y:
                dx = mouse_x - self.cue_ball.position[0]
                dy = mouse_y - self.cue_ball.position[1]
                self.angle_slider_value = math.degrees(math.atan2(dy, dx))

    def all_balls_stopped(self):
        return all(np.linalg.norm(ball.velocity) < 0.1 for ball in self.balls)

    def handle_shooting(self):
        if self.retract < 100:
            self.retract += self.retract_speed
        else:
            angle_rad = math.radians(self.angle_slider_value)
            velocity_x = self.velocity_slider_value * math.cos(angle_rad)
            velocity_y = self.velocity_slider_value * math.sin(angle_rad)
            self.cue_ball.velocity = np.array([velocity_x, velocity_y])
            self.shooting = False
            self.retract = 0
            self.angle_fixed = False

    def reset_game(self):
        self.running = True
        self.game_over = False
        self.current_player = 1  # Player 1 always starts
        self.player1_type = None
        self.player2_type = None
        self.game_winner = None
        self.velocity_slider_value = 0
        self.angle_slider_value = 0
        self.shooting = False
        self.retract = 0
        self.retract_speed = 20
        self.angle_fixed = False
        self.foul_occurred = False
        self.potted_balls_player1 = []
        self.potted_balls_player2 = []
        self.balls = self.arrange_triangle(TABLE_WIDTH * 3 / 4, TABLE_HEIGHT / 2, 15)
        self.cue_ball = Ball([TABLE_WIDTH / 4, TABLE_HEIGHT / 2], color=(255, 255, 255))
        self.balls.append(self.cue_ball)
