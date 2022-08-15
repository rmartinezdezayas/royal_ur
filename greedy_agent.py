from agent_interface import Agent

class GreedyAgent(Agent):
    '''
    Priority on taking rival tokens and taking rossetes.
    Decision-making process of the greedy agent:
    1. Can the agent capture any pieces? If it can, pick the most advanced piece that can make a capturing move, and move it.
    2. Can the agent move any pieces onto rosette tiles? If it can, pick the most advanced piece that can move onto a rosette, and move it.
    3. Move the most advanced piece it can!
    '''
    def __init__(self, name = 'GreedyAgent'):
        self.name = name

    def decide(self, game_state, options):
        # print('---------')
        return self.get_greater_move_that_capture_rival_token(game_state, options) or self.get_greater_option_go_into_rossete_tile(options) or sorted(options)[-1][0]
        # return None or None or None or options[0][0]
        # print('Result')
    
    def get_greater_move_that_capture_rival_token(self, game_state, options):
        light_player_token_positions = [game_state[f'light_token_{token}_position'] for token in range(1,8)]
        dark_player_token_positions = [game_state[f'dark_token_{token}_position'] for token in range(1,8)]
        rival_player_token_positions = light_player_token_positions if game_state['token_color'] == 'dark' else dark_player_token_positions

        # options_to_common_zone = [option if 5 <= option[1] <= 12 else None for option in options]
        options_to_common_zone = list(filter(lambda option: 5 <= option[1] <= 12, options))
        decision = None
        if len(options_to_common_zone) > 0:
            # options_to_common_zone_matching_rival_position = [option if option[1] in rival_player_token_positions else None for option in options_to_common_zone]
            options_to_common_zone_matching_rival_position = list(filter(lambda option: option[1] in rival_player_token_positions, options_to_common_zone))
            if len(options_to_common_zone_matching_rival_position) > 0:
                options_to_common_zone_matching_rival_position.sort(key = lambda x: x[1])
                decision = options_to_common_zone_matching_rival_position[-1][0]
                # print('captured rival token')
        return decision
    
    def get_greater_option_go_into_rossete_tile(self, options):
        # options_to_go_into_rossete_tiles = [option if option[1] in [4, 8, 14] else None for option in options]
        options_to_go_into_rossete_tiles = list(filter(lambda option: option[1] in [4, 8, 14], options))
        decision = None
        if len(options_to_go_into_rossete_tiles) > 0:
            options_to_go_into_rossete_tiles.sort(key = lambda x: x[1])
            decision = options_to_go_into_rossete_tiles[-1][0]
            # print('into rossete')
        return decision