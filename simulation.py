from agents.expectimax_agent import ExpectimaxAgent
from agents.first_move_agent import FirstMoveAgent
from agents.last_move_agent import LastMoveAgent
from agents.random_agent import RandomAgent
from agents.greedy_agent import GreedyAgent
from agents.human_agent import Human
from environment import Game

iterations = 2

# human_agent_vs_random_agent
for iter in range(iterations):
    new_game = Game(player1=Human('Player1'), player2=RandomAgent(), log_path='game_simulation_logs/human_agent_vs_random_agent', print_board=True)

# random_agent_vs_random_agent
for iter in range(iterations):
    new_game = Game(player1=RandomAgent('RandomAgent1'), player2=RandomAgent('RandomAgent2'), log_path='game_simulation_logs/random_agent_vs_random_agent')
    
# random_agent_vs_first_move_agent
for iter in range(iterations):
    new_game = Game(player1=RandomAgent(), player2=FirstMoveAgent(),log_path='game_simulation_logs/random_agent_vs_first_move_agent')

# random_agent_vs_last_move_agent
for iter in range(iterations):
    new_game = Game(player1=RandomAgent(), player2=LastMoveAgent(), log_path='game_simulation_logs/random_agent_vs_last_move_agent')

# first_move_agent_vs_last_move_agent
for iter in range(iterations):
    new_game = Game(player1=FirstMoveAgent(), player2=LastMoveAgent(), log_path='game_simulation_logs/first_move_agent_vs_last_move_agent')

# first_move_agent_vs_greedy_agent
for iter in range(iterations):
    new_game = Game(player1=FirstMoveAgent(), player2=GreedyAgent(), log_path='game_simulation_logs/first_move_agent_vs_greedy_agent')

# last_move_agent_vs_greedy_agent
for iter in range(iterations):
    new_game = Game(player1=LastMoveAgent(), player2=GreedyAgent(), log_path='game_simulation_logs/last_move_agent_vs_greedy_agent')

# random_agent_vs_greedy_agent
for iter in range(iterations):
    new_game = Game(player1=RandomAgent(), player2=GreedyAgent(), log_path='game_simulation_logs/random_agent_vs_greedy_agent')

# random_agent_vs_expectimax_agent
for iter in range(iterations):
    new_game = Game(player1=RandomAgent(), player2=ExpectimaxAgent(), log_path='game_simulation_logs/random_agent_vs_expectimax_agent')

# greedy_vs_expectimax
for iter in range(iterations):
    new_game = Game(player1=GreedyAgent(), player2=ExpectimaxAgent(), log_path='game_simulation_logs/greedy_vs_expectimax')

# last_move_agent_vs_expectimax
for iter in range(iterations):
    new_game = Game(player1=LastMoveAgent(), player2=ExpectimaxAgent(), log_path='game_simulation_logs/last_move_agent_vs_expectimax')