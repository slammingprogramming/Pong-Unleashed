# Pong Unleashed
Latest Version: 0.2.1

Pong Unleashed is a classic pong game implemented in Python using the Pygame library. It offers various game modes, including local multiplayer, single-player against CPU, online multiplayer, and a tutorial mode to help players get familiar with the game mechanics.

![Pong Unleashed Gameplay](pong_unleashed.png)

## Features

- Classic pong gameplay with simple controls
- Multiple game modes to choose from:
  - Local Multiplayer: Play against a friend on the same computer.
  - VS CPU: Challenge yourself against an AI-controlled opponent with adjustable difficulty levels.
  - Online Multiplayer: Play against a friend over a network by hosting or joining a server. (Needs fixing)
  - Tutorial: Learn the game mechanics and rules through a step-by-step tutorial.
- Various difficulties in CPU-controlled mode to provide a challenging experience.
- Real-time synchronization of game state in online multiplayer mode.
- Pause functionality for all offline game modes.
- Colorful and responsive graphics using Pygame.

## Installation

To run the game, follow these steps:

1. Make sure you have Python 3.x installed on your system.
2. Clone this repository or download the source code files.
3. Install the required dependencies by running the following commands:
   ```
   pip install pygame
   pip install ipaddress
   ```
4. Run the game by executing the `pong_unleashed.py` file:
   ```
   python pong_unleashed.py
   ```

## Game Controls

### General Controls

- P key: Pause/Unpause the game (Not available in online multiplayer mode).

### Local Multiplayer

- Player 1 (Left Paddle):
  - Move Up: W key
  - Move Down: S key

- Player 2 (Right Paddle):
  - Move Up: Up Arrow key
  - Move Down: Down Arrow key

### VS CPU/Online Multiplayer

- Player 1 (Left Paddle):
  - Move Up: W key
  - Move Down: S key

- CPU (Right Paddle):
  - The CPU paddle is controlled by the AI with adjustable difficulty levels or by another player over the network.

## Networking Setup (Online Multiplayer) (NEEDS FIXING)

To enable online multiplayer functionality in Pong Unleashed, you can set up a server-hosted game or join an existing game server. The game utilizes sockets for network communication and pickle for data serialization. Follow the steps below to configure the networking setup for online multiplayer:

1. Ensure that you and your opponent are connected to the same network or have access to the internet.

2. Decide who will be the host and who will join the game as the client.

### Host Setup (NEEDS FIXING)

If you want to host the game, follow these steps:

1. Open the terminal and navigate to the directory where the game code is located.

2. Run the game by executing the Python script: `python pong_unleashed.py`

3. Choose option 3, which represents hosting an online game.

4. Take note of your host IP address, which will be displayed in the terminal. You'll need to provide this IP address to the client for them to connect to your game.

5. Enter a specific port number to host the server on (optional). By default, the port number is set to 12345. Make sure the chosen port is not blocked by your firewall.

Note: If you plan to host a server for online multiplayer over the Internet, you will need to configure port forwarding on your router. Port forwarding allows incoming network connections to reach your server. Consult your router's documentation or refer to online resources for guidance on how to set up port forwarding.

### Client Setup (NEEDS FIXING)

If you want to join a game as a client, follow these steps:

1. Open the terminal and navigate to the directory where the game code is located.

2. Run the game by executing the Python script: `python pong_unleashed.py`

3. Choose option 4, which represents joining an online game.

4. Enter the IP address of the server you want to connect to.

5. Enter the port number of the server (optional). By default, the port number is set to 12345.

6. If the provided IP address and port are correct, the game will establish a connection to the server, and you will join the game as a client.

### Online Gameplay (NEEDS FIXING)

Once the host and client are connected, they can start playing Pong Unleashed together. The game will synchronize the game state between the host and the client, allowing both players to see the same paddles and ball positions.

Note: In case of any issues or errors related to networking, ensure that your network allows for socket communication, and the necessary ports are open. Additionally, make sure you have the required dependencies installed, such as Pygame and pickle.

Enjoy playing Pong Unleashed with your friends online!

## Planned Improvements

