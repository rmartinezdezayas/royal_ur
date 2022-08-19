from agents.agent_interface import Agent

class MetaAgent(Agent):
    '''
    Meta agent is a Machine Learning Neural Network model that learn from the metagame.
    It plays an entire game using some times random plays and other times its own selected as best plays given the game state.
    After finishing playing the game, read all the movement in the game (its own movement and the rival also) and learn if each movement result in winning the game or loosing it.

    This is a very simmple machine learning model which only take into consideration the meta game.
    It does not take into consideration continuous movement, just the best statistical well know decision for winning the game for every game state.

    This is not a reinforcement learning model. It ca be trained just with historical data from games using supervised learning techniques. 
    Also could learn by playing with others and analyzing the game results.
    '''
    def __init__(self, name='MetaAgent'):
        '''pending to create, train and load the model'''
        self.name = name
        self.model = 'load the model'
    
    def decide(self, game_state, options):
        '''pending to implement'''
        pass
        # return model.predict()
