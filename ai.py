import time
import random

def new_ai(game_data, out_queue):
    possible_moves = []
    
    for k, v in game_data.items():
        if v == None:
            possible_moves.append(k)
    
    if len(possible_moves) > 0:
        out_queue.put(random.choice(possible_moves))
    else:
        out_queue.put(None)