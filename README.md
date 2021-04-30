# MinimaxConnect383Bot

Connect 383

Our variant, Connect 383, will have three main differences from the basic game. First, we will
not be limited to 6x7 boards. Secondly, games may start with one or more “obstacle” pieces
already on the board which do not belong to either player. Lastly, play will always continueuntil the board is completely full (even after a player has achieved 4-in-a-row), at which point
scores for each player will be calculated.
Points are awarded as follows: for each run of length three or
greater, the player will receive points equal to the square of the
length of that run. For example, 3-in-a-row is worth 9 points,
4-in-a-row 16, 5-in-a-row 25, etc.
For the 4x4 board on the left, Player 1 scores 18 points (one vertical
and one diagonal 3-in-a-row), while Player 2 receives 16 points (one
diagonal 4-in-a-row). The two obstacles (gray) don’t contribute to
either player’s score.
When calculating the value of different moves, your game-playing
agent will use the scores as utility values for the terminal games states, and seek to maximize
the delta between its score and that of its opponent using Minimax.
