from __future__ import division
import pygame
import renderer

import multiprocessing
import time
import ai

class GameEngine (renderer.Renderer):
    def __init__(self):
        super(GameEngine, self).__init__()
        
        self._next_cycle = 0
        self._cycle_delay = 1/30
        
        self.ai_queue = multiprocessing.Queue()
        self.connections = []
        
        self.player = 0
        
        self.startup()
    
    def quit(self):
        super(GameEngine, self).quit()
    
    def startup(self):
        super(GameEngine, self).startup()
        
        self.resources['x'] = pygame.Surface((self.counter_size, self.counter_size))
        self.resources['x'].fill((0, 0, 0), pygame.Rect(0, 0, self.counter_size, self.counter_size))
        
        self.resources['o'] = pygame.Surface((self.counter_size, self.counter_size))
        self.resources['o'].fill((255, 255, 255), pygame.Rect(0, 0, self.counter_size, self.counter_size))
    
    def set_speed(self, cycles_per_second):
        self._cycle_delay = 1/cycles_per_second
    
    def new_game(self):
        self.tiles = {}
        for x in range(self.columns):
            for y in range(self.rows):
                self.tiles[(x,y)] = None
        
        self.tiles[(2,2)] = 0
        self.tiles[(3,3)] = 0
        self.tiles[(4,4)] = 0
        self.build_connections()
    
    def new_ai(self):
        ai_proc = multiprocessing.Process(
            target = ai.new_ai,
            args=(self.tiles, self.ai_queue)
        )
        
        ai_proc.start()
    
    def check_ai_move(self):
        if self.ai_queue.empty():
            return None
        
        return self.ai_queue.get()
    
    def logic(self):
        if time.time() < self._next_cycle:
            return
        
        ai_move = self.check_ai_move()
        
        if ai_move != None:
            ai_success = self.make_move(*ai_move)
            
            if not ai_success:
                self.new_ai()
        
        self._next_cycle = time.time() + self._cycle_delay
    
    def make_move(self, x, y):
        if self.tiles[(x,y)] != None:
            return False
        
        self.tiles[(x,y)] = self.player
        self.player = 1 - self.player
        
        if self.player == 1:
            self.new_ai()
        
        self.build_connections()
        return True
    
    def tile_click(self, x, y):
        if self.player == 0:
            self.make_move(x,y)
                
    def build_connections(self):
        self.connections = []
        tr_bl_connections = set()# Top right to bottom left
        tl_br_connections = set()# Top left to bottom right
        
        def _check(v, tiles, check_set):
            for t in tiles:
                if self.tiles[t] != v:
                    return False
                
                if t in check_set:
                    return False
            
            return True  
        
        # At the base level we want to get an end-node, if we don't
        # get an end node then we don't care, we'll catch it later
        for x in range(self.columns):
            for y in range(self.rows):
                v = self.tiles[(x,y)]
                
                if v == None:
                    continue
            
                if (x,y) in tr_bl_connections and (x,y) in tl_br_connections:
                    continue
                
                # First try looking up and to the left
                if x > 2 and y > 2:
                    tiles = [
                        (x-1, y-1),
                        (x-2, y-2),
                        (x-3, y-3),
                    ]
            
                    if _check(v, tiles, tl_br_connections):
                        tl_br_connections.add((x, y))
                        tl_br_connections.add((x-1, y-1))
                        tl_br_connections.add((x-2, y-2))
                        tl_br_connections.add((x-3, y-3))
                
                        self.connections.append(((x-3, y-3), (x, y)))
            
                # Now down and to the left
                if x > 2 and y < self.rows-3:
                    tiles = [
                        (x-1, y+1),
                        (x-2, y+2),
                        (x-3, y+3),
                    ]
                
                    if _check(v, tiles, tr_bl_connections):
                        tr_bl_connections.add((x, y))
                        tr_bl_connections.add((x-1, y+1))
                        tr_bl_connections.add((x-2, y+2))
                        tr_bl_connections.add((x-3, y+3))
                
                        self.connections.append(((x-3, y+3), (x, y)))
                
            
        
            
        
        
        
        