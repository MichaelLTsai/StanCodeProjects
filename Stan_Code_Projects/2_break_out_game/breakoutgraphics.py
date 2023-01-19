"""
File: breakoutgraphics.py
Name: 蔡霖
-------------------------
This file shows a bouncing ball animation
by campy library
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10         # Number of rows of bricks
BRICK_COLS = 10         # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 15       # Radius of the ball (in pixels)
PADDLE_WIDTH = 100      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball
SIDE_PADDLE_SPEED = 15


class BreakoutGraphics:
    """
    create a break out game frame by GOval, GLabel, GWindow and GRect
    """

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(paddle_width / 3, paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = "gold"
        self.window.add(self.paddle,
                        x=(self.window.width-paddle_width/3)/2, y=self.window.height-paddle_height-paddle_offset)
        # Create l_paddle and r_paddle for additional function (left and right ball control)
        self.l_paddle = GRect(paddle_width / 3, paddle_height)
        self.l_paddle.filled = True
        self.l_paddle.fill_color = "fuchsia"
        self.window.add(self.l_paddle,
                        x=self.window.width / 2 - self.paddle.width * 1.5,
                        y=self.window.height - paddle_height - paddle_offset)
        self.r_paddle = GRect(paddle_width / 3, paddle_height)
        self.r_paddle.filled = True
        self.r_paddle.fill_color = "fuchsia"
        self.window.add(self.r_paddle,
                        x=(self.window.width + self.paddle.width) / 2,
                        y=self.window.height - paddle_height - paddle_offset)
        # add paddle decorate
        self.paddle_offset = paddle_offset
        self.l_symbol = GLabel("<<<")
        self.l_symbol.font = "-12"
        self.window.add(self.l_symbol,
                        x=self.window.width / 2 - self.paddle.width * 1.5 + (self.paddle.width - self.l_symbol.width)/2,
                        y=self.window.height - paddle_offset)
        self.r_symbol = GLabel(">>>")
        self.r_symbol.font = "-12"
        self.window.add(self.r_symbol,
                        x=self.window.width / 2 + self.paddle.width * 0.5 + (
                                    self.paddle.width - self.r_symbol.width) / 2,
                        y=self.window.height - paddle_offset)
        # Center a filled ball in the graphical window
        self.r = ball_radius
        self.ball = GOval(ball_radius, ball_radius,
                          x=self.paddle.x+(self.paddle.width-self.r)/2, y=(self.window.height-self.r)/2)
        self.ball.filled = True
        self.window.add(self.ball)
        # Set Switch
        self.switch = True
        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0
        # Initialize our mouse listeners
        onmouseclicked(self.ball_speed)
        onmousemoved(self.paddle_move)
        # Initialize score and left_life
        self.__score = self.__used_life = 0
        # Add score board
        self.score_board = GLabel(f"Score:{self.__score}")
        self.score_board.font = "-30"
        self.window.add(self.score_board, x=0, y=self.window.height)
        # Add life board
        self.life_board = GLabel(f"Life:_")
        self.life_board.font = "-30"
        self.window.add(self.life_board, x=self.window.width-self.life_board.width, y=self.window.height)
        # Draw bricks
        brick_ys = BRICK_OFFSET     # the start of y coordinate

        for y in range(1, BRICK_ROWS+1):
            brick_xs = 0  # the start of x coordinate
            for x in range(1, BRICK_COLS+1):
                self.brick = GRect(BRICK_WIDTH, BRICK_HEIGHT)
                self.brick.filled = True
                if y < 3:
                    self.brick.fill_color = "orangered"
                elif y < 5:
                    self.brick.fill_color = "lightsalmon"
                elif y < 7:
                    self.brick.fill_color = "khaki"
                elif y < 9:
                    self.brick.fill_color = "springgreen"
                else:
                    self.brick.fill_color = "royalblue"
                self.window.add(self.brick, x=brick_xs, y=brick_ys)
                brick_xs += BRICK_WIDTH + BRICK_SPACING
            brick_ys += BRICK_HEIGHT + BRICK_SPACING

    def paddle_move(self, mouse):
        self.window.add(self.l_paddle, x=mouse.x-self.paddle.width * 1.5, y=self.paddle.y)
        self.window.add(self.paddle, x=mouse.x-self.paddle.width / 2, y=self.paddle.y)
        self.window.add(self.r_paddle, x=mouse.x + self.paddle.width * 0.5, y=self.paddle.y)
        self.window.add(self.l_symbol,
                        x=mouse.x - self.paddle.width * 1.5 + (self.paddle.width - self.l_symbol.width)/2,
                        y=self.window.height - self.paddle_offset)
        self.window.add(self.r_symbol,
                        x=mouse.x + self.paddle.width * 0.5 + (self.paddle.width - self.r_symbol.width) / 2,
                        y=self.window.height - self.paddle_offset)

    def ball_speed(self, run):
        if self.switch is True:
            self.__dx = random.randint(1, MAX_X_SPEED)
            self.__dy = INITIAL_Y_SPEED
            if random.random() > 0.5:
                self.__dx = -self.__dx
            if random.random() > 0.5:
                self.__dy = -self.__dy
        self.switch = False

    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    def reset_ball(self):
        self.__dx = self.__dy = 0
        self.window.add(self.ball,
                        x=(self.window.width-self.r)/2, y=(self.window.height-self.r)/2)

    def out_ball(self):
        if self.ball.y > self.window.height:
            print("ball out!")
            self.__used_life += 1
            self.switch = True
            self.reset_ball()

    def get_used_life(self):
        return self.__used_life

    def check_object(self, impact):
        if impact is self.paddle or impact is self.l_paddle or impact is self.r_paddle:
            if self.__dy > 0:
                self.__dy = -self.__dy
                if impact is self.paddle:
                    self.__dx *= 0.8
                elif impact is self.l_paddle:
                    self.__dx = -10
                elif impact is self.r_paddle:
                    self.__dx = 10
        elif impact is self.life_board or impact is self.score_board:
            pass
        else:
            self.__dy = -self.__dy
            self.window.remove(impact)
            self.__score += 1

    def get_score(self):
        return self.__score

    def bump(self):
        p1 = self.window.get_object_at(self.ball.x, self.ball.y)
        p2 = self.window.get_object_at(self.ball.x+self.r, self.ball.y)
        p3 = self.window.get_object_at(self.ball.x, self.ball.y+self.r)
        p4 = self.window.get_object_at(self.ball.x+self.r, self.ball.y+self.r)
        if p1 is not None:
            self.check_object(p1)
        elif p2 is not None:
            self.check_object(p2)
        elif p3 is not None:
            self.check_object(p3)
        elif p4 is not None:
            self.check_object(p4)

    def bouncing(self):
        if self.ball.x < 0 or self.ball.x+self.ball.width > self.window.width:
            self.__dx = -self.__dx
        if self.ball.y < 0:
            self.__dy = -self.__dy

    def get_total_bricks(self):
        total_bricks = BRICK_ROWS * BRICK_COLS
        return total_bricks
