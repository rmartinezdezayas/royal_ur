from expectimax_agent import ExpectimaxAgent
from first_move_agent import FirstMoveAgent
from last_move_agent import LastMoveAgent
from random_agent import RandomAgent
from greedy_agent import GreedyAgent
from agent_interface import Agent
from human_agent import Human
from environment import Game

iterations = 2

game_state = {
            'game_id': 'partial_game',
            'turn_id': 5,
            'turn': 'RandomAgent1',
            'token_color': 'dark',
            'dice_roll_result': 3,
            'light_token_1_position': 1,
            'light_token_2_position': 2,
            'light_token_3_position': 0,
            'light_token_4_position': 0,
            'light_token_5_position': 0,
            'light_token_6_position': 0,
            'light_token_7_position': 0,
            'dark_token_1_position': 5,
            'dark_token_2_position': 0,
            'dark_token_3_position': 0,
            'dark_token_4_position': 0,
            'dark_token_5_position': 0,
            'dark_token_6_position': 0,
            'dark_token_7_position': 0,
            'decision': ''
        }

# # human_agent_vs_random_agent
# for iter in range(iterations):
#     new_game = Game(player1=Human('Player1'), player2=RandomAgent(), log_path='game_simulation_logs/human_agent_vs_random_agent', game_state=game_state, dice_roll_manual=False, print_board=True)

# random_agent_vs_random_agent
for iter in range(iterations):
    new_game = Game(player1=RandomAgent('RandomAgent1'), player2=RandomAgent('RandomAgent2'), log_path='game_simulation_logs/random_agent_vs_random_agent', log_output=True)
    
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