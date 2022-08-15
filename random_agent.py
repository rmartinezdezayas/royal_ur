from agent_interface import Agent
import random

class RandomAgent(Agent):
    '''Choose at random one of the possible options.'''
    def __init__(self, name = 'RandomAgent'):
        self.name = name

    def decide(self, game_state, options):
        return options[random.randint(0, len(options)-1)][0]