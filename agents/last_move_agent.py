from agents.agent_interface import Agent

class LastMoveAgent(Agent):
    '''Always choose the most advanced token to move.'''
    def __init__(self, name = 'LastMoveAgent'):
        self.name = name

    def decide(self, game_state, options):
        return sorted(options)[-1][0]