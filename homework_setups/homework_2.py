



from engine.core import SimulationApplication
from engine.input_handler import InputHandler
from engine.physics_engine import PhysicsEngine_v1
from engine.renderer import Renderer
from engine.scene import PlanetScene, Scene
from vectors.vector2 import Vector2

class EventHandler:
    def handle(self,events):
        pass

def main():
    W, H = 800, 600
    scene = PlanetScene(
        world_size=Vector2(W, H),
        ball_amt = 5
    )
    
    physics_engine = PhysicsEngine_v1(
        gravity=Vector2(0,0),
        dt=1.0/60,
        center=Vector2(W/2,H/2),
        wire_radius=100
    )

    scene.setup_scene()
    
    renderer = Renderer(W, H, show_legend= False)
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