import pygame
import socket
import pickle
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
        client_socket.send(pickle.dumps(data))
    else:
        server_socket.send(pickle.dumps(data))

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

# Game setup
reset_game()

# Game mode selection
print("Pong Game")
print("Select Game Mode:")
print("1. Local Multiplayer")
print("2. VS CPU")
print("3. Host")
print("4. Join")

mode = input("Enter your choice (1-4): ")

if mode == "1":
    game_mode = "local_multiplayer"
elif mode == "2":
    game_mode = "vs_cpu"
    print("Select Difficulty Level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    difficulty = input("Enter your choice (1-3): ")
    if difficulty == "1":
        paddle_speed = 3
    elif difficulty == "2":
        paddle_speed = 5
    elif difficulty == "3":
        paddle_speed = 7
    else:
        print("Invalid choice. Using medium difficulty.")
elif mode == "3":
    game_mode = "online"
    start_server()
elif mode == "4":
    game_mode = "online"
    server_ip = input("Enter the server IP address: ")
    join_server(server_ip)
else:
    print("Invalid choice. Exiting the game.")
    exit()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            if is_host:
                server_socket.close()
            else:
                client_socket.close()
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
        if ball.y < right_paddle.y:
            right_paddle.y -= paddle_speed
        if ball.y > right_paddle.y + paddle_height:
            right_paddle.y += paddle_speed

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
        send_data(game_state)
        game_state = receive_data()
        left_paddle = game_state["left_paddle"]
        right_paddle = game_state["right_paddle"]
        ball = game_state["ball"]

    # Draw the game objects
    window.fill(BLACK)
    pygame.draw.rect(window, WHITE, left_paddle)
    pygame.draw.rect(window, WHITE, right_paddle)
    pygame.draw.ellipse(window, WHITE, ball)
    pygame.draw.aaline(window, WHITE, (window_width // 2, 0), (window_width // 2, window_height))

    # Update the display
    pygame.display.update()
    clock.tick(60)