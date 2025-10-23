

import math
import random
from objects.ball import Ball
from vectors.vector2 import Vector2


class Scene:
    def __init__(self,
        world_size: Vector2
    ):
        self.world_size = world_size
        # probably would like to make it into a general container class at some point
        self.balls = []
        
    def setup_scene(self, num_balls: int=20):
        self.balls = []
        w, h = self.world_size.x, self.world_size.y
        for _ in range(num_balls):
            radius = 5 + random.random() * 20  # in pixels
            mass = math.pi * (radius ** 2)
            pos = Vector2(random.uniform(radius, w - radius), random.uniform(radius, h - radius))
            vel = Vector2(random.uniform(-100.0, 100.0), random.uniform(-100.0, 100.0))
            self.balls.append(Ball(radius, mass, pos, vel))