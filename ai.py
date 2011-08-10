import time

class Game_ai (object):
    def __init__(self, game):
        super(Game_ai, self).__init__()
        self.game = game
        self.move = (-1,-1)
    
    def make_move(self):
        raise Exception("Not implimented")