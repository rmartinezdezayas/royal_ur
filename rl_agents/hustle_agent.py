from agents.agent_interface import Agent

class HustleAgent(Agent):
    '''
    Hustle agent is a Reinforcement Learning Neural Network model that learned playing the game against himself.
    Some times making random decisions and other times making its own decisions.

    After a game is finished, all the game states and decisions are analyzed in order to determine if a decision drove to a winning or loosing.
    With this information, the model learns some specific move that are optimal for winning the game. The model learns from the metadata of the game.

    Instead of learning from historical games between other players, he only learns from its own games against himself. This makes him improve all the time
    and not being affected by reading gameplays from weaker players.
    '''
    def __init__(self, name='HustleAgent'):
        '''pending to create, train and load the model'''
        self.name = name
        self.model = 'load the model'
    
    def decide(self, game_state, options):
        '''pending to implement'''
        pass
        # return model.predict()
