



from agents.agent_interface import Agent
from environment import Game

class ExpectimaxAgent(Agent):
    '''
    This agent look ahead at potential future moves and tries to maximize the espected outcome score.
    The potential outcome or score is define by the formula:
    Σ own token advancement - Σ opponent's token advancement
    If by going 2 tiles ahead, an opponent token is taken, that count as +2-(-4)=6
    '''
    def __init__(self, name = 'ExpectimaxAgent', depth=2, dice_rolls=[0, 1, 2, 3, 4]):
        self.name = name
        self.depth = depth
        self.dice_rolls = dice_rolls
        self.dice_roll_probabilities = [(0, 0.0625), (1, 0.25), (2, 0.375), (3, 0.25), (4, 0.0625)]
        self.filered_dice_roll_probabilities = list(filter(lambda x: x[0] in self.dice_rolls, self.dice_roll_probabilities))

    def decide(self, game_state, options):
        
        current_depth = 0
        player_token_color = game_state['token_color']
        options_score = [self.evaluate_option(game_state, option, current_depth, player_token_color, self.filered_dice_roll_probabilities) for option in options]
        return options[options_score.index(max(options_score))][0]
    
    def get_option_score(self, game_state, option):
        rival_player_token_color = 'dark' if game_state['token_color'] == 'light' else 'light'
        rival_player_token_positions = [game_state[f'{rival_player_token_color}_token_{token}_position'] for token in range(1,8)]
        score = option[1] - option[0] - (- option[1] if option[1] in rival_player_token_positions else 0)
        return score
    
    def get_new_game_state_and_options(self, game_state, option, next_desire_dice_roll_result):
        simulated_game = Game(player1=Agent(game_state['turn']), player2=Agent('dummy_agent'), game_state=game_state, log_output=False, auto_start_game_engine=False)
        simulated_game.next_turn(option[0], simulated_game.get_options(), next_desire_dice_roll_result)
        return simulated_game.game_state, simulated_game.get_options()

    def evaluate_option(self, game_state, option, current_depth, player_token_color, dice_roll_probabilities, option_probability=1):
        current_depth += 1
        score = self.get_option_score(game_state, option)*option_probability
        if current_depth < self.depth:
            for i, roll in enumerate(dice_roll_probabilities):
                new_game_state, new_options = self.get_new_game_state_and_options(game_state.copy(), option, next_desire_dice_roll_result=roll[0])
                if len(new_options) > 0:
                    new_options_scores = [self.evaluate_option(new_game_state, new_option, current_depth, new_game_state['token_color'], dice_roll_probabilities, option_probability=roll[1]) for new_option in new_options]
                else:
                    new_options_scores = [0]
                score_sign = 1 if new_game_state['token_color'] == player_token_color else -1
                score += max(new_options_scores)*score_sign
        return score