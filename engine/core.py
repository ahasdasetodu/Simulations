

import inspect
import pygame
from engine.input_handler import InputHandler
from engine.renderer import Renderer
from engine.scene import Scene
from engine.physics_engine import BasePhysicsEngine




class SimulationApplication:
    def __init__(
        self,
        scene: Scene,
        physics_engine: BasePhysicsEngine,
        renderer: Renderer,
        input_handler: InputHandler,
        event_handler: callable
    ):
        self.scene = scene
        self.physics_engine = physics_engine
        self.renderer = renderer
        self.input_handler = input_handler
        self.event_handler = event_handler
    
    def run(self):
        _, clock = self.renderer.init()
        running = True
        
        while running:
            dt_ms = clock.tick(60)
            events = self.input_handler.handle()
            self.event_handler.handle(events, **self.get_kwargs_for_event_handler())
            self.physics_engine.simulate(self.scene, events)
            self.renderer.render(self.scene, events)
            if events.get("QUIT", None):
                break

        pygame.quit()
        
    def get_kwargs_for_event_handler(self):
        handler_sig = inspect.signature(self.event_handler.handle)
        kwargs = {}
        
        for name, param in handler_sig.parameters.items():
            # Skip 'events' or any positional-only arguments you pass explicitly
            if name == "events":
                continue
            
            if hasattr(self, name):
                kwargs[name] = getattr(self, name)
            elif param.default is param.empty:
                raise Exception(f"event handler has unexpected required argument {name}")
            # else: optional parameter, skip

        return kwargs
                
    