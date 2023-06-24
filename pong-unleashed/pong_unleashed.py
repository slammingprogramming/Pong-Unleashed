import pygame
import socket
import pickle
from pygame.locals import *
import sys
import select
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 640
window_height = 480
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pong Unleashed")

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

# Set up networking
HOST = socket.gethostname()  # Get the host name
PORT = 12345  # Choose a port number
server_socket = None
client_socket = None
is_host = None

# Set up game state synchronization
game_state = {
    "left_paddle": left_paddle,
    "right_paddle": right_paddle,
    "ball": ball
}

clock = pygame.time.Clock()

paused = False  # Variable to track whether the game is paused or not

def start_server():
    global server_socket, is_host
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    is_host = True

def join_server(server_ip):
    global client_socket, is_host
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, PORT))
    is_host = False

def send_data(data):
    if is_host:
        client_socket.sendall(pickle.dumps(data))
    else:
        client_socket.sendall(pickle.dumps(data))

def receive_data():
    if is_host:
        data = server_socket.recv(4096)
    else:
        data = client_socket.recv(4096)
    return pickle.loads(data)

def reset_game():
    global left_paddle, right_paddle, ball, ball_x_speed, ball_y_speed
    left_paddle = pygame.Rect(50, window_height // 2 - paddle_height // 2, paddle_width, paddle_height)
    right_paddle = pygame.Rect(window_width - 50 - paddle_width, window_height // 2 - paddle_height // 2, paddle_width, paddle_height)
    ball = pygame.Rect(window_width // 2 - ball_radius // 2, window_height // 2 - ball_radius // 2, ball_radius, ball_radius)
    ball_x_speed = 3
    ball_y_speed = 3

def run_tutorial():
    tutorial_steps = [
        "Welcome to Pong Unleashed Tutorial!",
        "Objective: Use your paddle to hit the ball past your opponent.",
        "Controls: Player 1 uses 'W' and 'S' keys to move the left paddle.",
        "Player 2 (CPU) controls the right paddle in this tutorial.",
        "Step 1: Move your paddle using the 'W' and 'S' keys to intercept the ball.",
        "Step 2: The ball will bounce off the paddles and walls.",
        "Step 3: Try to hit the ball past your opponent's paddle to score a point.",
        "Step 4: The first player to reach 5 points wins the game.",
        "Congratulations! You have completed the tutorial.",
        "Feel free to explore other game modes and options."
    ]

    current_step = 0
    font = pygame.font.Font(None, 24)

    while True:
        window.fill(BLACK)
        text = font.render(tutorial_steps[current_step], True, WHITE)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(text, text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_SPACE:
                    current_step += 1
                    if current_step >= len(tutorial_steps):
                        return

# Game setup
reset_game()

# Game mode selection
print("Pong Game")
print("Select Game Mode:")
print("1. Local Multiplayer")
print("2. VS CPU")
print("3. Host")
print("4. Join")
print("5. Tutorial")

mode = input("Enter your choice (1-5): ")

if mode == "1":
    game_mode = "local_multiplayer"
elif mode == "2":
    game_mode = "vs_cpu"
    print("Select Difficulty Level:")
    print("1. Easy - The CPU paddle has a moderate chance of missing the ball.")
    print("2. Medium - The CPU paddle has a lower chance of missing the ball.")
    print("3. Hard - The CPU paddle has a very low chance of missing the ball.")
    print("4. Advanced - The CPU paddle uses advanced strategies to avoid losing.")
    print("5. Expert - The CPU paddle actively attempts shots to challenge the player")
    print("6. Impossible - The CPU paddle never misses the ball.")
    difficulty_level = int(input("Enter difficulty level (1-6): "))
    if difficulty_level < 1 or difficulty_level > 6:
        print("Invalid difficulty level. Exiting the game.")
        sys.exit()
elif mode == "3":
    game_mode = "online"
    print("Server will be hosted on: ", HOST)
    port_choice = input("Enter the port to host the server on (default: 12345): ")
    PORT = int(port_choice) if port_choice.isdigit() else PORT
    start_server()
elif mode == "4":
    game_mode = "online"
    server_ip = input("Enter the server IP address: ")
    port_choice = input("Enter the port of the server (default: 12345): ")
    PORT = int(port_choice) if port_choice.isdigit() else PORT
    join_server(server_ip, PORT)
elif mode == "5":
    game_mode = "tutorial"
    run_tutorial()
else:
    print("Invalid choice. Exiting the game.")
    exit()

# Non-blocking receive function
def non_blocking_receive(socket_obj):
    ready = select.select([socket_obj], [], [], 0.01)
    if ready[0]:
        return socket_obj.recv(4096)
    else:
        return None

# Move the CPU paddle
def move_cpu_paddle(difficulty):
    if difficulty == 1:
        # Easy difficulty: The CPU paddle moves randomly
        if random.randint(0, 1) == 0:
            if right_paddle.y > 0:
                right_paddle.y -= paddle_speed
        else:
            if right_paddle.y < window_height - paddle_height:
                right_paddle.y += paddle_speed
    elif difficulty == 2:
        # Medium difficulty: The CPU paddle tries to follow the ball vertically
        if ball.y < right_paddle.y:
            if right_paddle.y > 0:
                right_paddle.y -= paddle_speed
        elif ball.y > right_paddle.y + paddle_height:
            if right_paddle.y < window_height - paddle_height:
                right_paddle.y += paddle_speed
    elif difficulty == 3:
        # Hard difficulty: The CPU paddle tries to predict the ball's position
        if ball.y < right_paddle.y + paddle_height // 2:
            if right_paddle.y > 0:
                right_paddle.y -= paddle_speed
        elif ball.y > right_paddle.y + paddle_height // 2:
            if right_paddle.y < window_height - paddle_height:
                right_paddle.y += paddle_speed
    elif difficulty == 4:
        # Advanced difficulty: The CPU paddle uses advanced strategies
        if ball_x_speed > 0:
            # Predict the ball's position based on the estimated time of arrival
            estimated_time = (right_paddle.x - ball.x) // ball_x_speed
            predicted_y = ball.y + ball_y_speed * estimated_time
            if predicted_y < right_paddle.y + paddle_height // 2:
                if right_paddle.y > 0:
                    right_paddle.y -= paddle_speed
            elif predicted_y > right_paddle.y + paddle_height // 2:
                if right_paddle.y < window_height - paddle_height:
                    right_paddle.y += paddle_speed
        else:
            # React to the ball's current position if the ball is moving away
            if ball.y < right_paddle.y + paddle_height // 2:
                if right_paddle.y > 0:
                    right_paddle.y -= paddle_speed
            elif ball.y > right_paddle.y + paddle_height // 2:
                if right_paddle.y < window_height - paddle_height:
                    right_paddle.y += paddle_speed
    elif difficulty == 5:
        # Expert difficulty: The CPU paddle actively attempts shots to challenge the player
        if ball_x_speed > 0:
            # Predict the ball's position based on the estimated time of arrival
            estimated_time = (right_paddle.x - ball.x) // ball_x_speed
            predicted_y = ball.y + ball_y_speed * estimated_time
            if predicted_y < right_paddle.y + paddle_height // 2:
                if right_paddle.y > 0:
                    right_paddle.y -= paddle_speed
            elif predicted_y > right_paddle.y + paddle_height // 2:
                if right_paddle.y < window_height - paddle_height:
                    right_paddle.y += paddle_speed
        else:
            # Move the paddle to perform shots that challenge the player
            if right_paddle.y + paddle_height // 2 < window_height // 2:
                if right_paddle.y < window_height - paddle_height:
                    right_paddle.y += paddle_speed
            elif right_paddle.y + paddle_height // 2 > window_height // 2:
                if right_paddle.y > 0:
                    right_paddle.y -= paddle_speed
    elif difficulty == 6:
        # Impossible difficulty: The CPU paddle never misses the ball
        if ball.y < right_paddle.y + paddle_height // 2:
            if right_paddle.y > 0:
                right_paddle.y -= paddle_speed
        elif ball.y > right_paddle.y + paddle_height // 2:
            if right_paddle.y < window_height - paddle_height:
                right_paddle.y += paddle_speed

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            if is_host:
                server_socket.close()
            else:
                client_socket.close()
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_p and game_mode != "online":
                paused = not paused  # Toggle pause state when 'P' key is pressed

    if not paused:  # Only update game logic if the game is not paused

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
        move_cpu_paddle(difficulty_level)

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

    # Synchronize game state
    game_state["left_paddle"] = left_paddle
    game_state["right_paddle"] = right_paddle
    game_state["ball"] = ball

    if game_mode == "online":
        try:
            send_data(game_state)
            received_data = non_blocking_receive(server_socket if is_host else client_socket)
            if received_data:
                game_state = pickle.loads(received_data)
                left_paddle = game_state["left_paddle"]
                right_paddle = game_state["right_paddle"]
                ball = game_state["ball"]
        except socket.error as e:
            print("Socket error:", e)
            break

    # Draw the game objects
    window.fill(BLACK)
    pygame.draw.rect(window, WHITE, left_paddle)
    pygame.draw.rect(window, WHITE, right_paddle)
    pygame.draw.ellipse(window, WHITE, ball)
    pygame.draw.aaline(window, WHITE, (window_width // 2, 0), (window_width // 2, window_height))

    # Draw pause message if the game is paused
    if paused:
        font = pygame.font.Font(None, 36)
        text = font.render("Paused", True, WHITE)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(text, text_rect)

    # Update the display
    pygame.display.update()
    clock.tick(60)