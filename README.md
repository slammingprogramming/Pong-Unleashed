# Pong Unleashed
 

To run this code, you'll need to have the Pygame library installed. You can install it using pip:

pip install pygame

# Pong Unleashed

A revitalized version of the classic game "Pong" using Python and Pygame library. The game supports both offline and online multiplayer modes.

## Features

- Local Multiplayer: Play against a friend on the same computer.
- VS CPU: Play against a computer-controlled opponent.
- Online Multiplayer: Host or join a game to play against other players over the network.

## Prerequisites

- Python 3.x
- Pygame library

## How to Run the Game

1. Install Python 3.x: If you don't have Python installed, download and install the latest version from the official Python website: https://www.python.org/downloads/

2. Install Pygame: Open the terminal/command prompt and run the following command to install Pygame: pip install pygame

3. Download the pong-unleashed.py code from the repository.

4. Run the game: Open a terminal/command prompt, navigate to the directory where the code is saved, and run the following command: python pong-unleashed.py

5. Select the game mode: Follow the on-screen instructions to choose the game mode: local multiplayer, vs CPU, host, or join.

6. Play the game: Control the paddles using the keyboard. Player 1 (left paddle) can use the 'W' and 'S' keys to move up and down, respectively. Player 2 or the CPU-controlled opponent can use the arrow keys ('UP' and 'DOWN').

## Networking Setup (Online Multiplayer)

- Host: Select the "Host" option to start a game server on your computer. Other players can join your game by entering your IP address.
- Join: Select the "Join" option and enter the IP address of the host to connect to their game.

Please note that the online multiplayer feature uses a simple host/join system and may not work in all network configurations. Ensure that your network allows incoming connections on the specified port (default: 12345) and that the necessary firewall settings are in place.

## Acknowledgements

- This game was created using the Pygame library: https://www.pygame.org/
- The code is inspired by various Pong game tutorials and examples available online.

## License

This project is licensed under the [GPLv3 License](LICENSE).