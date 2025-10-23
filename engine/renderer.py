

import pygame

from engine.scene import Scene


class Renderer:
    def __init__(self,
        display_width: int = 800,
        display_height: int = 600,
        show_legend = True
    ):
        self.display_width = display_width
        self.display_height = display_height
        self.clock = None
        self.screen = None
        self.font = None
        self.show_legend = show_legend
    def init(self):
        pygame.init()
        # window size

        self.screen = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Billiard - bouncy balls")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        return self.screen, self.clock
    
    def render(self, scene: Scene, events: dict):
        
        self.screen.fill((255, 255, 255))
        # draw balls
        for ball in scene.balls:
            pygame.draw.circle(self.screen, ball.color, (int(ball.pos.x), int(ball.pos.y)), int(ball.radius))
        # Draw drag indicator if dragging a ball
        # HUD 
        # TODO: this part should be a different component in the app
        if self.show_legend:
            lines = [
                f"Balls: {len(scene.balls)}",
                f"Paused: {True if events.get('SPACE') else False}",
                "Keys: R=restart  Space=pause LMB=clik and drag to bump a ball",
                "L/R=adjust air friction U/D adjust restitution",]
            y = 5
            for line in lines:
                surf = self.font.render(line, True, (0, 0, 0))
                self.screen.blit(surf, (5, y))
                y += surf.get_height() + 2

        pygame.display.flip()
