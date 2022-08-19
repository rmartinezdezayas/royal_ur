from agents.agent_interface import Agent

class GeminisAgent(Agent):
    '''
    Geminis agent is a Reinforcement Learning Neural Network model that has two Neural Network Models inside.
    Geminis learned playing the game against himself.
    Some times making random decisions and other times making its own decisions.
    
    After a game is finished, all the game states and decisions are analyzed.
    The winner model inside Geminis gets all the winner movements, and the looser model inside Geminis gets all the looser movements.
    Then train each model to determine if a decision  can take to a winning or loosing.
    With this information, the model learns some specific move that are optimal for winning the game. The model learns from the metadata of the game.

    Instead of learning from historical games between other players, he only learns from its own games against himself. This makes him improve all the time
    and not being affected by reading gameplays from weaker players.
    '''
    def __init__(self, name='GeminisAgent'):
        '''pending to create, train and load the model'''
        self.name = name
        self.model = 'load the model'
    
    def decide(self, game_state, options):
        '''pending to implement'''
        pass
        # return model.predict()
