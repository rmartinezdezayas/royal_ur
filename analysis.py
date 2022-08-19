from multiprocessing import Value
from ast import literal_eval
import pandas as pd
import numpy as np
import os

# logs_path = 'game_simulation_logs/random_vs_random'
# logs_path = 'game_simulation_logs/random_vs_first_move_agent'
# logs_path = 'game_simulation_logs/random_vs_last_move_agent'
# logs_path = 'game_simulation_logs/first_move_agent_vs_last_move_agent'
# logs_path = 'game_simulation_logs/first_move_agent_vs_greedy_agent'
# logs_path = 'game_simulation_logs/last_move_agent_vs_greedy_agent'
# logs_path = 'game_simulation_logs/random_vs_greedy_agent'
# logs_path = 'game_simulation_logs/greedy_vs_expectimax'
# logs_path='game_simulation_logs/last_move_agent_vs_expectimax'
logs_path='game_simulation_logs/deep_q_learning_agent_vs_random_agent'
log_file_limit = 100
log_dataframes = []

for log_file in os.listdir(logs_path)[:log_file_limit]:
    game_dataset = pd.read_csv(f'{logs_path}/{log_file}', delimiter='\t')
    game_dataset['winner'] = game_dataset['turn'].map(lambda x: 1 if x == game_dataset.tail(1)['turn'].values else 0)
    game_dataset['decision'] = game_dataset['decision'].fillna('(0, 0)')
    game_dataset['decision'] = game_dataset['decision'].map(lambda x: literal_eval(x))
    log_dataframes.append(game_dataset)

data = pd.concat(log_dataframes, ignore_index=True)

# winrate between players
last_play = data.groupby('game_id')[['turn_id']].max()
last_play = data.merge(last_play, how='inner', on=['game_id', 'turn_id'])
winrate = last_play.groupby('turn')[['game_id']].count().reset_index(False)
winrate.columns = ['player', 'wins']
winrate['winrate'] = (winrate['wins']/winrate['wins'].sum())
print(winrate)

# # most common game_ states
# data = data[data['token_color'] == 'light']
# data = data[['turn', 'dice_roll_result', 'winner', 'light_token_1_position', 'light_token_2_position', 'light_token_3_position', 'light_token_4_position', 'light_token_5_position', 'light_token_6_position', 'light_token_7_position', 'dark_token_1_position', 'dark_token_2_position', 'dark_token_3_position', 'dark_token_4_position', 'dark_token_5_position', 'dark_token_6_position', 'dark_token_7_position']]
# data.columns = ['turn', 'drr', 'winner', 'l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7']
# most_common_game_states = data.groupby(['drr', 'winner', 'l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7'])['turn'].count().reset_index()
# most_common_game_states = most_common_game_states.sort_values(['turn', 'l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'winner'], ascending=False)

# most_common_game_states.to_csv('most_common_game_states.csv', sep='\t')

# # test reward function hipotesis testing
# def get_reward(game_state: dict, option: tuple):
#     dice_roll_probabilities = [(0, 0.0625), (1, 0.25), (2, 0.375), (3, 0.25), (4, 0.0625)]
#     current_player_token_color = game_state['token_color']
#     rival_player_token_color = 'dark' if current_player_token_color == 'light' else 'light'
#     current_player_token_positions = [game_state[f'{current_player_token_color}_token_{token}_position'] for token in range(1,8)]
#     rival_player_token_positions = [game_state[f'{rival_player_token_color}_token_{token}_position'] for token in range(1,8)]
#     next_turn_score_if_token_land_in_rossete_tile = ((1 + (option[1] + 1 if option[1] + 1 in rival_player_token_positions and option[1] + 1 in [5, 6, 7, 9, 10, 11, 12] else 0)) * dice_roll_probabilities[1][1] + (2 + (option[1] + 2 if option[1] + 2 in rival_player_token_positions and option[1] + 2 in [5, 6, 7, 9, 10, 11, 12] else 0)) * dice_roll_probabilities[2][1] + (3 + (option[1] + 3 if option[1] + 3 in rival_player_token_positions and option[1] + 3 in [5, 6, 7, 9, 10, 11, 12] else 0)) * dice_roll_probabilities[3][1] + (4 + (option[1] + 4 if option[1] + 4 in rival_player_token_positions and option[1] + 4 in [5, 6, 7, 9, 10, 11, 12] else 0)) * dice_roll_probabilities[4][1]) if option[1] in [4, 8, 14] else 0
#     return game_state['dice_roll_result'] + (option[1] if option[1] in rival_player_token_positions and option[1] in [5, 6, 7, 9, 10, 11, 12] else 0) + next_turn_score_if_token_land_in_rossete_tile

# data['reward'] = data.apply(lambda x: get_reward(dict(x), x['decision']), axis=1)

# data = data.groupby(['game_id', 'token_color', 'winner'])['reward'].sum().reset_index()
# data['winner_token_color'] = data.apply(lambda x: x['token_color'] if x['winner'] == 1 else 'light' if x['token_color'] == 'dark' else 'dark', axis=1)
# data['light_reward'] = data.apply(lambda x: data[(data['game_id'] == x['game_id']) & (data['token_color'] == 'light')]['reward'].values[0], axis=1)
# data['dark_reward'] = data.apply(lambda x: data[(data['game_id'] == x['game_id']) & (data['token_color'] == 'dark')]['reward'].values[0], axis=1)

# data = data[['game_id', 'winner_token_color', 'light_reward', 'dark_reward']].drop_duplicates()
# data['winner_have_more_points'] = data.apply(lambda x: 1 if (x['dark_reward'] > x['light_reward'] and x['winner_token_color'] == 'dark') or (x['light_reward'] > x['dark_reward'] and x['winner_token_color'] == 'light') else 0, axis=1)

# data = data.groupby('winner_have_more_points')['game_id'].count().reset_index()
# data.columns = ['winner_have_more_points', 'games_count']

# print(data)
# data.head().to_csv('winner_have_more_points.csv', sep='\t')