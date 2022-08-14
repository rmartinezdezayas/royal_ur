from environment import Game
from agents import RandomAgent, Human, FirstMoveAgent, LastMoveAgent

iterations = 10

# random_vs_random
for iter in range(iterations):
    new_game = Game(RandomAgent('RandomAgent1'), RandomAgent('RandomAgent2'), 'game_simulation_logs/random_vs_random')

# random_vs_first_move_agent
for iter in range(iterations):
    new_game = Game(RandomAgent(), FirstMoveAgent(), 'game_simulation_logs/random_vs_first_move_agent')

# random_vs_last_move_agent
for iter in range(iterations):
    new_game = Game(RandomAgent(), LastMoveAgent(), 'game_simulation_logs/random_vs_last_move_agent')

# first_move_agent_vs_last_move_agent
for iter in range(iterations):
    new_game = Game(FirstMoveAgent(), LastMoveAgent(), 'game_simulation_logs/first_move_agent_vs_last_move_agent')