- Implement power-ups: Add power-ups that appear during gameplay and provide temporary advantages or disadvantages to the players, such as increasing paddle size, adding extra balls, or slowing down the opponent's paddle.
- Customizable game settings: Allow players to customize game settings, such as ball speed, paddle speed, paddle size, and game duration, to suit their preferences.
- Different ball behaviors: Introduce variations in ball behavior, such as balls that accelerate over time, balls that change direction randomly, or balls that leave a trail behind them.
- Multiple game modes: Add different game modes, such as time trial mode (where players try to score as many points as possible within a limited time), obstacle mode (where obstacles obstruct the ball's path), or target mode (where players aim for specific targets on the screen).
- Visual effects: Enhance the visual appeal of the game by incorporating particle effects, animations, and dynamic backgrounds.
- Difficulty levels: Expand the difficulty levels to provide a gradual progression of challenge, offering options for beginners, intermediate players, and advanced players.
- Skinning/Theming Support
- Multiplayer online matchmaking: Implement an online matchmaking system that allows players to compete against opponents of similar skill levels.
- High scores and leaderboards: Add a high score system and leaderboards to encourage competition among players and provide a sense of achievement.
- Customizable paddle skins: Allow players to choose different paddle skins or even upload their own custom images to personalize their paddles.
- Achievements and rewards: Introduce achievements or unlockable rewards for completing specific challenges or reaching milestones within the game.
- Support for UPnP for server hosting and matchmaking.
- Implement server-based multiplayer support and matchmaking.
- Implement GUI
- Scoring systems
- Direct connect functionality
- Settings file and menu
- Usernames and randomized identifier strings
- Improved security for multiplayer
- Something RJ wants
- Something the first person to ask for a feature wants(as long as it's relevant and reasonable, submit via issues.)
- Ease of use features (Less quitting constantly, more returning to menu.)
- QOL adjustments, such as having the ball go one or the other way depending on 1) random chance, 2) the last player to win serves, or 3) other variables i.e. constantly to one or the other side, as well as other things like paddles and window resizability without breaking things
- make it not break when you grab the window
- paddle materials, add bounciness and friction coefficients to change how paddles interact with the ball
- ball materials, add bounciness and friction coefficients to them as well
- make esc a way to return to menu(if offline in-game or in lobby), return to lobby(if online and in-game), back up in menus, and close the game from the main menu.
- fix issue with join game ip and port entering
- fix issue with server hosting where invalid port is displayed even when a valid port is available. Also, add the default port to screen text and allow user to just leave it blank to go to default.
- Fix the same issue and add the same default functionality to join game
- Time Limit: Set a time limit for the game, and the player with the highest score when the time runs out wins. For instance, the player with the highest score after 2 minutes wins.
- Lives System: Give each player a certain number of lives, and the first player to lose all their lives loses the game. The opponent is declared the winner. This adds an element of survival to the game.
- Round-based: Divide the game into multiple rounds, and the player who wins the majority of the rounds wins the game. For example, the first player to win 3 out of 5 rounds is the winner.

## License

Pong Unleashed and any of it's assets not otherwise specifically mentioned are licensed under the [GPLv3 License](LICENSE).

### Music Licensing and Credit
- Title Screen Music: The Chosen by Tetuano
- Song 1: Dream Potion by tubebackr
- Song 2: Let's Party by Aylex
- Song 3: Neon Metaphor by ESCP

- All music in this repository is licensed under the [Free To Use License](https://freetouse.com/music/usage-policy)
- Source: [No Copyright Music (Free Download)](https://freetouse.com/music)

### Sound Effect Licensing and Credit
All sound effects are from [Pixabay](https://pixabay.com/sound-effects/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music) and fall under the [Pixabay License](https://pixabay.com/service/license-summary/)

Interface Select Sound Effect by [UNIVERSFIELD](https://pixabay.com/users/universfield-28281460/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=124464) from [Pixabay](https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=124464)

## Acknowledgements

- This game was developed using the Pygame library: [https://www.pygame.org/](https://www.pygame.org/)
- Original game credit goes to Atari, Inc. and Allan Alcorn, designer of Pong.
- Inspiration credit goes to my good friend RJ, who inspired me to create this as my first game.

## Contributing

Contributions to Pong Unleashed are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## About

Pong Unleashed was developed by Ashtin Wilkin-Blanchard. You can find more of my projects on [GitHub](https://github.com/slammingprogramming).

Enjoy playing Pong Unleashed! Have fun!