# AI and Analytics for The Royal Game of Ur.

'''
    ExpectimaxAgent
    Create a method for getting the score of a game_state by taking a specific move option.
    
    probabilities
    possible outcomes
    0 0 0 0 --> 0
    0 0 0 1 --> 1
    0 0 1 0 --> 1
    0 1 0 0 --> 1
    1 0 0 0 --> 1
    0 0 1 1 --> 2
    0 1 0 1 --> 2
    0 1 1 0 --> 2
    1 0 0 1 --> 2
    1 0 1 0 --> 2
    1 1 0 0 --> 2
    0 1 1 1 --> 3
    1 1 0 1 --> 3
    1 0 1 1 --> 3
    1 1 1 0 --> 3
    1 1 1 1 --> 4
    
    0 -- 1/16 -- 0.0625
    1 -- 4/16 -- 0.25
    2 -- 6/16 -- 0.375
    3 -- 4/16 -- 0.25
    4 -- 1/16 -- 0.0625

    '''