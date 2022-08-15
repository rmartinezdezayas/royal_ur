from agent_interface import Agent

class FirstMoveAgent(Agent):
    '''Always choose the least advanced token to move.'''
    def __init__(self, name = 'FirstMoveAgent'):
        self.name = name

    def decide(self, game_state, options):
        return sorted(options)[0][0]