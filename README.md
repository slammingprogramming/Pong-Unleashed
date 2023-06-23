# Pong Unleashed
 A revitalized version of the classic game "Pong".

To run this code, you'll need to have the Pygame library installed. You can install it using pip:

pip install pygame

 the game mode is determined by the player_vs_player variable. If it's set to True, it will be a player vs player mode where both players can control their respective paddles using the 'W', 'S' keys for the left paddle and the up and down arrows for the right paddle. If it's set to False, it will be a player vs CPU mode where the right paddle is controlled by the CPU.

The CPU-controlled paddle in the player vs CPU mode uses a simple algorithm to track the ball's vertical position and moves towards it with a delay to simulate a more human-like movement.

You can switch between player vs player and player vs CPU modes by changing the value of the player_vs_player variable to True or False accordingly.