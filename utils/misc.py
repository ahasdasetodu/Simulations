

import math


def check_for_ball_click(mouse_pos, ball):
    """Check if a ball was clicked and return the ball if so."""
    dx = mouse_pos.x - ball.pos.x
    dy = mouse_pos.y - ball.pos.y
    return True if math.hypot(dx, dy) <= ball.radius else False
