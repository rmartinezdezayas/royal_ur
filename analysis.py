from tkinter.ttk import Separator
import pandas as pd
import os

# logs_path = 'game_simulation_logs/random_vs_random'
# logs_path = 'game_simulation_logs/random_vs_first_move_agent'
# logs_path = 'game_simulation_logs/random_vs_last_move_agent'
# logs_path = 'game_simulation_logs/first_move_agent_vs_last_move_agent'
# logs_path = 'game_simulation_logs/first_move_agent_vs_greedy_agent'
# logs_path = 'game_simulation_logs/last_move_agent_vs_greedy_agent'
# logs_path = 'game_simulation_logs/random_vs_greedy_agent'
# logs_path = 'game_simulation_logs/greedy_vs_expectimax'
logs_path='game_simulation_logs/last_move_agent_vs_expectimax'

log_dataframes = []

for log_file in os.listdir(logs_path):
    log_dataframes.append(pd.read_csv(f'{logs_path}/{log_file}', delimiter='\t'))

data = pd.concat(log_dataframes, ignore_index=True)

# winrate between players
last_play = data.groupby('game_id')[['turn_id']].max()
last_play = data.merge(last_play, how='inner', on=['game_id', 'turn_id'])
winrate = last_play.groupby('turn')[['game_id']].count().reset_index(False)
winrate.columns = ['player', 'wins']
winrate['winrate'] = (winrate['wins']/winrate['wins'].sum())
print(winrate)