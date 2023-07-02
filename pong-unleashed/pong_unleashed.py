# Import libraries
import ipaddress
import os
import pygame
import socket
import pickle
from pygame.locals import *
import sys
import select
import random
# import time
import threading

"""
 PONG UNLEASHED!
 Thank you for downloading Pong Unleashed (I really hope this doesn't violate any copyrights)
 This is a project to bring Pong to the modern era, along with a series of other games I'd like
 to revitalize as part of the larger goal.
 And of course, thanks for enjoying the game :)
 Made by SlammingProgramming (https://github.com/slammingprogramming)
 Source is available on GitHub, this work is licensed under the GPLv3
 https://github.com/slammingprogramming/Pong-Unleashed
"""

pygame.init()  # Initialize pygame immediately, so we can do some set up using it
debug = True  # Debug output to terminal

"""
Variables
"""
if debug:
    print("Initializing variables...")

# Global declarations
global showMenu, inGame, game_mode, paused, music_volume, current_song, player1_score, player2_score, win_type, \
    game_over, splash_bg, player1_rounds_won, player2_rounds_won, reaction_time
"""
Settings
"""
if debug:
    print("Loading settings...")
# Program vars
version_number = "0.3.0"
program_name = "Pong Unleashed v" + version_number
skin = "default"  # The name of your skin which will be placed in the resources folder with a unique name with
# your resources inside

# Window vars
window_width = 960
window_height = 720
splash_bg = pygame.image.load('resources/' + skin + '/images/splash.jpg')

# Font vars
title_font_size = 36
options_font_size = 24
winner_text_size = 72
score_font_size = 18

# Color vars
bgColor = pygame.Color(0, 0, 0)
textColor = pygame.Color(255, 255, 255)
errorColor = pygame.Color(255, 0, 0)

# Sound vars
music_directory = "resources/" + skin + "/music"  # Set the directory path
music_volume = 0.5  # valid options: 0.0 to 1
fade_duration = 2000  # in milliseconds
sound_volume = 1  # valid options: 0.0 to 1

# Networking vars
packet_size = 4096  # Sets the packet size in bytes for network communication
socket_timeout = 0.01

# Player 1 paddle vars
paddle_width_left = 10
paddle_height_left = 60
paddle_speed_left = 1
paddle_friction_left = 0.5
paddle_max_velocity_left = 12

# Player 2 paddle vars
paddle_width_right = 10
paddle_height_right = 60
paddle_speed_right = 1
paddle_friction_right = 0.5
paddle_max_velocity_right = 12

# Ball vars
ball_radius = 10
ball_x_speed = random.randint(4, 10)
ball_y_speed = random.randint(4, 10)

# Scoring & Win Condition vars
score_threshold = 5
win_type = "score_threshold"

# Set up networking
lan_IP = socket.gethostbyname(socket.gethostname())  # Get the IP of the device on the LAN
connection_ip = None  # Stores the IP we are connect(ing/ed) to
PORT = 12345  # Sets the port for connections

"""
Soundsystem Functions
"""


# Function to fade out the current song
def fade_out_song():
    if debug:
        print("Fading out song...")
    for vol in range(int(music_volume * 100), 0, -1):
        pygame.mixer.music.set_volume(vol / 100)
        pygame.time.delay(int(fade_duration / (music_volume * 100)))


# Function to select a new song from the playlist that is different from the current song
def change_song():
    if debug:
        print("Changing song...")
    global current_song
    # Select a new song from the playlist that is different from the current song
    new_song = random.choice(playlist)
    while new_song == current_song:
        new_song = random.choice(playlist)
    current_song = new_song


# Function to load and play the new song and set it to the desired volume level
def load_and_play_song():
    if debug:
        print("Loading and playing song...")
    pygame.mixer.music.load(current_song)
    pygame.mixer.music.set_volume(0)
    for vol in range(int(music_volume * 100)):
        pygame.mixer.music.set_volume(vol / 100)
        pygame.time.delay(int(fade_duration / (music_volume * 100)))
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(0)


def check_music():  # Check if music is still playing and play the next song if it isn't
    # Check if the current song has finished playing and play next if it has
    if not pygame.mixer.music.get_busy():
        if debug:
            print("Music is not playing anymore, changing the song...")
        pygame.mixer.music.fadeout(fade_duration)
        change_song()
        play_thread = threading.Thread(target=load_and_play_song)
        play_thread.start()


"""
Initialization & Exit Functions
"""


def init_bootstrap():  # Anything we want to run first goes here
    if debug:
        print("Initializing bootstrap...")
    global showMenu, inGame, game_mode, paused, current_song, server_socket, client_socket, hostdc_socket, is_host, \
        clock, game_over, player1_score, player2_score, player1_rounds_won, player2_rounds_won, right_paddle_y_speed, \
        left_paddle_y_speed, reaction_time, reaction_time_input
    pygame.init()
    clock = pygame.time.Clock()
    # Init vars
    showMenu = True
    inGame = False
    game_mode = None
    paused = False
    current_song = ""
    server_socket = None  # Dedicated server communication socket, also used to initiate Direct Connect sessions
    client_socket = None  # Direct Connect client communication socket
    hostdc_socket = None  # Direct Connect host communication socket
    is_host = None  # Stores if we are the host in a Direct Connect session
    game_over = False
    player1_score = 0
    player2_score = 0
    player1_rounds_won = 0
    player2_rounds_won = 0
    left_paddle_y_speed = 0
    right_paddle_y_speed = 0
    reaction_time = None


