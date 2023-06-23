import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 640
window_height = 480
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pong")

# Set up colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

# Set up the paddles
paddle_width = 10
paddle_height = 60
paddle_speed = 5
left_paddle = pygame.Rect(50, window_height // 2 - paddle_height // 2, paddle_width, paddle_height)
right_paddle = pygame.Rect(window_width - 50 - paddle_width, window_height // 2 - paddle_height // 2, paddle_width, paddle_height)

# Set up the ball
ball_radius = 10
ball_x_speed = 3
ball_y_speed = 3
ball = pygame.Rect(window_width // 2 - ball_radius // 2, window_height // 2 - ball_radius // 2, ball_radius, ball_radius)

# Set up game mode
player_vs_player = False  # Change to True for player vs player mode

# Set up CPU paddle
cpu_paddle_speed = 3
cpu_paddle_movement_delay = 30
cpu_paddle_movement_counter = 0

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    # Move the paddles (Player 1 controls)
    if keys[K_w] and left_paddle.y > 0:
        left_paddle.y -= paddle_speed
    if keys[K_s] and left_paddle.y < window_height - paddle_height:
        left_paddle.y += paddle_speed

    if player_vs_player:
        # Move the paddles (Player 2 controls)
        if keys[K_UP] and right_paddle.y > 0:
            right_paddle.y -= paddle_speed
        if keys[K_DOWN] and right_paddle.y < window_height - paddle_height:
            right_paddle.y += paddle_speed
    else:
        # Move the CPU paddle (Player 2 controlled by CPU)
        if cpu_paddle_movement_counter >= cpu_paddle_movement_delay:
            if ball.y < right_paddle.y:
                right_paddle.y -= cpu_paddle_speed
            if ball.y > right_paddle.y + paddle_height:
                right_paddle.y += cpu_paddle_speed
            cpu_paddle_movement_counter = 0
        else:
            cpu_paddle_movement_counter += 1

    # Move the ball
    ball.x += ball_x_speed
    ball.y += ball_y_speed

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_x_speed *= -1

    # Ball collision with walls
    if ball.y <= 0 or ball.y >= window_height - ball_radius:
        ball_y_speed *= -1

    # Draw the game objects
    window.fill(BLACK)
    pygame.draw.rect(window, WHITE, left_paddle)
    pygame.draw.rect(window, WHITE, right_paddle)
    pygame.draw.ellipse(window, WHITE, ball)
    pygame.draw.aaline(window, WHITE, (window_width // 2, 0), (window_width // 2, window_height))

    # Update the display
    pygame.display.update()
    clock.tick(60)