from __future__ import division
import pygame
import renderer

import time

class GameEngine (renderer.Renderer):
    def __init__(self):
        super(GameEngine, self).__init__()
        
        self.startup()
        
        self._next_cycle = 0
        self._cycle_delay = 1/30
        
        self.player = 0
    
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
        
        
    def logic(self):
        if time.time() > self._next_cycle:
            return
        
        self._next_cycle = time.time() + self._cycle_delay
    
    def make_move(self, x, y):
        self.tiles[(x,y)] = self.player
        self.player = 1 - self.player
    
    def tile_click(self, x, y):
        # Do stuff to make sure the player can do it
        self.make_move(x,y)

            
        
        