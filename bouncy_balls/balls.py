
import sys
import math
import random
import pygame


class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def set(self, v):
        self.x = v.x
        self.y = v.y

    def clone(self):
        return Vector2(self.x, self.y)

    def add(self, v, s=1.0):
        self.x += v.x * s
        self.y += v.y * s
        return self

    def add_vectors(self, a, b):
        self.x = a.x + b.x
        self.y = a.y + b.y
        return self

    def subtract(self, v, s=1.0):
        self.x -= v.x * s
        self.y -= v.y * s
        return self

    def subtract_vectors(self, a, b):
        self.x = a.x - b.x
        self.y = a.y - b.y
        return self

    def length(self):
        return math.hypot(self.x, self.y)

    def scale(self, s):
        self.x *= s
        self.y *= s

    def dot(self, v):
        return self.x * v.x + self.y * v.y


class Ball:
    def __init__(self, radius, mass, pos, vel):
        self.radius = float(radius)
        self.mass = float(mass)
        self.pos = pos.clone()
        self.vel = vel.clone()

    def simulate(self, dt, gravity, air_friction=0.0):
        # Apply air friction (proportional to velocity and radius)
        # Smaller balls experience more air resistance relative to their mass
        friction_factor = 1.0 - (air_friction * (30.0 / self.radius)) * dt
        self.vel.scale(max(0.0, friction_factor))  # Prevent negative scaling
        
        # velocity change from gravity
        self.vel.add(gravity, dt)
        # position update
        self.pos.add(self.vel, dt)


class PhysicsScene:
    def __init__(self, world_size, gravity=None, dt=1.0 / 60.0):
        self.gravity = gravity or Vector2(0.0, 0.0)
        self.dt = dt
        self.world_size = world_size
        self.paused = False
        self.balls = []
        self.restitution = 1.0
        self.air_friction = 0.0

    def setup_scene(self, num_balls=20):
        self.balls = []
        w, h = self.world_size.x, self.world_size.y
        for _ in range(num_balls):
            radius = 5 + random.random() * 20  # in pixels
            mass = math.pi * (radius ** 2)
            pos = Vector2(random.uniform(radius, w - radius), random.uniform(radius, h - radius))
            vel = Vector2(random.uniform(-100.0, 100.0), random.uniform(-100.0, 100.0))
            self.balls.append(Ball(radius, mass, pos, vel))

    def simulate(self):
        if self.paused:
            return

        for i in range(len(self.balls)):
            ball1 = self.balls[i]
            ball1.simulate(self.dt, self.gravity, self.air_friction)

            for j in range(i + 1, len(self.balls)):
                ball2 = self.balls[j]
                handle_ball_collision(ball1, ball2, self.restitution)

            handle_wall_collision(ball1, self.world_size)


def handle_ball_collision(ball1, ball2, restitution):
    dir = Vector2()
    dir.subtract_vectors(ball2.pos, ball1.pos)
    d = dir.length()
    if d == 0.0 or d > ball1.radius + ball2.radius:
        return

    # normalize
    dir.scale(1.0 / d)

    corr = (ball1.radius + ball2.radius - d) / 2.0
    ball1.pos.add(dir, -corr)
    ball2.pos.add(dir, corr)

    v1 = ball1.vel.dot(dir)
    v2 = ball2.vel.dot(dir)

    m1 = ball1.mass
    m2 = ball2.mass

    # 1D collision resolution along dir
    newV1 = (m1 * v1 + m2 * v2 - m2 * (v1 - v2) * restitution) / (m1 + m2)
    newV2 = (m1 * v1 + m2 * v2 - m1 * (v2 - v1) * restitution) / (m1 + m2)

    ball1.vel.add(dir, newV1 - v1)
    ball2.vel.add(dir, newV2 - v2)


def handle_wall_collision(ball, world_size):
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

def handle_ball_click(mouse_pos, ball):
    """Check if a ball was clicked and return the ball if so."""
    dx = mouse_pos.x - ball.pos.x
    dy = mouse_pos.y - ball.pos.y
    return ball if math.hypot(dx, dy) <= ball.radius else None

def apply_mouse_impulse(ball, start_pos, end_pos, hold_duration):
    """Apply an impulse to a ball based on mouse drag vector and hold duration."""
    impulse = Vector2()
    impulse.subtract_vectors(end_pos, start_pos)
    length = impulse.length()
    if length > 0:
        # Scale impulse by hold duration and normalize direction
        impulse.scale(min(hold_duration * 500, 1000) / length)
        ball.vel.add(impulse)

