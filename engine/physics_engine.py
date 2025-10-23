from abc import ABC, abstractmethod
import math

import pygame
from engine.scene import Scene
from utils.misc import check_for_ball_click
from vectors.vector2 import Vector2


class BasePhysicsEngine(ABC):

    @abstractmethod
    def simulate(self):
        pass

class PhysicsEngine_v0(BasePhysicsEngine):
    def __init__(self,
            gravity: Vector2 = Vector2(0.0, 0.0),
            dt: float = 1.0 / 60.0,
            air_friction: float = 0.0,
            restitution: float = 1.0,
        ):
        self.gravity = gravity
        self.dt = dt
        self.paused = False
        self.air_friction = air_friction
        self.restitution = restitution
        
    def simulate(self, scene: Scene,  events: dict):
        if self.paused:
            return

        for i in range(len(scene.balls)):
            ball1 = scene.balls[i]                
            self.simulate_object(ball1)
            for j in range(i + 1, len(scene.balls)):
                ball2 = scene.balls[j]
                self.handle_ball_collision(ball1, ball2, self.restitution)
            self.handle_wall_collision(ball1, scene.world_size)
            
    def handle_ball_collision(self, ball1, ball2, restitution):
        dir = Vector2()
        dir = ball2.pos - ball1.pos
        d = dir.length()
        if d == 0.0 or d > ball1.radius + ball2.radius:
            return

        # normalize
        dir *= 1.0 / d

        corr = (ball1.radius + ball2.radius - d) / 2.0
        ball1.pos += -corr*dir
        ball2.pos += corr*dir

        v1 = ball1.vel.dot(dir)
        v2 = ball2.vel.dot(dir)

        m1 = ball1.mass
        m2 = ball2.mass

        # 1D collision resolution along dir
        newV1 = (m1 * v1 + m2 * v2 - m2 * (v1 - v2) * restitution) / (m1 + m2)
        newV2 = (m1 * v1 + m2 * v2 - m1 * (v2 - v1) * restitution) / (m1 + m2)

        ball1.vel += (newV1 - v1) * dir
        ball2.vel += (newV2 - v2) * dir


    def handle_wall_collision(self, ball, world_size):
        if ball.pos.x < ball.radius:
            ball.pos.x = ball.radius
            ball.vel.x = -ball.vel.x
        if ball.pos.x > world_size.x - ball.radius:
            ball.pos.x = world_size.x - ball.radius
            ball.vel.x = -ball.vel.x
        if ball.pos.y < ball.radius:
            ball.pos.y = ball.radius
            ball.vel.y = -ball.vel.y
        if ball.pos.y > world_size.y - ball.radius:
            ball.pos.y = world_size.y - ball.radius
            ball.vel.y = -ball.vel.y

        
    
    def simulate_object(self,ball):
        # Apply air friction (proportional to velocity and radius)
        # Smaller balls experience more air resistance relative to their mass
        friction_factor = 1.0 - (self.air_friction * (30.0 / ball.radius)) * self.dt
        ball.vel *= max(0.0, friction_factor)  # Prevent negative scaling
        
        # velocity change from gravity
        ball.vel += self.gravity * self.dt
        # position update
        ball.pos +=ball.vel * self.dt

    

