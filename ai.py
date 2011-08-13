import time
import random

def new_ai(game_data, player, out_queue):
    possible_moves = []
    
    for k, v in game_data.items():
        if v == None:
            possible_moves.append(k)
    
    if len(possible_moves) == 0:
        out_queue.put(None)
    
    best_move, best_score = 0, -1
    for x,y in possible_moves:
        vals = (
            (x-1, y-1),
            (x, y-1),
            (x+1, y-1),
            
            (x-1, y),
            (x+1, y),
            
            (x-1, y+1),
            (x, y+1),
            (x+1, y+1),
        )
        
        temp_score = 0
        for v in vals:
            if game_data.get(v) == player:
                temp_score += 1
        
        if temp_score > best_score:
            best_move = x,y
            best_score = temp_score
    
    out_queue.put(best_move)