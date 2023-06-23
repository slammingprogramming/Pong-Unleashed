# Pong Unleashed
 A revitalized version of the classic game "Pong".

To run this code, you'll need to have the Pygame library installed. You can install it using pip:

pip install pygame

 the game mode is determined by the player_vs_player variable. If it's set to True, it will be a player vs player mode where both players can control their respective paddles using the 'W', 'S' keys for the left paddle and the up and down arrows for the right paddle. If it's set to False, it will be a player vs CPU mode where the right paddle is controlled by the CPU.

The CPU-controlled paddle in the player vs CPU mode uses a simple algorithm to track the ball's vertical position and moves towards it with a delay to simulate a more human-like movement.

the game starts with a game mode selection menu where the player can choose between local multiplayer and player vs CPU modes by pressing the '1' or '2' keys, respectively. The game mode is stored in the game_mode variable.

If the player selects local multiplayer mode, both players can control their respective paddles as before. If the player selects player vs CPU mode, the right paddle is controlled by the CPU, which uses a similar algorithm as in the previous version

The game resets and goes back to the game mode selection menu when the ball goes out of bounds, allowing the player to choose a new game mode or quit the game.

You can customize the menu layout and design by modifying the draw_game_mode_menu() function and adjusting the position and appearance of the text elements.