def init_window():  # Initialize window, display splash
    if debug:
        print("Initializing window...")
    global window, clock
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(program_name)


def init_soundsystem():
    if debug:
        print("Initializing soundsystem...")
    global paddle_hit_sound, ball_collision_sound, menu_select_sound, win_sound, lose_sound, reset_sound, playlist, current_song
    # Load sounds
    if debug:
        print("Loading sounds...")
    paddle_hit_sound = pygame.mixer.Sound("resources/" + skin + '/sounds/paddle_hit.wav')
    ball_collision_sound = pygame.mixer.Sound("resources/" + skin + '/sounds/ball_collision.wav')
    menu_select_sound = pygame.mixer.Sound("resources/" + skin + '/sounds/menu_select.wav')
    win_sound = pygame.mixer.Sound("resources/" + skin + '/sounds/win_sound.wav')
    lose_sound = pygame.mixer.Sound("resources/" + skin + '/sounds/lose_sound.wav')
    reset_sound = pygame.mixer.Sound("resources/" + skin + '/sounds/menu_select.wav')

    # Create a playlist of songs in the 'music' directory and set title screen music as current song
    playlist = []

    supported_sound_formats = ["WAV", "MP3", "OGG", "MIDI"]  # Set the supported file extensions for the sound system
    if debug:
        print("Loading music directory...")
    # Iterate over all files in the directory
    for filename in os.listdir(music_directory):
        if any(filename.lower().endswith(formats_allowed.lower()) for formats_allowed in supported_sound_formats):
            # Construct the relative file path and add it to the playlist
            file_path = os.path.join(music_directory, filename)
            if debug:
                print(file_path)
            playlist.append(file_path)

    # Set volume of sounds to the set level
    if debug:
        print("Setting volumes...")
    paddle_hit_sound.set_volume(sound_volume)
    ball_collision_sound.set_volume(sound_volume)
    menu_select_sound.set_volume(sound_volume)
    lose_sound.set_volume(sound_volume)
    win_sound.set_volume(sound_volume)


def init_networking():
    if debug:
        print("Initializing networking...")
    global game_state
    """
    # Set up game state synchronization table, this is all the data that will be sent to/from the server for sync.
    game_state = {
        "left_paddle": left_paddle,
        "right_paddle": right_paddle,
        "ball": ball
    }
    """


def load_title_screen():  # Load and play title screen music and background
    if debug:
        print("Loading title screen...")
    global window, splash_bg, current_song
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(program_name)
    splash_bg = pygame.transform.scale(splash_bg, (window_width, window_height))
    window.blit(splash_bg, (0, 0))
    change_song()
    load_and_play_song()
    reset_game()


def safe_exit():  # safely exit the game and ensure all sockets are closed and servers shut down
    if debug:
        print("Exiting safely!")
        if is_host and game_mode == "online":
            print("Shutting down hosted online game.")
        elif not is_host and game_mode == "online":
            print("Shutting down online game client")
        else:
            print("Shutting down offline game.")
    if is_host and game_mode == "online":
        server_socket.close()
        hostdc_socket.close()
    elif not is_host and game_mode == "online":
        client_socket.close()
    pygame.quit()
    sys.exit(0)


"""
Gameplay Functions
"""


