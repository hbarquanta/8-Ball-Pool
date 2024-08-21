import pygame
import numpy as np
from config import BALL_RADIUS, TABLE_WIDTH, TABLE_HEIGHT, FRICTION_COEFFICIENT

class Ball:
    def __init__(self, position, velocity=[0, 0], color=(255, 255, 255), is_striped=False, number=None):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.radius = BALL_RADIUS
        self.color = color
        self.is_striped = is_striped
        self.number = number
        self.rotation_angle = 0  # Initialize rotation angle

    def move(self, dt):
        speed = np.linalg.norm(self.velocity)
        if speed < 1:
            self.velocity = np.array([0.0, 0.0])
        else:
            self.velocity *= FRICTION_COEFFICIENT
        
        # Update rotation based on velocity
        self.rotation_angle += speed * dt * 5  # Adjust the factor to control rotation speed
        
        self.position += self.velocity * dt
        self.handle_boundary_collision()

    def handle_boundary_collision(self):
        if self.position[0] - self.radius <= 0 or self.position[0] + self.radius >= TABLE_WIDTH:
            self.velocity[0] *= -1
        if self.position[1] - self.radius <= 0 or self.position[1] + self.radius >= TABLE_HEIGHT:
            self.velocity[1] *= -1

    def handle_collision(self, other):
        dist = np.linalg.norm(self.position - other.position)
        if dist < self.radius + other.radius:
            normal = (self.position - other.position) / dist
            tangent = np.array([-normal[1], normal[0]])
            v1_normal = np.dot(self.velocity, normal)
            v1_tangent = np.dot(self.velocity, tangent)
            v2_normal = np.dot(other.velocity, normal)
            v2_tangent = np.dot(other.velocity, tangent)
            self.velocity = v2_normal * normal + v1_tangent * tangent
            other.velocity = v1_normal * normal + v2_tangent * tangent
            overlap = 0.5 * (self.radius + other.radius - dist)
            self.position += normal * overlap
            other.position -= normal * overlap

    def draw(self, screen):
        # Create a surface to draw the ball on
        ball_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(ball_surface, self.color, (self.radius, self.radius), self.radius)
        
        # If it's a striped ball, draw the stripe in the middle
        if self.is_striped:
            stripe_height = self.radius // 2
            stripe_rect = pygame.Rect(0, self.radius - stripe_height, self.radius * 2, stripe_height * 2)
            pygame.draw.rect(ball_surface, (255, 255, 255), stripe_rect)
        
        # Draw the number on the ball, unless it's the cue ball
        if self.number is not None:
            number_color = (255, 255, 255) if self.number == 8 else (0, 0, 0)  # White for 8-ball, black for others
            font = pygame.font.Font(None, 24)
            number_text = font.render(str(self.number), True, number_color)
            number_rect = number_text.get_rect(center=(self.radius, self.radius))
            ball_surface.blit(number_text, number_rect)

        # Rotate the ball surface
        rotated_ball_surface = pygame.transform.rotate(ball_surface, self.rotation_angle)
        rotated_rect = rotated_ball_surface.get_rect(center=self.position.astype(int))

        # Draw the rotated ball surface onto the screen
        screen.blit(rotated_ball_surface, rotated_rect)

    def draw_at_position(self, screen, position, scale=0.7):
        # Calculate the scaled radius
        scaled_radius = int(self.radius * scale)
        
        # Create a surface to draw the ball on
        ball_surface = pygame.Surface((scaled_radius * 2, scaled_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(ball_surface, self.color, (scaled_radius, scaled_radius), scaled_radius)
        
        # Draw the stripe if the ball is striped
        if self.is_striped:
            stripe_height = scaled_radius // 2
            stripe_rect = pygame.Rect(0, scaled_radius - stripe_height, scaled_radius * 2, stripe_height * 2)
            pygame.draw.rect(ball_surface, (255, 255, 255), stripe_rect)
        
        # Draw the number on the ball
        if self.number is not None:
            number_color = (255, 255, 255) if self.number == 8 else (0, 0, 0)
            font_size = int(24 * scale)  # Adjust font size according to the scale
            font = pygame.font.Font(None, font_size)
            number_text = font.render(str(self.number), True, number_color)
            number_rect = number_text.get_rect(center=(scaled_radius, scaled_radius))
            ball_surface.blit(number_text, number_rect)
        
        # Place the ball surface at the specified position
        screen.blit(ball_surface, (position[0] - scaled_radius, position[1] - scaled_radius))


    def is_potted(self, pockets, pocket_radius):
        for pocket in pockets:
            if np.linalg.norm(self.position - np.array(pocket)) < pocket_radius:
                return True
        return False
