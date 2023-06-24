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

 you can pause and resume using the p key when in offline play

## Planned Improvements
Implement power-ups: Add power-ups that appear during gameplay and provide temporary advantages or disadvantages to the players, such as increasing paddle size, adding extra balls, or slowing down the opponent's paddle.

Sound effects and music: Enhance the gaming experience by adding sound effects for paddle hits, ball collisions, and background music to create a more immersive environment.

Score tracking and win condition: Implement a scoring system to keep track of each player's score and declare a winner when a certain score threshold is reached.

Customizable game settings: Allow players to customize game settings, such as ball speed, paddle speed, paddle size, and game duration, to suit their preferences.

Different ball behaviors: Introduce variations in ball behavior, such as balls that accelerate over time, balls that change direction randomly, or balls that leave a trail behind them.

Multiple game modes: Add different game modes, such as time trial mode (where players try to score as many points as possible within a limited time), obstacle mode (where obstacles obstruct the ball's path), or target mode (where players aim for specific targets on the screen).

Visual effects: Enhance the visual appeal of the game by incorporating particle effects, animations, and dynamic backgrounds.

Difficulty levels: Expand the difficulty levels to provide a gradual progression of challenge, offering options for beginners, intermediate players, and advanced players.

Multiplayer online matchmaking: Implement an online matchmaking system that allows players to compete against opponents of similar skill levels.

High scores and leaderboards: Add a high score system and leaderboards to encourage competition among players and provide a sense of achievement.

Customizable paddle skins: Allow players to choose different paddle skins or even upload their own custom images to personalize their paddles.

Achievements and rewards: Introduce achievements or unlockable rewards for completing specific challenges or reaching milestones within the game.

## Acknowledgements

- This game was created using the Pygame library: https://www.pygame.org/
- The code is inspired by various Pong game tutorials and examples available online.

## License

This project is licensed under the [GPLv3 License](LICENSE).