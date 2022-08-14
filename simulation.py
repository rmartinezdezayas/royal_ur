from random import Random
from environment import Game
from agents import RandomAgent, Human, FirstMoveAgent, LastMoveAgent, GreedyAgent

iterations = 100

# # random_vs_random
# for iter in range(iterations):
#     new_game = Game(RandomAgent('RandomAgent1'), RandomAgent('RandomAgent2'), 'game_simulation_logs/random_vs_random')

# # random_vs_first_move_agent
# for iter in range(iterations):
#     new_game = Game(RandomAgent(), FirstMoveAgent(), 'game_simulation_logs/random_vs_first_move_agent')

# # random_vs_last_move_agent
# for iter in range(iterations):
#     new_game = Game(RandomAgent(), LastMoveAgent(), 'game_simulation_logs/random_vs_last_move_agent')

# # first_move_agent_vs_last_move_agent
# for iter in range(iterations):
#     new_game = Game(FirstMoveAgent(), LastMoveAgent(), 'game_simulation_logs/first_move_agent_vs_last_move_agent')

# # first_move_agent_vs_greedy_agent
# for iter in range(iterations):
#     new_game = Game(FirstMoveAgent(), GreedyAgent(), 'game_simulation_logs/first_move_agent_vs_greedy_agent', True)

# last_move_agent_vs_greedy_agent
for iter in range(iterations):
    new_game = Game(LastMoveAgent(), GreedyAgent(), 'game_simulation_logs/last_move_agent_vs_greedy_agent')

# random_vs_greedy_agent
for iter in range(iterations):
    new_game = Game(RandomAgent(), GreedyAgent(), 'game_simulation_logs/random_vs_greedy_agent')