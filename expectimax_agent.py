



from agent_interface import Agent

class ExpectimaxAgent(Agent):
    '''
    This agent look ahead at potential future moves and tries to maximize the espected outcome.
    The potential outcome is define by the formula:
    Σ own pieces advancement - Σ opponent's pieces advancement
    '''
    def __init__(self, name = 'ExpectimaxAgent'):
        self.name = name
    
    def decide(self, game_state, options):
        return options[0][0]