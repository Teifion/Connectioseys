from __future__ import division
import pygame
from pygame.locals import *

import math
import time

class Renderer (object):
    counter_size = 20
    counter_padding = 3
    tile_size = counter_size + (counter_padding * 2)
    
    columns = 20
    rows = 20
    
    window_width = tile_size * columns
    window_height = tile_size * rows + 40
    
    def __init__(self):
        super(Renderer, self).__init__()
        self.resources = {}
        self.keys_down = {}
        
        self.tiles = {}
        
        self._next_redraw = 0
        self._redraw_delay = 1/30
    
    def set_fps(self, fps):
        self._redraw_delay = 1/fps
    
    def quit():
        pygame.quit()
        sys.exit()
    
    def startup(self):
        pygame.init()
        
        self.surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Connectioseys')
    
    def draw_text(self, text, surface, x, y, colour=(0,0,0), font_name="Helvetica", font_size=20):
        font = pygame.font.SysFont(font_name, font_size)
        
        textobj = font.render(text, 1, colour)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
    
    def redraw(self):
        if time.time() < self._next_redraw:
            return
        
        # First the board
        self.surface.fill((100, 200, 100), pygame.Rect(0, 0, self.window_width, self.window_height-40))
        self.surface.fill((255, 255, 255), pygame.Rect(0, self.window_height-40, self.window_width, 40))
        
        # Now the tiles
        empties = 0
        for k, v in self.tiles.items():
            x, y = k
            
            r = pygame.Rect(
                x * self.tile_size + self.counter_padding,
                y * self.tile_size + self.counter_padding,
                self.counter_size, self.counter_size
            )
            
            if v == None:
                empties += 1
                continue
            elif v == 0:
                self.surface.blit(self.resources['o'], r)
            elif v == 1:
                self.surface.blit(self.resources['x'], r)
        
        # Connections
        white_points = 0
        black_points = 0
        
        for c1, c2 in self.connections:
            if self.tiles[c1] == 1:
                black_points += 1
            else:
                white_points += 1
            
            if (c1[0] + 3, c1[1] + 3) == c2 or (c2[0] + 3, c2[1] + 3) == c1:
                for i in range(-1, 2):
                    j = 0 - i
                
                    start_pos = (
                        c1[0] * self.tile_size + self.counter_size/2 + self.counter_padding + i + 3,
                        c1[1] * self.tile_size + self.counter_size/2 + self.counter_padding + j + 3,
                    )
            
                    end_pos = (
                        c2[0] * self.tile_size + self.counter_size/2 + self.counter_padding + i - 3,
                        c2[1] * self.tile_size + self.counter_size/2 + self.counter_padding + j - 3,
                    )
                
                    if self.tiles[c1] == 0:
                        pygame.draw.line(self.surface, (200, 0, 100), start_pos, end_pos, 2)
                    else:
                        pygame.draw.line(self.surface, (100, 100, 255), start_pos, end_pos, 2)
            else:
                for i in range(-1, 2):
                    j = 0 - i
                
                    start_pos = (
                        c1[0] * self.tile_size + self.counter_size/2 + self.counter_padding - i - 3,
                        c1[1] * self.tile_size + self.counter_size/2 + self.counter_padding + j + 3,
                    )
            
                    end_pos = (
                        c2[0] * self.tile_size + self.counter_size/2 + self.counter_padding - i - 3,
                        c2[1] * self.tile_size + self.counter_size/2 + self.counter_padding + j + 3,
                    )
                
                    if self.tiles[c1] == 0:
                        pygame.draw.line(self.surface, (200, 0, 100), start_pos, end_pos, 2)
                    else:
                        pygame.draw.line(self.surface, (100, 100, 255), start_pos, end_pos, 2)
        
            
        self.draw_text("White: {0} point{1}".format(
            white_points, "" if white_points == 1 else "s"
        ), self.surface, 20, self.window_height - 30)
        
        self.draw_text("Black: {0} point{1}".format(
            black_points, "" if black_points == 1 else "s"
        ), self.surface, 170, self.window_height - 30)
        
        self.draw_text("{0} empty tile{1}".format(
            empties, "" if empties == 1 else "s"
        ), self.surface, 320, self.window_height - 30)
        
        pygame.display.flip()
        self._next_redraw = time.time() + self._redraw_delay
    
    def handle_keydown(self, event):
        self.keys_down[event.key] = time.time()
        self.test_for_keyboard_commands()
        
        if event.key == 32 and not self.in_game:
            self.new_game()

    def handle_keyup(self, event):
        del(self.keys_down[event.key])

    def handle_mousedown(self, event):
        pass

    def handle_mouseup(self, event):
        x, y = event.pos
        tx = int(math.floor(x/self.tile_size))
        ty = int(math.floor(y/self.tile_size))
        
        self.tile_click(tx, ty)

    def handle_mousemove(self, event):
        pass

    def test_for_keyboard_commands(self):
        # Cmd + Q
        if 113 in self.keys_down and 310 in self.keys_down:
            if self.keys_down[310] <= self.keys_down[113]:# Cmd has to be pushed first
                quit()
    
    def new_game(self):
        self.game.__init__()
    
    def start(self):
        self.startup()
        self.new_game()
        
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self.handle_keydown(event)
                
                elif event.type == KEYUP:
                    self.handle_keyup(event)
                
                elif event.type == MOUSEBUTTONUP:
                    self.handle_mouseup(event)
                
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_mousedown(event)
                
                elif event.type == MOUSEMOTION:
                    self.handle_mousemove(event)
                
                elif event.type == QUIT:
                    self.quit()
            
            # Turn based game so we don't need to always update
            self.redraw()
            self.logic()
        
        quit()
