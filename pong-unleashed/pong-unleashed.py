import pygame
from pygame.locals import *

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

# Set up game mode selection
game_mode = None

# Set up CPU paddle
cpu_paddle_speed = 3
cpu_paddle_movement_delay = 30
cpu_paddle_movement_counter = 0

clock = pygame.time.Clock()

def reset_game():
    global game_mode, left_paddle, right_paddle, ball, ball_x_speed, ball_y_speed
    game_mode = None
    left_paddle = pygame.Rect(50, window_height // 2 - paddle_height // 2, paddle_width, paddle_height)
    right_paddle = pygame.Rect(window_width - 50 - paddle_width, window_height // 2 - paddle_height // 2, paddle_width, paddle_height)
    ball = pygame.Rect(window_width // 2 - ball_radius // 2, window_height // 2 - ball_radius // 2, ball_radius, ball_radius)
    ball_x_speed = 3
    ball_y_speed = 3

def draw_game_mode_menu():
    font = pygame.font.Font(None, 36)
    title_text = font.render("PONG", True, WHITE)
    local_multiplayer_text = font.render("1. Local Multiplayer", True, WHITE)
    vs_cpu_text = font.render("2. VS CPU", True, WHITE)

    window.fill(BLACK)
    window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 100))
    window.blit(local_multiplayer_text, (window_width // 2 - local_multiplayer_text.get_width() // 2, 200))
    window.blit(vs_cpu_text, (window_width // 2 - vs_cpu_text.get_width() // 2, 250))

    pygame.display.update()

reset_game()

while True:
    if game_mode is None:
        draw_game_mode_menu()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    game_mode = "local_multiplayer"
                elif event.key == K_2:
                    game_mode = "vs_cpu"
                    cpu_paddle_movement_counter = cpu_paddle_movement_delay // 2

        clock.tick(60)
        continue

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

    if game_mode == "local_multiplayer":
        # Move the paddles (Player 2 controls)
        if keys[K_UP] and right_paddle.y > 0:
            right_paddle.y -= paddle_speed
        if keys[K_DOWN] and right_paddle.y < window_height - paddle_height:
            right_paddle.y += paddle_speed
    elif game_mode == "vs_cpu":
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

    # Check if the ball is out of bounds
    if ball.x < 0 or ball.x > window_width:
        reset_game()

    # Draw the game objects
    window.fill(BLACK)
    pygame.draw.rect(window, WHITE, left_paddle)
    pygame.draw.rect(window, WHITE, right_paddle)
    pygame.draw.ellipse(window, WHITE, ball)
    pygame.draw.aaline(window, WHITE, (window_width // 2, 0), (window_width // 2, window_height))

    # Update the display
    pygame.display.update()
    clock.tick(60)