def reset_game():  # reset the match on screen
    if debug:
        print("Resetting game...")
    global left_paddle, right_paddle, ball, ball_x_speed, ball_y_speed, paused, left_paddle_y_speed, \
        right_paddle_y_speed
    left_paddle = pygame.Rect(50, window_height // 2 - paddle_height_left // 2, paddle_width_left, paddle_height_left)
    right_paddle = pygame.Rect(window_width - 50 - paddle_width_right, window_height // 2 - paddle_height_right // 2,
                               paddle_width_right, paddle_height_right)
    ball = pygame.Rect(window_width // 2 - ball_radius // 2, window_height // 2 - ball_radius // 2, ball_radius,
                       ball_radius)
    ball_x_speed = random.randint(4, 10)
    ball_y_speed = random.randint(4, 10)
    left_paddle_y_speed = 0
    right_paddle_y_speed = 0
    directionality = random.randint(0, 3)  # Send the ball in one of four directions depending on the results of a
    # random number roll
    if directionality == 0:  # +/+
        ball_x_speed = ball_x_speed * 1
        ball_y_speed = ball_y_speed * 1
    elif directionality == 1:  # +/-
        ball_x_speed = ball_x_speed * 1
        ball_y_speed = ball_y_speed * -1
    elif directionality == 2:  # -/+
        ball_x_speed = ball_x_speed * -1
        ball_y_speed = ball_y_speed * 1
    elif directionality == 3:  # -/-
        ball_x_speed = ball_x_speed * -1
        ball_y_speed = ball_y_speed * -1
    reset_sound.play()
    paused = False


def reset_scoring():  # Reset scoring system as needed (i.e. on return to Title Screen)
    if debug:
        print("Resetting scoring...")
    global player1_score, player2_score, player1_rounds_won, player2_rounds_won
    player1_score = 0
    player2_score = 0
    player1_rounds_won = 0
    player2_rounds_won = 0


def move_paddle(paddle, key_events=None, acceleration=0, max_velocity=0, friction=0, desired_move=None):
    global left_paddle_y_speed, right_paddle_y_speed
    if paddle == left_paddle:
        if debug:
            print(f"Moving left paddle...")
        velocity = left_paddle_y_speed
    else:
        if debug:
            print(f"Moving right paddle...")
        velocity = right_paddle_y_speed

    if isinstance(key_events, dict) and desired_move is not None:
        w_pressed = key_events.get(K_w, False)
        s_pressed = key_events.get(K_s, False)
        key_events = {K_w: w_pressed, K_s: s_pressed}
        key_events[K_w] = desired_move == "up"
        key_events[K_s] = desired_move == "down"

    if key_events is None:
        # No key events, move paddle based on current velocity
        if velocity > 0:
            velocity = max(0, velocity - friction)
        elif velocity < 0:
            velocity = min(0, velocity + friction)
    elif isinstance(key_events, dict) and key_events.get(K_w, False) and paddle.top > 0:
        # Key event for moving up
        velocity -= acceleration
        velocity = max(velocity, -max_velocity)
    elif isinstance(key_events, dict) and key_events.get(K_s, False) and paddle.bottom < window_height:
        # Key event for moving down
        velocity += acceleration
        velocity = min(velocity, max_velocity)

    paddle.y += velocity
    paddle.y = max(0, min(paddle.y, window_height - paddle.height))

    # Reset velocity to 0 if paddle hits the top or bottom wall
    if paddle.y == 0 or paddle.y == window_height - paddle.height:
        velocity = 0

    if paddle == left_paddle:
        left_paddle_y_speed = velocity
    elif paddle == right_paddle:
        right_paddle_y_speed = velocity

    return paddle


def cpu_paddle_move(paddle, reaction_time, desired_move):
    if debug:
        print(f"CPU paddle movement - Paddle: {paddle}, Reaction Time: {reaction_time}, Desired Move: {desired_move}")
    pygame.time.wait(int(reaction_time * 1000))
    key_events = {}  # Create an empty dictionary for key events
    acceleration = paddle_speed_right
    max_velocity = paddle_max_velocity_right
    friction = paddle_friction_right

    move_paddle(paddle, key_events, acceleration, max_velocity, friction, desired_move)


# Move the CPU paddle based on difficulty level
def move_cpu_paddle(difficulty_level):
    global reaction_time
    if reaction_time is None or reaction_time == 0:
        reaction_time = 0.0
    if debug:
        print(f"AI moving CPU paddle - Difficulty Level: {difficulty_level}")
    if difficulty_level == 1:
        # Easy difficulty: The CPU paddle will follow the ball but with a player-set reaction time delay, making it easier
        # for the player to hit the ball.
        if ball.y < right_paddle.y:
            # If the ball's y-coordinate is less than the right paddle's y-coordinate
            cpu_paddle_thread = threading.Thread(target=cpu_paddle_move,
                                                 args=(right_paddle, reaction_time, "up"))
            cpu_paddle_thread.start()

        elif ball.y > right_paddle.y + paddle_height_right:
            # If the ball's y-coordinate is greater than the sum of the right paddle's y-coordinate
            # and its height (ball is below the paddle)
            cpu_paddle_thread = threading.Thread(target=cpu_paddle_move,
                                                 args=(right_paddle, reaction_time, "down"))
            cpu_paddle_thread.start()

    elif difficulty_level == 2:
        # Medium difficulty: The CPU paddle follows the ball with a reaction time of 1-3 seconds.
        def update_paddle_position():
            if ball.y < right_paddle.y:
                # If the ball's y-coordinate is less than the right paddle's y-coordinate
                if right_paddle.y > 0:
                    # If the right paddle's y-coordinate is greater than 0 (not at the top edge)
                    cpu_paddle_thread = threading.Thread(target=cpu_paddle_move,
                                                         args=(right_paddle, reaction_time, "up"))
                    cpu_paddle_thread.start()

            elif ball.y > right_paddle.y + paddle_height_right:
                # If the ball's y-coordinate is greater than the sum of the right paddle's y-coordinate
                # and its height (ball is below the paddle)
                if right_paddle.y < window_height - paddle_height_right:
                    # If the right paddle's y-coordinate is less than the window height minus paddle height
                    # (not at the bottom edge)
                    cpu_paddle_thread = threading.Thread(target=cpu_paddle_move,
                                                         args=(right_paddle, reaction_time, "down"))
                    cpu_paddle_thread.start()

    elif difficulty_level == 3:
        # Hard difficulty: The CPU paddle tries to predict the ball's position with a reaction time of 0-2 seconds
        if ball_x_speed > 0:
            # Predict the ball's position based on the estimated time of arrival
            estimated_time = (right_paddle.x - ball.x) // ball_x_speed
            predicted_y = ball.y + ball_y_speed * estimated_time

            if predicted_y < right_paddle.y + (paddle_height_right // 2):
                # If the predicted y-coordinate is less than the middle point of the paddle
                cpu_paddle_thread = threading.Thread(target=cpu_paddle_move,
                                                     args=(right_paddle, reaction_time, "up"))
                cpu_paddle_thread.start()

            elif predicted_y > right_paddle.y + paddle_height_right // 2:
                # If the predicted y-coordinate is greater than the middle point of the paddle
                cpu_paddle_thread = threading.Thread(target=cpu_paddle_move,
                                                     args=(right_paddle, reaction_time, "down"))
                cpu_paddle_thread.start()

        else:
            # React to the ball's current position if the ball is moving away
            if ball.y < right_paddle.y + paddle_height_right // 2:
                # If the ball's y-coordinate is less than the middle point of the paddle
                cpu_paddle_thread = threading.Thread(target=cpu_paddle_move,
                                                     args=(right_paddle, reaction_time, "down"))
                cpu_paddle_thread.start()

            elif ball.y > right_paddle.y + paddle_height_right // 2:
                # If the ball's y-coordinate is greater than the middle point of the paddle
                cpu_paddle_thread = threading.Thread(target=cpu_paddle_move,
                                                     args=(right_paddle, reaction_time, "up"))
                cpu_paddle_thread.start()
    elif difficulty_level == 4:
        # Advanced difficulty: The CPU paddle prediction is improved and tracks the ball with a delay of 0-2 seconds.

        if ball_x_speed > 0:
            # Predict the ball's position based on the estimated time of arrival, factoring in wall bounces
            estimated_time = (right_paddle.x - ball.x) // ball_x_speed
            predicted_y = ball.y + ball_y_speed * estimated_time

            # Adjust the predicted y-coordinate based on wall bounces
            remaining_bounces = estimated_time // (window_height - 2 * ball_radius)
            if remaining_bounces % 2 == 1:
                predicted_y = window_height - predicted_y

            if predicted_y < right_paddle.y + paddle_height_right // 2:
                # If the predicted y-coordinate is less than the middle point of the paddle
                desired_move = "up"
            elif predicted_y > right_paddle.y + paddle_height_right // 2:
                # If the predicted y-coordinate is greater than the middle point of the paddle
                desired_move = "down"
            else:
                desired_move = None

        else:
            # React to the ball's current position if the ball is moving away
            if ball.y < right_paddle.y + paddle_height_right // 2:
                # If the ball's y-coordinate is less than the middle point of the paddle
                desired_move = "up"
            elif ball.y > right_paddle.y + paddle_height_right // 2:
                # If the ball's y-coordinate is greater than the middle point of the paddle
                desired_move = "down"
            else:
                desired_move = None

        # Move the paddle using the modified move_paddle function
        move_paddle(right_paddle, {}, paddle_speed_right, paddle_max_velocity_right, paddle_friction_right,
                    desired_move)
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
    if debug:
        print("Running tutorial program...")
    global showMenu
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
        check_music()
        window.blit(splash_bg, (0, 0))
        text = font.render(tutorial_steps[current_step], True, textColor)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(text, text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                safe_exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_SPACE:
                    if debug:
                        print("Pressed key to move forward in tutorial.")
                    menu_select_sound.play()
                    current_step += 1
                    if current_step >= len(tutorial_steps):
                        global difficulty_level, inGame
                        difficulty_level = 2
                        inGame = True
                        showMenu = False
                        return
                    # needs fixed so you can get back to the menu if you press esc
                elif event.key == K_ESCAPE:
                    if debug:
                        print("Pressed key to move back in tutorial or exit to menu.")
                    menu_select_sound.play()
                    if current_step > 0:
                        current_step -= 1
                    if current_step == 0:
                        showMenu = True
                        inGame = False
                        return


"""
Networking Functions
"""


def start_server():  # Start a server on the local device to host a direct connect session
    if debug:
        print("Starting server...")
    global server_socket, is_host
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((lan_IP, PORT))
    server_socket.listen(1)
    is_host = True


def listen_for_clients():  # Once the  direct connect server is running, listen for an incoming connection.
    if debug:
        print("Listening for clients...")
    global hostdc_socket
    hostdc_socket, client_address = server_socket.accept()


def join_server(connection_ip, PORT):  # Join a server or direct connect
    if debug:
        print("Joining server...")
    global client_socket, is_host
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((connection_ip, PORT))
    is_host = False


def send_data(data):  # Send data to the client(if hosting direct connect), or to the server/host.
    if is_host:
        if debug:
            print("Sending data as host...")
        hostdc_socket.sendall(pickle.dumps(data))
    else:
        if debug:
            print("Sending data as client...")
        client_socket.sendall(pickle.dumps(data))


def receive_data():  # Receive data from the client(if hosting direct connect), or to the server/host.
    if is_host:
        if debug:
            print("Receiving data as host...")
        data = hostdc_socket.recv(packet_size)
    else:
        if debug:
            print("Receiving data as client...")
        data = client_socket.recv(packet_size)
    return pickle.loads(data)


def non_blocking_receive(socket_obj):
    if debug:
        print("non_blocking_receive doing work...")
    ready = select.select([socket_obj], [], [], socket_timeout)
    if ready[0]:
        return socket_obj.recv(packet_size)
    else:
        return None


"""
MAIN PROGRAM
"""


def main():  # Define main
    if debug:
        print("Start of main program execution")
    # Define global variables
    global showMenu, paused, game_mode, is_host, inGame, left_paddle, game_state, right_paddle, ball, ball_x_speed, \
        ball_y_speed, current_song, player1_score, player2_score, winner_text, game_over
    # Initialize the game
    init_bootstrap()
    init_soundsystem()
    init_window()
    init_networking()
    while True:
        check_music()
        while showMenu:  # Contain the menu screen
            if debug:
                print("Showing menu...")
            check_music()
            reset_scoring()
            load_title_screen()
            if game_over:  # Check if there is a game over condition and display on screen if there is
                if debug:
                    print("Showing game over screen...")
                window.blit(splash_bg, (0, 0))
                winner_font = pygame.font.Font(None, winner_text_size)
                winner_text_rendered = winner_font.render(winner_text, True, textColor)
                winner_text_width = winner_text_rendered.get_width()
                winner_text_height = winner_text_rendered.get_height()
                window.blit(winner_text_rendered, (
                    window_width // 2 - winner_text_width // 2, window_height // 2 - winner_text_height // 2))
                pygame.display.flip()
                pygame.time.delay(5000)
                game_over = False
                load_title_screen()
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
            window.blit(splash_bg, (0, 0))
            window.blit(title_text, title_pos)
            for option_text, option_pos in zip(option_texts, option_positions):
                window.blit(option_text, option_pos)
            pygame.display.flip()
            valid_options = ["1", "2", "3", "4", "5"]
            selected_option = None
            while not selected_option:
                check_music()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        if debug:
                            print("Quit command issued while in menu.")
                        safe_exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.unicode in valid_options:
                            if debug:
                                print("Valid option was selected on main menu.")
                            menu_select_sound.play()
                            selected_option = event.unicode
                        elif event.key == K_ESCAPE:
                            if debug:
                                print("Quit game button was pressed while in menu.")
                            menu_select_sound.play()
                            safe_exit()
                        else:
                            if debug:
                                print("Invalid button was pressed on main menu.")
                            font = pygame.font.Font(None, options_font_size)
                            error_text = font.render("Invalid option. Please enter a valid option.", True, errorColor)
                            error_rect = error_text.get_rect(center=(window_width // 2, 400))
                            window.blit(error_text, error_rect)
                            pygame.display.flip()
                        if selected_option == "1":
                            if debug:
                                print("Local multiplayer selected.")
                            game_mode = "local_multiplayer"
                            showMenu = False
                            game_over = False
                        elif selected_option == "2":
                            if debug:
                                print("VS CPU Selected.")
                            game_mode = "vs_cpu"
                            showMenu = False
                            game_over = False
                        elif selected_option == "3":
                            if debug:
                                print("Host Direct Connect Selected.")
                            game_mode = "online"
                            is_host = True
                            showMenu = False
                            game_over = False
                        elif selected_option == "4":
                            if debug:
                                print("Join Server Selected.")
                            game_mode = "online"
                            is_host = False
                            showMenu = False
                            game_over = False
                        elif selected_option == "5":
                            if debug:
                                print("Tutorial Selected.")
                            game_mode = "tutorial"
                            showMenu = False
                            game_over = False
        if game_mode == "vs_cpu":
            if debug:
                print("Asking for difficulty setting...")
            font = pygame.font.Font(None, options_font_size)
            window.blit(splash_bg, (0, 0))
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
                check_music()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        if debug:
                            print("Quit command received while on difficulty select screen.")
                        safe_exit()
                    if event.type == KEYDOWN:
                        if event.unicode in valid_options:
                            if debug:
                                print("Valid option selected.")
                            global difficulty_level
                            menu_select_sound.play()
                            selected_option = event.unicode
                            difficulty_level = int(selected_option)
                            if difficulty_level < 1 or difficulty_level > 6:
                                if debug:
                                    print("Invalid difficulty_level stored. This shouldn't happen.")
                                print("Invalid difficulty level stored, unable to proceed.")
                                safe_exit()
                            else:
                                if debug:
                                    print("Difficulty level check returns valid.")
                                global inGame
                                game_over = False
                                inGame = True
                        elif event.key == K_ESCAPE:  # needs fixed so you can go back
                            if debug:
                                print("Key to return to menu pressed.")
                            menu_select_sound.play()
                            showMenu = True
                            inGame = False
                            return
                        else:
                            if debug:
                                print("Invalid option selected.")
                            error_text = font.render("Invalid option. Please enter a valid option.", True, errorColor)
                            error_rect = error_text.get_rect(center=(window_width // 2, 400))
                            window.blit(error_text, error_rect)
                            pygame.display.flip()

            # Select reaction time
            if debug:
                print("Asking for reaction time setting...")
            window.blit(splash_bg, (0, 0))
            reaction_time_input = ""
            valid_reaction_time = False
            while not valid_reaction_time:
                check_music()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        if debug:
                            print("Quit command received while on reaction time input screen.")
                        safe_exit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:  # needs fixed so you can go back
                            if debug:
                                print("Key to back up in vs_cpu reaction time selection or return to menu pressed.")
                            menu_select_sound.play()
                            showMenu = True
                            inGame = False
                            return
                        elif event.key == K_RETURN:
                            if debug:
                                print("Reaction time entered.")
                            menu_select_sound.play()
                            reaction_time_str = reaction_time_input.strip()
                            if reaction_time_str.isdigit() or reaction_time_str.replace('.', '', 1).isdigit():
                                reaction_time = float(reaction_time_str)
                                valid_reaction_time = True
                                if debug:
                                    print(f"Valid reaction time entered: {reaction_time}")
                            else:
                                if debug:
                                    print("Invalid reaction time entered.")
                                error_text = font.render("Invalid reaction time. Please enter a valid number.",
                                                         True, errorColor)
                                error_rect = error_text.get_rect(center=(window_width // 2, 400))
                                window.blit(error_text, error_rect)
                                pygame.display.flip()
                        elif event.key == K_BACKSPACE:
                            reaction_time_input = reaction_time_input[:-1]
                        else:
                            reaction_time_input += event.unicode

                window.blit(splash_bg, (0, 0))
                reaction_time_input_text = font.render("Please enter your desired reaction time in seconds: " + reaction_time_input, True, textColor)
                reaction_time_input_rect = reaction_time_input_text.get_rect(center=(window_width // 2, 300))
                window.blit(reaction_time_input_text, reaction_time_input_rect)
                pygame.display.flip()

        elif game_mode == "online" and is_host:
            if debug:
                print("Displaying server hosting options screen...")
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
                check_music()
                global PORT
                for event in pygame.event.get():
                    if event.type == QUIT:
                        if debug:
                            print("Quit command received on server host options page.")
                        safe_exit()
                    if event.type == KEYDOWN:
                        paddle_hit_sound.play()  # Play paddle hit sound on keystroke in IP info screen
                        if event.unicode.isdigit():
                            if debug:
                                print("Adding digit to port choice.")
                            port_choice += event.unicode
                        elif event.key == K_ESCAPE:  # needs fixed so it actually goes back
                            if debug:
                                print("Button to return to menu has been pressed.")
                            menu_select_sound.play()
                            showMenu = True
                            inGame = False
                            return
                        elif event.key == K_BACKSPACE:
                            if debug:
                                print("Removing character from port choice.")
                            port_choice = port_choice[:-1]
                        elif event.key == K_RETURN:
                            if debug:
                                print("Checking port choice...")
                            if port_choice.isdigit() and 1 <= int(port_choice) <= 65535:
                                if debug:
                                    print("Port choice is valid!")
                                valid_input = True
                            else:
                                if debug:
                                    print("Port choice is not valid!")
                        window.blit(splash_bg, (0, 0))
                        window.blit(title_text, title_rect)
                        window.blit(host_text, host_rect)
                        window.blit(lan_ip_text, lan_ip_rect)
                        window.blit(port_text, port_rect)
                        input_text = font.render(port_choice, True, textColor)
                        input_rect = input_text.get_rect(center=(window_width // 2, 400))
                        window.blit(input_text, input_rect)
                        if not valid_input:
                            if debug:
                                print("Port number invalid!")
                            error_text = font.render("Invalid port number. Please enter a valid port (1-65535).", True,
                                                     textColor)
                            error_rect = error_text.get_rect(center=(window_width // 2, 500))
                            window.blit(error_text, error_rect)
                        pygame.display.flip()
            PORT = int(port_choice)
            start_server()
            if debug:
                print("Starting client listener thread...")
            listen_thread = threading.Thread(target=listen_for_clients)
            listen_thread.start()
            font = pygame.font.Font(None, options_font_size)
            text = "Waiting for client to connect..."
            text_rendered = font.render(text, True, textColor)
            text_width = text_rendered.get_width()
            text_height = text_rendered.get_height()
            text_x = (window_width - text_width) // 2
            text_y = (window_height - text_height) // 2
            window.blit(splash_bg, (0, 0))
            window.blit(text_rendered, (text_x, text_y))
            pygame.display.flip()
            listen_thread.join()
            if debug:
                print("Client connected!")
            text = "Client connected!"
            text_rendered = font.render(text, True, textColor)
            text_width = text_rendered.get_width()
            text_height = text_rendered.get_height()
            text_x = (window_width - text_width) // 2
            text_y = (window_height - text_height) // 2
            window.blit(splash_bg, (0, 0))
            window.blit(text_rendered, (text_x, text_y))
            pygame.display.flip()
        elif game_mode == "online" and not is_host:
            if debug:
                print("Showing join server options...")
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
                check_music()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        if debug:
                            print("Quit command received while on server join options.")
                        safe_exit()
                    if event.type == KEYDOWN:
                        paddle_hit_sound.play()
                        if event.unicode.isdigit():
                            if debug:
                                print("Digit detected.")
                            if len(server_ip) < 15:
                                if debug:
                                    print("Digit added to server_ip.")
                                server_ip += event.unicode
                        elif event.key == K_ESCAPE:  # needs fixed so you can actually go back
                            if debug:
                                print("Button to return to menu pressed.")
                            menu_select_sound.play()
                            showMenu = True
                            inGame = False
                            return
                        elif event.key == K_BACKSPACE:
                            if debug:
                                print("Removing a character from the server_ip.")
                            server_ip = server_ip[:-1]
                        elif event.key == K_RETURN:
                            if debug:
                                print("Checking ip address...")
                            try:
                                ipaddress.IPv4Address(server_ip)
                                if debug:
                                    print("server_ip is a valid IPv4 address.")
                                if port_choice.isdigit() and 1 <= int(port_choice) <= 65535:
                                    if debug:
                                        print("port_choice is a valid port.")
                                    valid_input = True
                            except ipaddress.AddressValueError:
                                if debug:
                                    print("server_ip is not a valid IPv4 address.")
                                pass
                        elif event.key == K_PERIOD:
                            if debug:
                                print("Period detected.")
                            if len(server_ip) < 15:
                                if debug:
                                    print("Period added to server_ip")
                                server_ip += "."
                        elif event.key == K_COLON:
                            if debug:
                                print("Colon detected.")
                            if not port_choice:
                                if debug:
                                    print("Adding colon to port_choice.")
                                port_choice += ":"
                        elif event.key == K_MINUS:
                            if debug:
                                print("Minus detected.")
                            if not port_choice:
                                if debug:
                                    print("Adding minus to port_choice.")
                                port_choice += "-"
                        elif event.key == K_UNDERSCORE:
                            if debug:
                                print("Underscore detected.")
                            if not port_choice:
                                if debug:
                                    print("Adding underscore to port_choice.")
                                port_choice += "_"
                        elif event.key == K_BACKSLASH:
                            if debug:
                                print("Backslash detected.")
                            if not port_choice:
                                if debug:
                                    print("Adding backslash to port_choice.")
                                port_choice += "\\"
                        window.blit(splash_bg, (0, 0))
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
                            if debug:
                                print("Invalid data passed and valid_input is false.")
                            error_text = font.render("Invalid server IP address or port number.", True, errorColor)
                            error_rect = error_text.get_rect(center=(window_width // 2, 550))
                            window.blit(error_text, error_rect)
                        pygame.display.flip()
            PORT = int(port_choice)
            join_server(server_ip, PORT)
        elif game_mode == "tutorial":
            run_tutorial()
        elif game_mode == "local_multiplayer":
            inGame = True
        else:
            if debug:
                print("Invalid data passed to game mode interpreter. Crashing softly.")
            safe_exit()
        while inGame:
            check_music()
            for event in pygame.event.get():
                if event.type == QUIT:
                    if debug:
                        print("Quit command received while in game.")
                    safe_exit()
                elif event.type == KEYDOWN:
                    if event.key == K_p and game_mode != "online":
                        if debug:
                            print("Pause toggled.")
                        paused = not paused  # Toggle pause state when 'P' key is pressed
                        menu_select_sound.play()
                    elif event.key == pygame.K_m:
                        if debug:
                            print("Change song key pressed...")
                        fade_thread = threading.Thread(target=fade_out_song)
                        fade_thread.start()
                        change_song()
                        play_thread = threading.Thread(target=load_and_play_song)
                        play_thread.start()
                    elif event.key == K_ESCAPE:
                        if debug:
                            print("Return to menu key pressed.")
                        menu_select_sound.play()
                        showMenu = True
                        inGame = False
                        reset_scoring()
                        reset_game()
                        break
            if not paused:  # Only update game logic if the game is not paused
                keys = pygame.key.get_pressed()

                # Move the paddles (Player 1 controls)
                if game_mode != "online" or (game_mode == "online" and is_host):
                    if keys[K_w] and left_paddle.y > 0:
                        move_paddle(left_paddle, {K_w: True}, paddle_speed_left, paddle_max_velocity_left,
                                    paddle_friction_left)
                        if game_mode == "online":
                            send_data(game_state)
                    if keys[K_s] and left_paddle.y < window_height - paddle_height_left:
                        move_paddle(left_paddle, {K_s: True}, paddle_speed_left, paddle_max_velocity_left,
                                    paddle_friction_left)
                        if game_mode == "online":
                            send_data(game_state)
                    # Move the paddle (no keys pressed)
                    move_paddle(left_paddle, acceleration=paddle_speed_left, max_velocity=paddle_max_velocity_left,
                                friction=paddle_friction_left)

                # Move the paddles (Player 2 controls)
                if game_mode == "local_multiplayer" or (game_mode == "online" and not is_host):
                    if keys[K_UP] and right_paddle.y > 0:
                        move_paddle(right_paddle, {K_UP: True}, paddle_speed_right, paddle_max_velocity_right,
                                    paddle_friction_right, "up")
                        if game_mode == "online":
                            send_data(game_state)
                    if keys[K_DOWN] and right_paddle.y < window_height - paddle_height_right:
                        move_paddle(right_paddle, {K_DOWN: True}, paddle_speed_right, paddle_max_velocity_right,
                                    paddle_friction_right, "down")
                        if game_mode == "online":
                            send_data(game_state)
                    # Move the paddles (no keys pressed)
                    move_paddle(right_paddle, acceleration=paddle_speed_right, max_velocity=paddle_max_velocity_right,
                                friction=paddle_friction_right)
                elif game_mode == "vs_cpu" or "tutorial":
                    # Move the CPU paddle (Player 2 controlled by CPU)
                    move_cpu_paddle(difficulty_level)
                # Move the ball
                if debug:
                    print("Moving the ball...")
                    if debug:
                        print(f"Ball old position: ({ball.x}, {ball.y})")
                ball.x += ball_x_speed
                ball.y += ball_y_speed
                if debug:
                    print(f"Ball new position: ({ball.x}, {ball.y})")
                # Ball collision with paddles
                if ball.colliderect(left_paddle):
                    if debug:
                        print("Ball collided with the left paddle.")
                    paddle_hit_sound.play()
                    if ball.centery < left_paddle.top or ball.centery > left_paddle.bottom:
                        # Ball hit the top or bottom of the left paddle
                        ball_x_speed = abs(ball_x_speed)  # Reverse the x-speed to make the ball move to the right
                        ball_y_speed *= -1  # Reverse the y-speed to make the ball bounce up or down
                    elif ball.right > left_paddle.left:
                        # Ball hit the front face of the left paddle
                        ball_x_speed = abs(ball_x_speed)  # Reverse the x-speed to make the ball move to the right
                        ball_y_speed -= left_paddle_y_speed * paddle_friction_left  # Apply left paddle friction force

                    # Adjust ball position to prevent getting stuck inside paddle
                    ball.left = left_paddle.right + 1  # Add a small offset to move the ball slightly outside the paddle

                elif ball.colliderect(right_paddle):
                    if debug:
                        print("Ball collided with the right paddle.")
                    paddle_hit_sound.play()
                    if ball.centery < right_paddle.top or ball.centery > right_paddle.bottom:
                        # Ball hit the top or bottom of the right paddle
                        ball_x_speed = -abs(ball_x_speed)  # Reverse the x-speed to make the ball move to the left
                        ball_y_speed *= -1  # Reverse the y-speed to make the ball bounce up or down
                    elif ball.left < right_paddle.right:
                        # Ball hit the front face of the right paddle
                        ball_x_speed = -abs(ball_x_speed)  # Reverse the x-speed to make the ball move to the left
                        ball_y_speed -= right_paddle_y_speed * paddle_friction_right  # Apply right paddle friction
                        # force

                    # Adjust ball position to prevent getting stuck inside paddle
                    ball.right = right_paddle.left + 1  # Add a small offset to move the ball slightly outside the
                    # paddle
                # Ball collision with walls
                if ball.y <= 0 or ball.y >= window_height - ball_radius:
                    if debug:
                        if ball.y <= 0:
                            print("Ball collided with the top wall")
                        else:
                            print("Ball collided with the bottom wall")
                    ball_collision_sound.play()
                    ball_y_speed *= -1
                # Check if the ball is out of bounds
                if ball.x < 0:  # if ball goes past left wall
                    if debug:
                        print("Ball went past the left wall.")
                    player2_score += 1
                    reset_game()
                elif ball.x > window_width:  # if ball goes past right wall
                    if debug:
                        print("Ball went past the right wall.")
                    player1_score += 1
                    reset_game()
                # Check for the winning condition, depending on win type
                if win_type == "score_threshold":
                    if player1_score >= score_threshold:
                        if debug:
                            print("Score threshold reached. Player 1 Wins!")
                        winner_text = "Player 1 wins!"
                        win_sound.play()
                        game_over = True
                        inGame = False
                        showMenu = True
                        break
                    elif player2_score >= score_threshold:
                        if debug:
                            print("Score threshold reached. Player 2 wins!")
                        winner_text = "Player 2 wins!"
                        lose_sound.play()
                        game_over = True
                        inGame = False
                        showMenu = True
                        break
                # elif win_type == "time_trial":
                # elif win_type == "survival":
                # elif win_type == "rounds":
                else:
                    if debug:
                        print("Error during win condition selection. Data doesn't match known types. Crashing softly.")
                    safe_exit()
                if is_host and game_mode == "online":
                    if debug:
                        print("Sending game state...")
                    send_data(game_state)
                    # Synchronize game state
                    if debug:
                        print("Synchronizing game state to match current match circumstances.")
                    game_state["left_paddle"] = left_paddle
                    game_state["right_paddle"] = right_paddle
                    game_state["ball"] = ball
                if game_mode == "online":
                    try:
                        if is_host:
                            if debug:
                                print("Received data as host.")
                            received_data = non_blocking_receive(hostdc_socket)
                        else:
                            if debug:
                                print("Received data as client.")
                            received_data = non_blocking_receive(client_socket)
                        if received_data:
                            if debug:
                                print("Unpacking received data.")
                            game_state = pickle.loads(received_data)
                            if debug:
                                print("Data stream: " + game_state)
                            left_paddle = game_state["left_paddle"]
                            right_paddle = game_state["right_paddle"]
                            ball = game_state["ball"]
                    except socket.error as e:
                        print("Socket error:", e)
                        break
                # Draw the game objects
                if debug:
                    print("Begin drawing the game.")
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
                    if debug:
                        print("Game is paused.")
                    font = pygame.font.Font(None, options_font_size)
                    text = font.render("Paused", True, textColor)
                    text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
                    window.blit(text, text_rect)
                # Update the display
                pygame.display.update()
                clock.tick(60)


if debug:
    print("Starting main().")
main()
if debug:
    print("Exiting after main() has closed.")
safe_exit()
if debug:
    print("EOF")
