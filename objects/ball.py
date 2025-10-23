from typing import Any
from vectors.vector2 import Vector2


class Ball:
    def __init__(
        self,
        radius: float,
        mass: float,
        pos: Vector2,
        vel: Vector2,
        color: tuple[int,int,int] = (255,0,0),
        **extra_properties
    ):
        self.radius = float(radius)
        self.mass = float(mass)
        self.pos = pos.clone()
        self.vel = vel.clone()
        self.extra_properties = extra_properties or {}
        self.color = color
    
    def set_extra_property(self, name: str, value: Any):
         self.extra_properties[name] = value
    
    def get_extra_property(self, name: str):
        return self.extra_properties.get(name, None)