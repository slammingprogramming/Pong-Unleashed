import ipaddress
import pygame
import socket
import pickle
from pygame.locals import *
import sys
import select
import random
# import time
import threading

pygame.init()

# PONG UNLEASHED!
# Thank you for downloading Pong Unleashed (I really hope this doesn't violate any copyrights)
# This is a project to bring Pong to the modern era, along with a series of other games I'd like
# to revitalize as part of the larger goal.
# And of course, thanks for enjoying the game :)
# Made by SlammingProgramming (https://github.com/slammingprogramming)
# Source is available on GitHub, this work is licensed under the GPLv3
# https://github.com/slammingprogramming/Pong-Unleashed

# Global declaration
global showMenu, inGame, game_mode, paused, music_volume, current_song, player1_score, player2_score

# Window vars
window_width = 960
window_height = 720
splash_bg = pygame.image.load('images/splash.jpg')
paused = False
version_number = "0.1.0"
program_name = "Pong Unleashed v" + version_number
showMenu = True
inGame = False
game_mode = None
music_volume = 0.5
fade_duration = 2000  # milliseconds

# Create a playlist of songs for inGame and set title screen music as current song
playlist = ["music/song1.mp3", "music/song2.mp3", "music/song3.mp3"]
current_song = "music/title_screen_music.mp3"

# Fonts
title_font_size = 36
options_font_size = 24

# Colors
bgColor = pygame.Color(0, 0, 0)
textColor = pygame.Color(255, 255, 255)
errorColor = pygame.Color(255, 0, 0)

# Player 1 paddle settings
paddle_width_left = 10
paddle_height_left = 60
paddle_speed_left = 8

# Player 2 paddle settings
paddle_width_right = 10
paddle_height_right = 60
paddle_speed_right = 8

# Ball settings
ball_radius = 10
ball_x_speed = random.randint(4, 10)
ball_y_speed = random.randint(4, 10)

