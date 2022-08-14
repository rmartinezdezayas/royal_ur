import random

class Agent:
    def __init__(self, name):
        '''Initialize the Agent with a custom name.'''
        self.name = name

    def decide(self, game_state, options):
        '''Decides the option to play given the current game state.'''
        pass

class Human:
    def __init__(self, name):
        self.name = name

    def decide(self, game_state, options):
        print(f'The options are {options}')
        decision = input()
        return decision

class RandomAgent(Agent):
    '''Choose at random one of the possible options.'''
    def __init__(self, name = 'RandomAgent'):
        self.name = name

    def decide(self, game_state, options):
        return options[random.randint(0, len(options)-1)][0]

class FirstMoveAgent(Agent):
    '''Always choose the least advanced token to move.'''
    def __init__(self, name = 'FirstMoveAgent'):
        self.name = name

    def decide(self, game_state, options):
        return sorted(options)[0][0]

class LastMoveAgent(Agent):
    '''Always choose the most advanced token to move.'''
    def __init__(self, name = 'LastMoveAgent'):
        self.name = name

    def decide(self, game_state, options):
        return sorted(options)[-1][0]

class GreedyAgent(Agent):
    '''
    Priority on taking rival tokens and taking rossetes.
    Decision-making process of the greedy agent:
    1. Can the agent capture any pieces? If it can, pick the most advanced piece that can make a capturing move, and move it.
    2. Can the agent move any pieces onto rosette tiles? If it can, pick the most advanced piece that can move onto a rosette, and move it.
    3. Move the most advanced piece it can!
    '''
    def __init__(self, name = 'LastMoveAgent'):
        self.name = name

    def decide(self, game_state, options):
        return sorted(options)[-1][0]
    
    # def get_moves_that_capture_rival_tokens(self, game_state, options):