def draw_drag_indicator(screen, start_pos, current_pos, hold_duration):
    """Draw visual indicators for drag direction and strength."""
    # Draw line showing drag direction
    pygame.draw.line(screen, (0, 255, 0), 
                    (int(start_pos.x), int(start_pos.y)),
                    (int(current_pos[0]), int(current_pos[1])), 2)
    
    # Draw circle showing potential strength
    strength = min(hold_duration * 500, 10000)
    radius = int(strength / 50)  # Scale down for visualization
    pygame.draw.circle(screen, (255, 0, 0), 
                      (int(start_pos.x), int(start_pos.y)), 
                      radius, 1)

def run():
    pygame.init()
    # window size
    W, H = 800, 600
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Billiard - bouncy balls")

    clock = pygame.time.Clock()

    scene = PhysicsScene(Vector2(W, H), gravity=Vector2(0.0, 0.0), dt=1.0 / 60.0)
    scene.setup_scene(num_balls=20)

    font = pygame.font.SysFont(None, 24)

    running = True
    mouse_down_pos = None
    mouse_down_time = None
    selected_ball = None
    
    while running:
        dt_ms = clock.tick(60)
        # keep physics dt fixed to scene.dt; however we can scale velocities to dt_ms/1000 if desired
        
        current_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    scene.setup_scene()
                elif event.key == pygame.K_SPACE:
                    scene.paused = not scene.paused
                elif event.key == pygame.K_UP:
                    scene.restitution = min(1.0, scene.restitution + 0.05)
                elif event.key == pygame.K_DOWN:
                    scene.restitution = max(0.0, scene.restitution - 0.05)
                elif event.key == pygame.K_LEFT:
                    scene.air_friction = max(0.0, scene.air_friction - 0.1)
                elif event.key == pygame.K_RIGHT:
                    scene.air_friction = min(1.0, scene.air_friction + 0.1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Store initial click position and time
                mouse_down_pos = Vector2(*pygame.mouse.get_pos())
                mouse_down_time = pygame.time.get_ticks()
                # Find clicked ball
                for ball in scene.balls:
                    selected_ball = handle_ball_click(mouse_down_pos, ball)
                    if selected_ball:
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                if mouse_down_pos and mouse_down_time and selected_ball:
                    # Calculate hold duration and apply impulse
                    hold_duration = (pygame.time.get_ticks() - mouse_down_time) / 1000.0
                    release_pos = Vector2(*pygame.mouse.get_pos())
                    
                    impulse = Vector2()
                    impulse.subtract_vectors(release_pos, mouse_down_pos)
                    # negate impulse to push ball away from drag direction
                    impulse.scale(-1)
                    length = impulse.length()
                    if length > 0:
                        # Scale impulse by hold duration and normalize direction
                        impulse.scale(min(hold_duration * 500, 10000) / length)
                        selected_ball.vel.add(impulse)
                    
                    
                    mouse_down_pos = None
                    mouse_down_time = None
                    selected_ball = None
        scene.simulate()

        screen.fill((255, 255, 255))



        # draw balls
        for ball in scene.balls:
            color = (0, 255, 0) if ball is selected_ball else (255, 0, 0)
            pygame.draw.circle(screen, color, (int(ball.pos.x), int(ball.pos.y)), int(ball.radius))
        # Draw drag indicator if dragging a ball
        if mouse_down_time and selected_ball:
            current_pos = pygame.mouse.get_pos()
            hold_duration = (pygame.time.get_ticks() - mouse_down_time) / 1000.0
            draw_drag_indicator(screen, selected_ball.pos, current_pos, hold_duration)

        # HUD
        lines = [
            f"Balls: {len(scene.balls)}",
            f"Paused: {scene.paused}",
            f"Restitution: {scene.restitution:.2f}",
            f"Air Friction: {scene.air_friction:.2f}",
            "Keys: R=restart  Space=pause LMB=clik and drag to bump a ball",
            "L/R=adjust air friction U/D adjust restitution",]
        y = 5
        for line in lines:
            surf = font.render(line, True, (0, 0, 0))
            screen.blit(surf, (5, y))
            y += surf.get_height() + 2

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()
