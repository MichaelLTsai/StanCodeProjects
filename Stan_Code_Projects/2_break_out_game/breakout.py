"""
File: breakout.py.py
Name: 蔡霖
-------------------------
This file shows a bouncing ball animation
by campy library
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 15      # 100 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    """
    set any break out game factor that relate to animation here
    """

    # Add the animation loop here
    graphics = BreakoutGraphics()
    score = 0
    ttl_bricks = graphics.get_total_bricks()

    while graphics.get_used_life() < NUM_LIVES and score < ttl_bricks:
        graphics.ball.move(graphics.get_dx(), graphics.get_dy())
        graphics.out_ball()
        graphics.bump()
        graphics.bouncing()
        score = graphics.get_score()
        graphics.score_board.text = f"Score:{score}"
        graphics.life_board.text = f"Life:{NUM_LIVES-graphics.get_used_life()}"
        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
