import pygame
from engine.input_handler import InputHandler
from engine.physics_engine import PhysicsEngine_v0
from engine.renderer import Renderer
from engine.scene import Scene
from utils.misc import check_for_ball_click
from vectors.vector2 import Vector2
from engine.core import SimulationApplication

class EventHandler:
    def __init__(self):
        self.mouse_down_time = None
        self.mouse_loc = None
    def handle(self,events, scene : Scene, physics_engine: PhysicsEngine_v0):
        mouse_up_event = events.get("MOUSE_UP",None)
        mouse_down_event= events.get("MOUSE_DOWN",None)
        if mouse_down_event or mouse_up_event:
            self.handle_mouse_events(scene, mouse_down_event, mouse_up_event)
        self.handle_button_events(events, physics_engine, scene)
        
    def handle_mouse_events(self, scene, mouse_down_event, mouse_up_event):
        for ball in scene.balls:
            if mouse_down_event:
                self.mouse_down_time = mouse_down_event["ts"]
                self.mouse_loc = mouse_down_event["location"]
            if mouse_down_event and check_for_ball_click(self.mouse_loc, ball):
                ball.color = (0,255,0)
                ball.set_extra_property("selected", True)
            elif mouse_up_event and ball.get_extra_property("selected"):
                ball.color = (255,0,0)
                self.handle_mouse_button_up(ball, self.mouse_loc, self.mouse_down_time) 
                 
    def handle_mouse_button_up(self, ball, mouse_loc, mouse_down_time):
        # Calculate hold duration and apply impulse
        hold_duration = (pygame.time.get_ticks() - mouse_down_time) / 1000.0
        release_pos = Vector2(*pygame.mouse.get_pos())
        
        impulse = release_pos - mouse_loc
        # negate impulse to push ball away from drag direction
        impulse *= -1
        length = impulse.length()
        if length > 0:
            # Scale impulse by hold duration and normalize direction
            impulse *= (min(hold_duration * 500, 10000) / length)
            ball.vel += impulse
        
        ball.set_extra_property("selected", False)
    
    def handle_button_events(self, events, physics_engine, scene):
        for key,_ in events.items():
            if key == "R":
                scene.setup_scene()
            elif key == "SPACE":
                physics_engine.paused = not physics_engine.paused
            elif key == "UP":
                physics_engine.restitution = min(1.0, physics_engine.restitution + 0.05)
            elif key == "DOWN":
                physics_engine.restitution = max(0.0, physics_engine.restitution - 0.05)
            elif key == "LEFT":
                physics_engine.air_friction = max(0.0, physics_engine.air_friction - 0.1)
            elif key == "RIGHT":
                physics_engine.air_friction = min(1.0, physics_engine.air_friction + 0.1)

def main():

    W, H = 800, 600
    scene = Scene(
        world_size=Vector2(W, H),
    )
    
    physics_engine = PhysicsEngine_v0(
        gravity=Vector2(0,0),
        dt=1.0/60, air_friction=0.0,
        restitution=1.0
    )

    scene.setup_scene(num_balls=20)
    
    renderer = Renderer(W, H)
    input_handler = InputHandler()
    event_handler = EventHandler()
    app = SimulationApplication(
        scene=scene,
        physics_engine=physics_engine,
        renderer=renderer,
        input_handler=input_handler,
        event_handler = event_handler
    )
    
    app.run()