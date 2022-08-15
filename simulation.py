from first_move_agent import FirstMoveAgent
from last_move_agent import LastMoveAgent
from random_agent import RandomAgent
from greedy_agent import GreedyAgent
from human_agent import Human
from environment import Game

iterations = 2

game_state = {
            'game_id': 'partial_game',
            'turn_id': 1,
            'turn': 'Player1',
            'token_color': 'light',
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

# # human_vs_random
# for iter in range(iterations):
#     new_game = Game(player1=Human('Player1'), player2=RandomAgent(), log_path='game_simulation_logs/human_vs_random', game_state=game_state, dice_roll_manual=False, print_board=True)

# random_vs_random
for iter in range(iterations):
    new_game = Game(player1=RandomAgent('RandomAgent1'), player2=RandomAgent('RandomAgent2'),log_path='game_simulation_logs/random_vs_random')

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
#     new_game = Game(FirstMoveAgent(), GreedyAgent(), 'game_simulation_logs/first_move_agent_vs_greedy_agent')

# # last_move_agent_vs_greedy_agent
# for iter in range(iterations):
#     new_game = Game(LastMoveAgent(), GreedyAgent(), 'game_simulation_logs/last_move_agent_vs_greedy_agent')

# # random_vs_greedy_agent
# for iter in range(iterations):
#     new_game = Game(RandomAgent(), GreedyAgent(), 'game_simulation_logs/random_vs_greedy_agent')