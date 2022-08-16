from agents.agent_interface import Agent
import datetime
import random
import csv

class Game:

    def __init__(self, player1: Agent, player2: Agent, log_path: str ='.', game_state: dict =None, dice_roll_manual: bool =False, print_board: bool =False, log_output: bool =True, auto_start_game_engine: bool =True):
        '''
        Creates a Game environment instance.

        Parameters:
        player1: A Game like object to be the player 1.
        player2: A Game like object to be the player 2.
        log_path: The string path where the log of the game will be stored as a csv file with "tab" delimiter.
        game_state: A dict indicating a specific game_state from where to start the game environment.
        dice_roll_manual: Boolean indicating if the dice roll shoul be introduced manually or not. (True -> environment will ask for roll dice result value, False -> environment generates a random dice roll result)
        print_board: Boolean for printing a board by console.
        log_output: Boolean indicating if the gameplay log should be stored or not.
        auto_start_game_engine: Boolean for automatically start the game loop after instantiating the class. If False, each next steps in the play should be invoke manually.
        '''
        self.player1 = player1
        self.player2 = player2
        self.game_state = game_state
        self.print_board = print_board
        self.winner = None
        self.log_path = log_path
        self.dice_roll_manual = dice_roll_manual
        if game_state == None:
            self.create_new_game_state()
        self.player1_token_color = self.game_state['token_color']
        self.player2_token_color = 'dark' if self.game_state['token_color'] == 'light' else 'light'
        self.log_output = log_output
        self.create_game_log()
        self.auto_start_game_engine = auto_start_game_engine
        if self.auto_start_game_engine == True:
            self.start_game_engine()

    def create_new_game_state(self):
        '''Creates a new game state to start from.'''
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
        '''Generate dice roll result. If dice_roll_manual is set to True, it will ask for the dice roll result value by console input.'''
        if self.dice_roll_manual == False:
            dice_roll_result = 0
            for dice in range(0, 4):
                dice_roll_result += random.randint(0,1)
            return dice_roll_result
        else:
            while True:
                try:
                    dice_roll_result = int(input('Enter dice roll value [0 1 2 3 4]: '))
                    if dice_roll_result in range(0, 5):
                        break
                except:
                    print('Input not valid, try again.')

            return dice_roll_result

    def create_game_log(self):
        '''Creates the initial file where to store all the gamplay log.'''
        if self.log_output == True:
            with open(f'{self.log_path}/{self.game_state["game_id"]}.csv', 'w', newline='') as game_file:
                writer = csv.DictWriter(game_file, delimiter='\t', fieldnames = self.game_state.keys())
                writer.writeheader()
                game_file.close()

    def log_turn(self):
        '''Add the current ended turn to the log file.'''
        if self.log_output == True:
            with open(f'{self.log_path}/{self.game_state["game_id"]}.csv', 'a', newline='') as game_file:
                writer = csv.DictWriter(game_file, delimiter='\t', fieldnames = self.game_state.keys())
                writer.writerow(self.game_state)
                game_file.close()

    def get_both_players_positions(self):
        '''Get both player position.'''
        self.current_player_token_color = self.player1_token_color if self.game_state['turn'] == self.player1.name else self.player2_token_color
        self.rival_player_token_color = self.player2_token_color if self.game_state['turn'] == self.player1.name else self.player1_token_color
        current_player_token_positions = [self.game_state[f'{self.current_player_token_color}_token_{token}_position'] for token in range(1,8)]
        rival_player_token_positions = [self.game_state[f'{self.rival_player_token_color}_token_{token}_position'] for token in range(1,8)]
        return current_player_token_positions, rival_player_token_positions

    def get_options(self):
        '''Get available options to move the tokens given the current game state.'''
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
        '''Verify if the game has finished.'''
        current_player_token_positions, rival_player_token_positions = self.get_both_players_positions()
        if set(current_player_token_positions) == {15} or set(rival_player_token_positions) == {15}:
            self.winner = self.player2.name if self.game_state['turn'] == self.player1.name else self.player1.name
            return True
        else:
            return False

    def next_turn(self, player_decision: int, player_options: list, desire_dice_roll_result: int =None):
        '''
        Step into the nest turn. Add the decision to the current turn, log that turn into the log file and update all new turn values.

        Parameters:
        player_decision: The position of the token to move forward.
        player_options: The list of options the player have. (Each option is a tuple indicating the initial position of the token to move and the final position where the token will land)
        desire_dice_roll_result: Int value between 0 and 4 to force a specific dice roll.
        '''
        # add decision to current game_state
        try:
            self.game_state['decision'] = list(filter(lambda x: x[0]==int(player_decision), player_options))[0]
        except:
            self.game_state['decision'] = ''

        # log current turn (finished)
        self.log_turn()
        if self.print_board == True:
            print(f'Option chosen: {self.game_state["decision"]}')

        # set values for next turn
        # update token positions based on decision taken
        if self.game_state['decision']  != '':
            current_player_token_positions, rival_player_token_positions = self.get_both_players_positions()
            for i, player_position in enumerate(current_player_token_positions):
                if player_position == self.game_state['decision'][0]:
                    self.game_state[f'{self.current_player_token_color}_token_{i+1}_position'] = self.game_state['decision'][1]
                    for i, rival_position in enumerate(rival_player_token_positions):
                        if rival_position == self.game_state['decision'][1] and rival_position in [5, 6, 7, 9, 10, 11, 12]:
                            self.game_state[f'{self.rival_player_token_color}_token_{i+1}_position'] = 0
                            break
                    break
        # update dice_roll_result and turn_id
        self.game_state['dice_roll_result'] = self.dice_roll() if desire_dice_roll_result == None else desire_dice_roll_result
        self.game_state['turn_id'] += 1

        # do not update player turn if the decision was to get a token into a rossete tile
        if self.game_state['decision'] == '' or self.game_state['decision'][1] not in [4, 8, 14]:
            self.game_state['turn'] = self.player1.name if self.game_state['turn'] == self.player2.name else self.player2.name

        # update token_color based on player turn change
        self.game_state['token_color'] = self.player1_token_color if self.game_state['turn'] == self.player1.name else self.player2_token_color

        # restart decision value
        self.game_state['decision'] = ''

    def start_game_engine(self):
        '''Starts the game loop.'''
        while self.is_game_finished() == False:
            player_options = self.get_options()
            if self.print_board == True:
                self.print_game(player_options)
            player_decision = None
            if len(player_options) > 1:
                player_decision = self.player1.decide(self.game_state, player_options) if self.player1.name == self.game_state['turn'] else self.player2.decide(self.game_state, player_options)
            if len(player_options) == 1:
                player_decision = player_options[0][0]

            self.next_turn(player_decision, player_options)

    def print_game(self, player_options):
        '''Print the game board by console along with usefull information about the turn and the decisions made.'''
        light_player_board_positions = [self.game_state[f'light_token_{token}_position'] for token in range(1,8)]
        dark_player_board_positions = [self.game_state[f'dark_token_{token}_position'] for token in range(1,8)]
        # from token positions
        # light [0, 0, 2, 3, 0, 0, 0]
        # dark  [1, 2, 15, 15, 15, 15, 15]
        # to
        # light ['L', '.', 'L', 'L', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
        # dark  ['.', 'D', 'D', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'D']
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
        print(f'Turn for player {self.game_state["turn"]}. ({current_token_color_turn}).')