# Define characteristics of paddles and ball
left_paddle = pygame.Rect(50, window_height // 2 - paddle_height_left // 2, paddle_width_left, paddle_height_left)
right_paddle = pygame.Rect(window_width - 50 - paddle_width_right, window_height // 2 - paddle_height_right // 2,
                           paddle_width_right, paddle_height_right)
ball = pygame.Rect(window_width // 2 - ball_radius // 2, window_height // 2 - ball_radius // 2, ball_radius, ball_radius
                   )

# Set up scoring system
player1_score = 0
player2_score = 0
score_font_size = 18

# Set up game state synchronization
game_state = {
    "left_paddle": left_paddle,
    "right_paddle": right_paddle,
    "ball": ball
}

# Set up networking
lan_IP = socket.gethostbyname(socket.gethostname())  # Get the IP of the device on the LAN
connection_ip = None  # Stores the IP we are connect(ing/ed) to
PORT = 12345  # Sets the port for connections
server_socket = None  # Dedicated server communication socket, also used to initiate Direct Connect sessions
client_socket = None  # Direct Connect client communication socket
hostdc_socket = None  # Direct Connect host communication socket
is_host = None  # Stores if we are the host in a Direct Connect session
packet_size = 4096  # Sets the packet size in bytes for network communication
socket_timeout = 0.01

# Function to fade out the current song
def fade_out_song():
    for vol in range(int(music_volume * 100), 0, -1):
        pygame.mixer.music.set_volume(vol / 100)
        pygame.time.delay(int(fade_duration / (music_volume * 100)))


# Function to select a new song from the playlist that is different from the current song
def change_song():
    global current_song
    # Select a new song from the playlist that is different from the current song
    new_song = random.choice(playlist)
    while new_song == current_song:
        new_song = random.choice(playlist)
    current_song = new_song


# Function to load and play the new song and set it to the desired volume level
def load_and_play_song():
    pygame.mixer.music.load(current_song)
    pygame.mixer.music.set_volume(0)
    for vol in range(int(music_volume * 100)):
        pygame.mixer.music.set_volume(vol / 100)
        pygame.time.delay(int(fade_duration / (music_volume * 100)))
    pygame.mixer.music.set_volume(music_volume)
    if showMenu:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play(0)

# Initialize window, display splash

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(program_name)
splash_bg = pygame.transform.scale(splash_bg, (window_width, window_height))
window.blit(splash_bg, (0, 0))
clock = pygame.time.Clock()

# Load and play title screen music
current_song = "music/title_screen_music.mp3"
load_and_play_song()

# Networking Functions
def start_server():  # Start a server on the local device to host a direct connect session
    global server_socket, is_host
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((lan_IP, PORT))
    server_socket.listen(1)
    is_host = True


def listen_for_clients():  # Once the  direct connect server is running, listen for an incoming connection.
    global hostdc_socket
    hostdc_socket, client_address = server_socket.accept()


def join_server(connection_ip, PORT):  # Join a server or direct connect
    global client_socket, is_host
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((connection_ip, PORT))
    is_host = False


def send_data(data):  # Send data to the client(if hosting direct connect), or to the server/host.
    if is_host:
        hostdc_socket.sendall(pickle.dumps(data))
    else:
        client_socket.sendall(pickle.dumps(data))


def receive_data():  # Receive data from the client(if hosting direct connect), or to the server/host.
    if is_host:
        data = hostdc_socket.recv(packet_size)
    else:
        data = client_socket.recv(packet_size)
    return pickle.loads(data)


def non_blocking_receive(socket_obj):
    ready = select.select([socket_obj], [], [], socket_timeout)
    if ready[0]:
        return socket_obj.recv(packet_size)
    else:
        return None


def reset_game():  # reset the match on screen
    global left_paddle, right_paddle, ball, ball_x_speed, ball_y_speed
    left_paddle = pygame.Rect(50, window_height // 2 - paddle_height_left // 2, paddle_width_left, paddle_height_left)
    right_paddle = pygame.Rect(window_width - 50 - paddle_width_right, window_height // 2 - paddle_height_right // 2,
                               paddle_width_right, paddle_height_right)
    ball = pygame.Rect(window_width // 2 - ball_radius // 2, window_height // 2 - ball_radius // 2, ball_radius,
                       ball_radius)
    ball_x_speed = random.randint(4, 10)
    ball_y_speed = random.randint(4, 10)


def safe_exit():  # safely exit the game and ensure all sockets are closed and servers shut down
    if is_host and game_mode == "online":
        print("Shutting down hosted online game.")
        server_socket.close()
        hostdc_socket.close()
    elif not is_host and game_mode == "online":
        print("Shutting down online game client")
        client_socket.close()
    else:
        print("Shutting down offline game.")
    pygame.quit()
    sys.exit(0)


# Move the CPU paddle based on difficulty level
def move_cpu_paddle(difficulty_level):
    if difficulty_level == 1:
        # Easy difficulty: The CPU paddle follows the ball with random delay (3 to 10 seconds)
        def update_paddle_position():
            reaction_time = random.uniform(3, 10)
            pygame.time.wait(int(reaction_time * 1000))
            if ball.y < right_paddle.y:
                if right_paddle.y > 0:
                    right_paddle.y -= paddle_speed_right
            elif ball.y > right_paddle.y + paddle_height_right:
                if right_paddle.y < window_height - paddle_height_right:
                    right_paddle.y += paddle_speed_right
        cpu_paddle_thread = threading.Thread(target=update_paddle_position)
        cpu_paddle_thread.start()

    elif difficulty_level == 2:
        # Medium difficulty: The CPU paddle follows the ball with a reaction time of 1 to 3 seconds
        def update_paddle_position():
            reaction_time = random.uniform(1, 3)
            pygame.time.wait(int(reaction_time * 1000))
            if ball.y < right_paddle.y:
                if right_paddle.y > 0:
                    right_paddle.y -= paddle_speed_right
            elif ball.y > right_paddle.y + paddle_height_right:
                if right_paddle.y < window_height - paddle_height_right:
                    right_paddle.y += paddle_speed_right
        cpu_paddle_thread = threading.Thread(target=update_paddle_position)
        cpu_paddle_thread.start()
    elif difficulty_level == 3:
        # Hard difficulty: The CPU paddle tries to predict the ball's position with a reaction time of 0-2 seconds
        def update_paddle_position():
            reaction_time = random.uniform(0, 2)
            pygame.time.wait(int(reaction_time * 1000))
            if ball_x_speed > 0:
                # Predict the ball's position based on the estimated time of arrival
                estimated_time = (right_paddle.x - ball.x) // ball_x_speed
                predicted_y = ball.y + ball_y_speed * estimated_time
                if predicted_y < right_paddle.y + paddle_height_right // 2:
                    if right_paddle.y > 0:
                        right_paddle.y -= paddle_speed_right
                elif predicted_y > right_paddle.y + paddle_height_right // 2:
                    if right_paddle.y < window_height - paddle_height_right:
                        right_paddle.y += paddle_speed_right
            else:
                # React to the ball's current position if the ball is moving away
                if ball.y < right_paddle.y + paddle_height_right // 2:
                    if right_paddle.y > 0:
                        right_paddle.y -= paddle_speed_right
                elif ball.y > right_paddle.y + paddle_height_right // 2:
                    if right_paddle.y < window_height - paddle_height_right:
                        right_paddle.y += paddle_speed_right
        paddle_thread = threading.Thread(target=update_paddle_position)
        paddle_thread.start()
    elif difficulty_level == 4:
        # Advanced difficulty: The CPU paddle predicts the ball without any delay.
        if ball_x_speed > 0:
            # Predict the ball's position based on the estimated time of arrival
            estimated_time = (right_paddle.x - ball.x) // ball_x_speed
            predicted_y = ball.y + ball_y_speed * estimated_time
            if predicted_y < right_paddle.y + paddle_height_right // 2:
                if right_paddle.y > 0:
                    right_paddle.y -= paddle_speed_right
            elif predicted_y > right_paddle.y + paddle_height_right // 2:
                if right_paddle.y < window_height - paddle_height_right:
                    right_paddle.y += paddle_speed_right
        else:
            # React to the ball's current position if the ball is moving away
            if ball.y < right_paddle.y + paddle_height_right // 2:
                if right_paddle.y > 0:
                    right_paddle.y -= paddle_speed_right
            elif ball.y > right_paddle.y + paddle_height_right // 2:
                if right_paddle.y < window_height - paddle_height_right:
                    right_paddle.y += paddle_speed_right
    elif difficulty_level == 5:
        # Expert difficulty: The CPU paddle actively attempts shots to challenge the player
        if ball_x_speed > 0:
            # Predict the ball's position based on the estimated time of arrival
            estimated_time = (right_paddle.x - ball.x) // ball_x_speed
            predicted_y = ball.y + ball_y_speed * estimated_time
            if predicted_y < right_paddle.y + paddle_height_right // 2:
                if right_paddle.y > 0:
                    right_paddle.y -= paddle_speed_right
            elif predicted_y > right_paddle.y + paddle_height_right // 2:
                if right_paddle.y < window_height - paddle_height_right:
                    right_paddle.y += paddle_speed_right
        else:
            # Move the paddle to perform shots that challenge the player
            if right_paddle.y + paddle_height_right // 2 < window_height // 2:
                if right_paddle.y < window_height - paddle_height_right:
                    right_paddle.y += paddle_speed_right
            elif right_paddle.y + paddle_height_right // 2 > window_height // 2:
                if right_paddle.y > 0:
                    right_paddle.y -= paddle_speed_right
    elif difficulty_level == 6:
        # Impossible difficulty: The CPU paddle never misses the ball.
        if ball.y < right_paddle.y + paddle_height_right // 2:
            if right_paddle.y > 0:
                right_paddle.y -= paddle_speed_right
        elif ball.y > right_paddle.y + paddle_height_right // 2:
            if right_paddle.y < window_height - paddle_height_right:
                right_paddle.y += paddle_speed_right


def run_tutorial():  # run the tutorial program
    tutorial_steps = [
        "Welcome to the " + program_name + " Tutorial! Press Enter or Space to proceed.",
        "Objective: Use your paddle to hit the ball past your opponent.",
        "You must not allow your opponent to get the ball past you.",
        "Controls: Player 1 uses 'W' and 'S' keys to move the left paddle.",
        "Player 2 controls the right paddle using the up and down arrows.",
        "In Local Multiplayer, you can use both paddles locally to facilitate two players on one device",
        "In Direct Connect, the Host is Player 1 and the person joining is Player 2.",
        "In Online Play you will be informed if you are currently Player 1 or 2.",
        "In VS CPU, you will be Player 1 and the CPU will be Player 2.",
        "While in a match you can press M to change song.",
        "Step 1: Move your paddle to intercept the ball.",
        "Step 2: The ball will bounce off the paddles and walls.",
        "Step 3: Try to hit the ball past your opponent's paddle to score a point.",
        "Press Enter or Space to return to the menu."
    ]

    current_step = 0
    font = pygame.font.Font(None, options_font_size)

    while True:
        window.fill(bgColor)
        text = font.render(tutorial_steps[current_step], True, textColor)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(text, text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                safe_exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_SPACE:
                    current_step += 1
                    if current_step >= len(tutorial_steps):
                        global showMenu, difficulty_level
                        difficulty_level = 2
                        showMenu = True
                        return


def main():  # Define main
    # Define global variables
    global showMenu, paused, game_mode, is_host, inGame, left_paddle, game_state, right_paddle, ball, ball_x_speed, \
        ball_y_speed, current_song, player1_score, player2_score
    while True:
        while showMenu:  # Contain the menu screen
            font_title = pygame.font.Font(None, title_font_size)
            font_options = pygame.font.Font(None, options_font_size)
            title_text = font_title.render(program_name, True, textColor)
            option_texts = [
                font_options.render("1. Local Multiplayer", True, textColor),
                font_options.render("2. VS CPU", True, textColor),
                font_options.render("3. Host Direct Connect", True, textColor),
                font_options.render("4. Join", True, textColor),
                font_options.render("5. Tutorial", True, textColor),
                font_options.render("Enter your choice (1-5): ", True, textColor)
            ]
            title_pos = title_text.get_rect(center=(window_width // 2, 50))
            option_positions = []
            for i, option_text in enumerate(option_texts):
                option_pos = option_text.get_rect(
                    center=(window_width // 2, 100 + i * 30)
                )
                option_positions.append(option_pos)
            window.fill(bgColor)
            window.blit(title_text, title_pos)
            for option_text, option_pos in zip(option_texts, option_positions):
                window.blit(option_text, option_pos)
            pygame.display.flip()
            valid_options = ["1", "2", "3", "4", "5"]
            selected_option = None
            while not selected_option:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        safe_exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.unicode in valid_options:
                            selected_option = event.unicode
                        else:
                            font = pygame.font.Font(None, options_font_size)
                            error_text = font.render("Invalid option. Please enter a valid option.", True, errorColor)
                            error_rect = error_text.get_rect(center=(window_width // 2, 400))
                            window.blit(error_text, error_rect)
                            pygame.display.flip()
                        if selected_option == "1":
                            game_mode = "local_multiplayer"
                            showMenu = False
                        elif selected_option == "2":
                            game_mode = "vs_cpu"
                            showMenu = False
                        elif selected_option == "3":
                            game_mode = "online"
                            is_host = True
                            showMenu = False
                        elif selected_option == "4":
                            game_mode = "online"
                            is_host = False
                            showMenu = False
                        elif selected_option == "5":
                            game_mode = "tutorial"
                            showMenu = False
                        else:
                            print("Error: Invalid input passed to examiner. (This shouldn't happen.)")
                            safe_exit()
        if game_mode == "vs_cpu":
            font = pygame.font.Font(None, 36)
            window.fill(bgColor)
            option_texts = [
                "Easy - The CPU paddle follows the ball with random delay (3 to 10 seconds)",
                "Medium - The CPU paddle tracks the ball with some delay.",
                "Hard - The CPU paddle tracks the ball accurately.",
                "Advanced - The CPU paddle predicts the ball's movement.",
                "Expert - The CPU paddle actively attempts shots to challenge the player.",
                "Impossible - The CPU paddle took six adderall about an hour ago.",
            ]
            text_y = 100
            for i, option_texts in enumerate(option_texts):
                text = font.render(f"{i + 1}. {option_texts}", True, textColor)
                text_rect = text.get_rect(center=(window_width // 2, text_y))
                window.blit(text, text_rect)
                text_y += 50
            title_text = font.render("Select Difficulty Level:", True, textColor)
            title_rect = title_text.get_rect(center=(window_width // 2, 50))
            window.blit(title_text, title_rect)
            pygame.display.flip()
            valid_options = ["1", "2", "3", "4", "5", "6"]
            selected_option = None
            while not selected_option:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        safe_exit()
                    if event.type == KEYDOWN:
                        if event.unicode in valid_options:
                            global difficulty_level
                            selected_option = event.unicode
                            difficulty_level = int(selected_option)
                            if difficulty_level < 1 or difficulty_level > 6:
                                print("Invalid difficulty level stored, unable to proceed.")
                                safe_exit()
                            else:
                                global inGame
                                inGame = True
                        else:
                            error_text = font.render("Invalid option. Please enter a valid option.", True, errorColor)
                            error_rect = error_text.get_rect(center=(window_width // 2, 400))
                            window.blit(error_text, error_rect)
                            pygame.display.flip()
        elif game_mode == "online" and is_host:
            font = pygame.font.Font(None, options_font_size)
            title_text = font.render("Server Hosting Options:", True, textColor)
            title_rect = title_text.get_rect(center=(window_width // 2, 50))
            window.blit(title_text, title_rect)
            host_text = font.render("Server will be hosted on: ", True, textColor)
            host_rect = host_text.get_rect(center=(window_width // 2, 150))
            window.blit(host_text, host_rect)
            lan_ip_text = font.render(lan_IP, True, textColor)
            lan_ip_rect = lan_ip_text.get_rect(center=(window_width // 2, 200))
            window.blit(lan_ip_text, lan_ip_rect)
            port_text = font.render("Enter the port to host the server on (1-65535):", True, textColor)
            port_rect = port_text.get_rect(center=(window_width // 2, 300))
            window.blit(port_text, port_rect)
            pygame.display.flip()
            valid_input = False
            port_choice = ""
            while not valid_input:
                global PORT
                for event in pygame.event.get():
                    if event.type == QUIT:
                        safe_exit()
                    if event.type == KEYDOWN:
                        if event.unicode.isdigit():
                            port_choice += event.unicode
                        elif event.key == K_BACKSPACE:
                            port_choice = port_choice[:-1]
                        elif event.key == K_RETURN:
                            if port_choice.isdigit() and 1 <= int(port_choice) <= 65535:
                                valid_input = True
                        window.fill(bgColor)
                        window.blit(title_text, title_rect)
                        window.blit(host_text, host_rect)
                        window.blit(lan_ip_text, lan_ip_rect)
                        window.blit(port_text, port_rect)
                        input_text = font.render(port_choice, True, textColor)
                        input_rect = input_text.get_rect(center=(window_width // 2, 400))
                        window.blit(input_text, input_rect)
                        if not valid_input:
                            error_text = font.render("Invalid port number. Please enter a valid port (1-65535).", True,
                                                     textColor)
                            error_rect = error_text.get_rect(center=(window_width // 2, 500))
                            window.blit(error_text, error_rect)
                        pygame.display.flip()
            PORT = int(port_choice)
            start_server()
            listen_thread = threading.Thread(target=listen_for_clients)
            listen_thread.start()
            print("Waiting for client to connect...")
            font = pygame.font.Font(None, options_font_size)
            text = "Waiting for client to connect..."
            text_rendered = font.render(text, True, textColor)
            text_width = text_rendered.get_width()
            text_height = text_rendered.get_height()
            text_x = (window_width - text_width) // 2
            text_y = (window_height - text_height) // 2
            window.fill(bgColor)
            window.blit(text_rendered, (text_x, text_y))
            pygame.display.flip()
            listen_thread.join()
            print("Client connected!")
            text = "Client connected!"
            text_rendered = font.render(text, True, textColor)
            text_width = text_rendered.get_width()
            text_height = text_rendered.get_height()
            text_x = (window_width - text_width) // 2
            text_y = (window_height - text_height) // 2
            window.fill(bgColor)
            window.blit(text_rendered, (text_x, text_y))
            pygame.display.flip()
        elif game_mode == "online" and not is_host:
            font = pygame.font.Font(None, options_font_size)
            title_text = font.render("Server Connection Options:", True, textColor)
            title_rect = title_text.get_rect(center=(window_width // 2, 50))
            window.blit(title_text, title_rect)
            server_ip_text = font.render("Enter the server IP address:", True, textColor)
            server_ip_rect = server_ip_text.get_rect(center=(window_width // 2, 150))
            window.blit(server_ip_text, server_ip_rect)
            port_text = font.render("Enter the port of the server (1-65535):", True, textColor)
            port_rect = port_text.get_rect(center=(window_width // 2, 250))
            window.blit(port_text, port_rect)
            pygame.display.flip()
            valid_input = False
            server_ip = ""
            port_choice = ""
            while not valid_input:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        safe_exit()
                    if event.type == KEYDOWN:
                        if event.unicode.isdigit():
                            if len(server_ip) < 15:
                                server_ip += event.unicode
                        elif event.key == K_BACKSPACE:
                            server_ip = server_ip[:-1]
                        elif event.key == K_RETURN:
                            try:
                                ipaddress.IPv4Address(server_ip)
                                if port_choice.isdigit() and 1 <= int(port_choice) <= 65535:
                                    valid_input = True
                            except ipaddress.AddressValueError:
                                pass
                        elif event.key == K_PERIOD:
                            if len(server_ip) < 15:
                                server_ip += "."
                        elif event.key == K_COLON:
                            if not port_choice:
                                port_choice += ":"
                        elif event.key == K_MINUS:
                            if not port_choice:
                                port_choice += "-"
                        elif event.key == K_UNDERSCORE:
                            if not port_choice:
                                port_choice += "_"
                        elif event.key == K_BACKSLASH:
                            if not port_choice:
                                port_choice += "\\"
                        window.fill(bgColor)
                        window.blit(title_text, title_rect)
                        window.blit(server_ip_text, server_ip_rect)
                        window.blit(port_text, port_rect)
                        input_ip_text = font.render(server_ip, True, textColor)
                        input_ip_rect = input_ip_text.get_rect(center=(window_width // 2, 350))
                        window.blit(input_ip_text, input_ip_rect)
                        input_port_text = font.render(port_choice, True, textColor)
                        input_port_rect = input_port_text.get_rect(center=(window_width // 2, 450))
                        window.blit(input_port_text, input_port_rect)
                        if not valid_input:
                            error_text = font.render("Invalid server IP address or port number.", True, errorColor)
                            error_rect = error_text.get_rect(center=(window_width // 2, 550))
                            window.blit(error_text, error_rect)
                        pygame.display.flip()
            PORT = int(port_choice)
            join_server(server_ip, PORT)
        elif game_mode == "tutorial":
            run_tutorial()
            difficulty_level = 1
            inGame = True
        elif game_mode == "local_multiplayer":
            print("Starting local multiplayer match")
            inGame = True
        else:
            print("Invalid input passed to game mode interpreter. Crashing.")
            safe_exit()
        while inGame:
            for event in pygame.event.get():
                if event.type == QUIT:
                    safe_exit()
                elif event.type == KEYDOWN:
                    if event.key == K_p and game_mode != "online":
                        paused = not paused  # Toggle pause state when 'P' key is pressed
                    if event.key == pygame.K_m:
                        fade_thread = threading.Thread(target=fade_out_song)
                        fade_thread.start()
                        change_song()
                        play_thread = threading.Thread(target=load_and_play_song)
                        play_thread.start()
            # Check if the current song has finished playing
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(fade_duration)
                change_song()
                play_thread = threading.Thread(target=load_and_play_song)
                play_thread.start()
            if not paused:  # Only update game logic if the game is not paused
                keys = pygame.key.get_pressed()
                # Move the paddles (Player 1 controls)
                if game_mode != "online" or (game_mode == "online" and is_host):
                    if keys[K_w] and left_paddle.y > 0:
                        left_paddle.y -= paddle_speed_left
                        game_state["left_paddle"] = left_paddle
                        if game_mode == "online":
                            send_data(game_state)
                    if keys[K_s] and left_paddle.y < window_height - paddle_height_left:
                        left_paddle.y += paddle_speed_left
                        game_state["left_paddle"] = left_paddle
                        if game_mode == "online":
                            send_data(game_state)
                if game_mode == "local_multiplayer" or (game_mode == "online" and not is_host):
                    # Move the paddles (Player 2 controls)
                    if keys[K_UP] and right_paddle.y > 0:
                        right_paddle.y -= paddle_speed_right
                        game_state["right_paddle"] = right_paddle
                        if game_mode == "online":
                            send_data(game_state)  # send updated game_state to server
                    if keys[K_DOWN] and right_paddle.y < window_height - paddle_height_right:
                        right_paddle.y += paddle_speed_right
                        game_state["right_paddle"] = right_paddle
                        if game_mode == "online":
                            send_data(game_state)  # send updated game_state to server
                elif game_mode == "vs_cpu" or "tutorial":
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
                if ball.x < 0: # if ball goes past left wall
                    player2_score += 1
                    reset_game()
                elif ball.x > window_width: # if ball goes past right wall
                    player1_score += 1
                    reset_game()
                # Synchronize game state
                game_state["left_paddle"] = left_paddle
                game_state["right_paddle"] = right_paddle
                game_state["ball"] = ball
                if is_host and game_mode == "online":
                    send_data(game_state)
                if game_mode == "online":
                    try:
                        if is_host:
                            received_data = non_blocking_receive(hostdc_socket)
                        else:
                            received_data = non_blocking_receive(client_socket)
                        if received_data:
                            game_state = pickle.loads(received_data)
                            left_paddle = game_state["left_paddle"]
                            right_paddle = game_state["right_paddle"]
                            ball = game_state["ball"]
                    except socket.error as e:
                        print("Socket error:", e)
                        break
                # Draw the game objects
                window.fill(bgColor)
                pygame.draw.rect(window, textColor, left_paddle)
                pygame.draw.rect(window, textColor, right_paddle)
                pygame.draw.ellipse(window, textColor, ball)
                pygame.draw.aaline(window, textColor, (window_width // 2, 0), (window_width // 2, window_height))
                # Draw player scores
                score_font = pygame.font.Font(None, score_font_size)  # Score font
                player1_score_text = score_font.render(str(player1_score), True, textColor)  # Render player 1 score
                player2_score_text = score_font.render(str(player2_score), True, textColor)  # Render player 2 score
                # Position of player scores
                player1_score_pos = (20, 20)  # Top left position
                player2_score_pos = (window_width - player2_score_text.get_width() - 20, 20)  # Top right position
                # Draw player scores on the screen
                window.blit(player1_score_text, player1_score_pos)
                window.blit(player2_score_text, player2_score_pos)
                # Draw pause message if the game is paused
                if paused:
                    font = pygame.font.Font(None, options_font_size)
                    text = font.render("Paused", True, textColor)
                    text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
                    window.blit(text, text_rect)
                # Update the display
                pygame.display.update()
                clock.tick(60)


main()

safe_exit()
