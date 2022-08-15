import pandas as pd
import datetime
import random
import csv

class Game:

    def __init__(self, player1, player2, log_path, game_state=None, dice_roll_manual=False, print_board=False):
        self.player1 = player1
        self.player1_token_color = 'light'
        self.player2 = player2
        self.player2_token_color = 'dark'
        self.game_state = game_state
        self.print_board = print_board
        self.winner = None
        self.log_path = log_path
        self.dice_roll_manual = dice_roll_manual
        if game_state == None:
            self.create_new_game_state()
        self.create_game_log()
        self.start_game_engine()

    def create_new_game_state(self):
        self.game_state = {
            'game_id': datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'),
            'turn_id': 1,
            'turn': self.player1.name,
            'token_color': 'light',
            'dice_roll_result': self.dice_roll(),
            'light_token_1_position': 0,
            'light_token_2_position': 0,
            'light_token_3_position': 0,
            'light_token_4_position': 0,
            'light_token_5_position': 0,
            'light_token_6_position': 0,
            'light_token_7_position': 0,
            'dark_token_1_position': 0,
            'dark_token_2_position': 0,
            'dark_token_3_position': 0,
            'dark_token_4_position': 0,
            'dark_token_5_position': 0,
            'dark_token_6_position': 0,
            'dark_token_7_position': 0,
            'decision': ''
        }

    def dice_roll(self):
        if self.dice_roll_manual == False:
            dice_roll_result = 0
            for dice in range(0, 4):
                dice_roll_result += random.randint(0,1)
            return dice_roll_result
        else:
            while True:
                try:
                    dice_roll_result = int(input('Enter dice roll value [0 1 2 3 4]: '))
                    if dice_roll_result in range(1, 5):
                        break
                except:
                    print('Input not valid, try again.')

            return dice_roll_result

    def create_game_log(self):
        with open(f'{self.log_path}/{self.game_state["game_id"]}.csv', 'w', newline='') as game_file:
            writer = csv.DictWriter(game_file, delimiter='\t', fieldnames = self.game_state.keys())
            writer.writeheader()
            game_file.close()

    def log_decision(self):
        with open(f'{self.log_path}/{self.game_state["game_id"]}.csv', 'a', newline='') as game_file:
            writer = csv.DictWriter(game_file, delimiter='\t', fieldnames = self.game_state.keys())
            writer.writerow(self.game_state)
            game_file.close()

    def get_both_players_positions(self):
        self.current_player_token_color = self.player1_token_color if self.game_state['turn'] == self.player1.name else self.player2_token_color
        self.rival_player_token_color = self.player2_token_color if self.game_state['turn'] == self.player1.name else self.player1_token_color
        current_player_token_positions = [self.game_state[f'{self.current_player_token_color}_token_{token}_position'] for token in range(1,8)]
        rival_player_token_positions = [self.game_state[f'{self.rival_player_token_color}_token_{token}_position'] for token in range(1,8)]
        return current_player_token_positions, rival_player_token_positions

    def get_options(self):
        current_player_token_positions, rival_player_token_positions = self.get_both_players_positions()
        options = []
        if self.game_state['dice_roll_result'] > 0:
            # check each token position in order to evaluate if it can be moved or not.
            for i, token_position in enumerate(current_player_token_positions):
                # An option is created if:
                # 1. The option is not already in the bag of options. (0->2 0->2 are the same option, just using different tokens to put on the board.)
                # 2. The token position of the option + the dice roll steps <= 15
                # 3. There is no ally token on the destination tile (except if it is the goal tile 15).
                # 4. The destination tile can be the 8 (blocking rossete) but there can not be a rival token there. (not being an ally token is covered by condition 3)
                if ((token_position, token_position + self.game_state['dice_roll_result']) not in options) and (token_position + self.game_state['dice_roll_result'] <= 15) and (token_position + self.game_state['dice_roll_result'] not in current_player_token_positions or token_position + self.game_state['dice_roll_result'] == 15) and ((token_position + self.game_state['dice_roll_result'] == 8 and 8 not in rival_player_token_positions) or token_position + self.game_state['dice_roll_result'] != 8):
                    options.append((token_position, token_position + self.game_state['dice_roll_result']))
        return options

    def is_game_finished(self):
        current_player_token_positions, rival_player_token_positions = self.get_both_players_positions()
        if set(current_player_token_positions) == {15} or set(rival_player_token_positions) == {15}:
            self.winner = self.player2.name if self.game_state['turn'] == self.player1.name else self.player1.name
            return True
        else:
            return False

    def update_game_state_with_decision(self, player_decision, player_options):
        try:
            self.game_state['decision'] = list(filter(lambda x: x[0]==int(player_decision), player_options))[0]
        except:
            self.game_state['decision'] = ''
        self.log_decision()

        if player_decision != None:
            current_player_token_positions, rival_player_token_positions = self.get_both_players_positions()
            for i, player_position in enumerate(current_player_token_positions):
                if player_position == self.game_state['decision'][0]:
                    self.game_state[f'{self.current_player_token_color}_token_{i+1}_position'] = self.game_state['decision'][1]
                    for i, rival_position in enumerate(rival_player_token_positions):
                        if rival_position == self.game_state['decision'][1] and rival_position in [5, 6, 7, 9, 10, 11, 12]:
                            self.game_state[f'{self.rival_player_token_color}_token_{i+1}_position'] = 0
                            break
                    break

        self.game_state['dice_roll_result'] = self.dice_roll()
        self.game_state['turn_id'] += 1
        if self.game_state['decision'] == '' or self.game_state['decision'][1] not in [4, 8, 14]:
            self.game_state['turn'] = self.player1.name if self.game_state['turn'] == self.player2.name else self.player2.name
        self.game_state['token_color'] = self.player1_token_color if self.game_state['turn'] == self.player1.name else self.player2_token_color

    def start_game_engine(self):
        while self.is_game_finished() == False:
            player_options = self.get_options()
            if self.print_board == True:
                self.print_game(player_options)
            player_decision = None
            if len(player_options) > 1:
                player_decision = self.player1.decide(self.game_state, player_options) if self.player1.name == self.game_state['turn'] else self.player2.decide(self.game_state, player_options)
            if len(player_options) == 1:
                player_decision = player_options[0][0]

            self.update_game_state_with_decision(player_decision, player_options)
        print(f'Game finished! Winner: {self.winner}.')

    def print_game(self, player_options):
        light_player_board_positions = [self.game_state[f'light_token_{token}_position'] for token in range(1,8)]
        dark_player_board_positions = [self.game_state[f'dark_token_{token}_position'] for token in range(1,8)]
        # from
        # [0, 0, 2, 3, 0, 0, 0]
        # to
        # ['L', '.', 'L', 'L', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
        light_final_positions = ['L' if i in light_player_board_positions else '.' for i, value in enumerate(range(0, 16))]
        dark_final_positions = ['D' if i in dark_player_board_positions else '.' for i, value in enumerate(range(0, 16))]

        print(f'Begining of turn {self.game_state["turn_id"]}')
        print(f'Player turn: {self.game_state["turn"]}. Rolled dice: {self.game_state["dice_roll_result"]}')
        print('lights')
        print(light_player_board_positions)
        print('darks')
        print(dark_player_board_positions)
        print('-------')
        print(f'|{light_final_positions[4]}|{light_final_positions[5] + dark_final_positions[5]}|{dark_final_positions[4]}|')
        print('-------')
        print(f'|{light_final_positions[3]}|{light_final_positions[6] + dark_final_positions[6]}|{dark_final_positions[3]}|')
        print('-------')
        print(f'|{light_final_positions[2]}|{light_final_positions[7] + dark_final_positions[7]}|{dark_final_positions[2]}|')
        print('-------')
        print(f'|{light_final_positions[1]}|{light_final_positions[8] + dark_final_positions[8]}|{dark_final_positions[1]}|')
        print('-------')
        print(f'  |{light_final_positions[9] + dark_final_positions[9]}|')
        print('-------')
        print(f'  |{light_final_positions[10] + dark_final_positions[10]}|')
        print('-------')
        print(f'|{light_final_positions[14]}|{light_final_positions[11] + dark_final_positions[11]}|{dark_final_positions[14]}|')
        print('-------')
        print(f'|{light_final_positions[13]}|{light_final_positions[12] + dark_final_positions[12]}|{dark_final_positions[13]}|')
        print('-------')
        print('Options to choose from:')
        print(player_options)
        current_token_color_turn = self.player1_token_color if self.game_state['turn'] == self.player1.name else self.player2_token_color
        print(f'Turn for player {self.game_state["turn"]}. ({current_token_color_turn}). Make your movement...')