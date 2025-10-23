

import math
import pygame

from engine.scene import Scene
from vectors.vector2 import Vector2


class InputHandler:
    def __init__(self):
        self.events = {}
    
    def handle(self):
        self.events = {}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.add_event("QUIT")
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.add_event("R")
                elif event.key == pygame.K_SPACE:
                    self.add_event("SPACE")
                elif event.key == pygame.K_UP:
                    self.add_event("UP")
                elif event.key == pygame.K_DOWN:
                    self.add_event("DOWN")
                elif event.key == pygame.K_LEFT:
                    self.add_event("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.add_event("RIGHT")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.add_event("MOUSE_DOWN")
            elif event.type == pygame.MOUSEBUTTONUP:
                self.add_event("MOUSE_UP")
        return self.events
    
    def add_event(self, event_name: str):
        timestamp = pygame.time.get_ticks()
        mouse_pos = Vector2(*pygame.mouse.get_pos())
        self.events[event_name] = {
                "location": mouse_pos,
                "ts" : timestamp
            }

   