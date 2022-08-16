from distutils.log import error
from agents.agent_interface import Agent

class Human(Agent):
    def __init__(self, name):
        self.name = name

    def decide(self, game_state, options):
        while True:
            try:
                decision = int(input(f'Select an option to play (the first number value of the option).\nThe options are {options}: '))
                if decision in [value[0] for value in options]:
                    break
                else:
                    raise error
            except:
                print('Not a valid option. Try again.')
        return decision