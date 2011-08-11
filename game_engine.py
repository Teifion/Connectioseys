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
        
        self.tiles[(6,5)] = 0
        self.tiles[(6,6)] = 0
        self.tiles[(5,5)] = 1
        self.tiles[(5,6)] = 1
    
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
        
        return True
    
    def tile_click(self, x, y):
        if self.player == 0:
            self.make_move(x,y)
                

            
        
        