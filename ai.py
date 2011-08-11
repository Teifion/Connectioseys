import time
import random

def new_ai(game_data, out_queue):
    possible_moves = []
    
    for k, v in game_data.items():
        if v == None:
            possible_moves.append(k)
    
    out_queue.put(random.choice(possible_moves))